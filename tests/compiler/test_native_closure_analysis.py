"""Differential and profiling tests for native closure-return analysis.

The baseline emitter below is a test-only AST clone of the current Linux
emitter with only the named seedless-function ``continue`` guard removed. It
therefore exercises the legacy, unpruned fixed-point worklist without relying
on a Git checkout, a saved baseline file, or implementation details beyond the
optimization's explicit guard name. Equality of full assembly (or of the
reported NativeBackendError) checks that pruning changes work, not results.
"""

import ast
from functools import lru_cache
import inspect
import random
import sys

import compiler.native as native
from compiler.ir import IRFunction, IRProgram, Instr


def _fn(name, *body):
    return IRFunction(name, [], list(body))


def _i(op, *args, dest=None):
    return Instr(op, tuple(args), dest)


@lru_cache(maxsize=1)
def _unpruned_emitter():
    """Clone emit_x86_64_linux with just the seedless-skip guard removed."""
    tree = ast.parse(inspect.getsource(native.emit_x86_64_linux))

    class RemoveSeedlessSkip(ast.NodeTransformer):
        removed = 0

        def visit_If(self, node):
            if any(
                isinstance(part, ast.Name)
                and part.id == "closure_return_constructors"
                for part in ast.walk(node.test)
            ):
                self.removed += 1
                return None
            return self.generic_visit(node)

    transformer = RemoveSeedlessSkip()
    tree = transformer.visit(tree)
    assert transformer.removed == 1, "expected exactly one named pruning guard"
    namespace = vars(native).copy()
    exec(compile(ast.fix_missing_locations(tree), "<unpruned-native-emitter>", "exec"), namespace)
    return namespace["emit_x86_64_linux"]


def _emission_result(emit, program):
    try:
        return ("assembly", emit(program))
    except native.NativeBackendError as error:
        return ("native-error", type(error), str(error))


def _assert_matches_unpruned(program, case):
    expected = _emission_result(_unpruned_emitter(), program)
    actual = _emission_result(native.emit_x86_64_linux, program)
    assert actual == expected, f"optimized/unpruned mismatch for {case}"


def _handcrafted_program():
    """Cover direct/forwarded/merged returns and seedless control-flow cases."""
    functions = {
        # Insertion before Direct checks that fixed-point propagation is not
        # tied to function declaration order.
        "Forward": _fn("Forward", _i("CALL", "Direct", dest="got"), _i("RETURN", "got")),
        "Target": _fn("Target", _i("CONST", 17, dest="n"), _i("RETURN", "n")),
        "OtherTarget": _fn("OtherTarget", _i("CONST", 29, dest="n"), _i("RETURN", "n")),
        "Direct": _fn(
            "Direct",
            _i("CONST", "Target", dest="name"),
            _i("CALL", "MakeClosure", "name", dest="closure"),
            _i("RETURN", "closure"),
        ),
        "Branch": _fn(
            "Branch",
            _i("CONST", 1, dest="condition"),
            _i("JUMPF", "right", "condition"),
            _i("CONST", "OtherTarget", dest="left_name"),
            _i("CALL", "MakeClosure", "left_name", dest="left_closure"),
            _i("RETURN", "left_closure"),
            _i("LABEL", dest="right"),
            _i("CALL", "Direct", dest="right_closure"),
            _i("RETURN", "right_closure"),
        ),
        # One branch returns a known closure, the other a scalar; the mixed
        # return must not seed a known closure-return summary.
        "Mixed": _fn(
            "Mixed",
            _i("CONST", 1, dest="condition"),
            _i("JUMPF", "scalar", "condition"),
            _i("CONST", "Target", dest="name"),
            _i("CALL", "MakeClosure", "name", dest="known"),
            _i("RETURN", "known"),
            _i("LABEL", dest="scalar"),
            _i("CONST", 4, dest="number"),
            _i("RETURN", "number"),
        ),
        "MixedForward": _fn(
            "MixedForward", _i("CALL", "Mixed", dest="mixed"), _i("RETURN", "mixed")
        ),
        # Recursive seedless call cycle, a loop, an unreachable constructor,
        # and an empty function exercise paths that cannot create a seed.
        "Recursive": _fn(
            "Recursive", _i("CALL", "Recursive", dest="again"), _i("RETURN", "again")
        ),
        "Loop": _fn(
            "Loop",
            _i("LABEL", dest="start"),
            _i("CONST", 1, dest="condition"),
            _i("JUMPF", "done", "condition"),
            _i("JUMP", "start"),
            _i("LABEL", dest="done"),
            _i("RETURN", "condition"),
        ),
        "UnreachableConstructor": _fn(
            "UnreachableConstructor",
            _i("JUMP", "reachable"),
            _i("CONST", "Target", dest="name"),
            _i("CALL", "MakeClosure", "name", dest="closure"),
            _i("RETURN", "closure"),
            _i("LABEL", dest="reachable"),
            _i("CONST", 0, dest="zero"),
            _i("RETURN", "zero"),
        ),
        "Empty": _fn("Empty"),
    }
    return IRProgram(main=[
        _i("CALL", "Forward", dest="forwarded"),
        _i("CALL", "Invoke", "forwarded", dest="first_result"),
        _i("CALL", "Branch", dest="branched"),
        _i("CALL", "Invoke", "branched", dest="second_result"),
    ], functions=functions)


def _randomized_program(seed):
    """Small deterministic valid-shape IR mixtures with varied call graphs."""
    rng = random.Random(seed)
    names = [f"Action{n}" for n in range(7)]
    target = "Action6"
    functions = {}
    # The concrete closure target is always present, but the other functions
    # randomly mix scalar returns, calls, direct constructors, and branches.
    functions[target] = _fn(target, _i("CONST", 23, dest="value"), _i("RETURN", "value"))
    for index, name in enumerate(names[:-1]):
        mode = rng.randrange(5)
        callee = rng.choice(names)
        if mode == 0:
            body = [_i("CONST", rng.randrange(10), dest="value"), _i("RETURN", "value")]
        elif mode == 1:
            body = [_i("CALL", callee, dest="value"), _i("RETURN", "value")]
        elif mode == 2:
            body = [
                _i("CONST", target, dest="name"),
                _i("CALL", "MakeClosure", "name", dest="closure"),
                _i("RETURN", "closure"),
            ]
        elif mode == 3:
            body = [
                _i("CONST", 1, dest="condition"),
                _i("JUMPF", "else", "condition"),
                _i("CALL", callee, dest="left"),
                _i("RETURN", "left"),
                _i("LABEL", dest="else"),
                _i("CONST", rng.randrange(10), dest="right"),
                _i("RETURN", "right"),
            ]
        else:
            # Explicitly exercise a recursive edge and a return with no
            # locally-created target.
            body = [_i("CALL", name, dest="value"), _i("RETURN", "value")]
        functions[name] = _fn(name, *body)
    # Shuffle non-target insertion order to vary forward-reference behavior.
    order = names[:-1]
    rng.shuffle(order)
    shuffled = {name: functions[name] for name in order}
    shuffled[target] = functions[target]
    main = []
    for name, function in shuffled.items():
        if any(item.op == "CALL" and item.args[0] == "MakeClosure" for item in function.body):
            main.extend((
                _i("CALL", name, dest=f"closure_{name}"),
                _i("CALL", "Invoke", f"closure_{name}", dest=f"result_{name}"),
            ))
    return IRProgram(main=main, functions=shuffled)


def test_closure_return_analysis_matches_unpruned_fixedpoint():
    """Pruning is observationally neutral on hand-built and seeded IR graphs."""
    program = _handcrafted_program()
    assert _emission_result(native.emit_x86_64_linux, program)[0] == "assembly"
    _assert_matches_unpruned(program, "handcrafted CFG/call cases")
    mixed = IRProgram(main=[
        _i("CALL", "MixedForward", dest="maybe_closure"),
        _i("CALL", "Invoke", "maybe_closure", dest="result"),
    ], functions=program.functions)
    outcome = _emission_result(native.emit_x86_64_linux, mixed)
    assert outcome[0] == "native-error"
    assert "statically known targets" in outcome[2]
    _assert_matches_unpruned(mixed, "mixed known/unknown closure invocation")
    for seed in (3, 17, 41, 89):
        _assert_matches_unpruned(_randomized_program(seed), f"deterministic IR seed {seed}")


def _count_analyzer_calls(program):
    calls = 0

    def profile(frame, event, arg):
        nonlocal calls
        if event == "call" and frame.f_code.co_name == "analyze_action_closure_returns":
            calls += 1

    previous = sys.getprofile()
    sys.setprofile(profile)
    try:
        native.emit_x86_64_linux(program)
    finally:
        sys.setprofile(previous)
    return calls


def test_seedless_large_bodies_skip_return_analyzer_but_productive_functions_do_not():
    """Count nested analyzer calls, not elapsed time, to prevent timing flakiness."""
    functions = {}
    count = 24
    for index in range(count):
        body = []
        for item in range(24):
            # Calls have destinations, but all callees are seedless, so no
            # returned-target set can ever be introduced into this graph.
            body.append(_i("CALL", f"Seedless{(index + 1) % count}", dest=f"t{item}"))
        body.extend((_i("CONST", index, dest="result"), _i("RETURN", "result")))
        name = f"Seedless{index}"
        functions[name] = _fn(name, *body)
    seedless = IRProgram(main=[], functions=functions)
    assert _count_analyzer_calls(seedless) == 0

    productive = _handcrafted_program()
    assert _count_analyzer_calls(productive) > 0
