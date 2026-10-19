#!/usr/bin/env python3
"""Small test fixtures for closure work-queue and sticky RETURN ordering.

The nine-instruction ``QueueWitness`` body is a compact handcrafted witness,
not a claim of global minimality. Its RETURN accumulator is intentionally
sticky: once a known target has been added, a later unknown path clears
``all_returns_known`` but does not retract that target.
"""
from __future__ import annotations


def _ins(op, *args, dest=None):
    from compiler.ir import Instr
    return Instr(op, tuple(args), dest)


def _fn(name, *body):
    from compiler.ir import IRFunction
    return IRFunction(name, [], list(body))


def _program(function_name, body):
    from compiler.ir import IRProgram
    target = _fn("QueueTarget", _ins("CONST", 17, dest="n"), _ins("RETURN", "n"))
    witness = _fn(function_name, *body)
    return IRProgram(main=[], functions={"QueueTarget": target, function_name: witness})


def minimal_sticky_return_program():
    """Return closure-or-missing through one join; nine body instructions."""
    return _program("QueueWitness", [
        _ins("CONST", "QueueTarget", dest="name"),
        _ins("CALL", "MakeClosure", "name", dest="c"),
        _ins("CONST", 1, dest="cond"),
        _ins("JUMPF", "unknown", "cond"),
        _ins("JUMP", "join"),
        _ins("LABEL", dest="unknown"),
        _ins("LOADVAR", "absent", dest="c"),
        _ins("LABEL", dest="join"),
        _ins("RETURN", "c"),
    ])


def layout_swapped_predecessor_program():
    """Same known/unknown join with physical layout swapping arrival order."""
    return _program("LayoutWitness", [
        _ins("CONST", "QueueTarget", dest="name"),
        _ins("CALL", "MakeClosure", "name", dest="c"),
        _ins("CONST", 1, dest="cond"),
        # Fallthrough is now unknown and the label successor is known. Under
        # production LIFO scheduling this reverses which predecessor arrives first.
        _ins("JUMPF", "known", "cond"),
        _ins("LOADVAR", "absent", dest="c"),
        _ins("JUMP", "join"),
        _ins("LABEL", dest="known"),
        _ins("JUMP", "join"),
        _ins("LABEL", dest="join"),
        _ins("RETURN", "c"),
    ])


def bounded_adversarial_cases():
    """Return a bounded set of existing and focused CFG stress fixtures.

    Existing builders intentionally provide independent multiple-backedge,
    missing-name-join, and alternate-return-path shapes for schedule replay.
    """
    from scripts.audit_normalized_closures import multibackedge_workload
    from scripts.profile_sparse_closures import closure_edge_workloads, generated_graph_workload

    edge_cases = closure_edge_workloads()
    return {
        "multiple_backedges_and_missing_name_join": multibackedge_workload(0),
        "generated_missing_name_return_join": generated_graph_workload(1, "missing"),
        "missing_target_return_path": edge_cases["missing_target_return"],
        "loop_zero_path_return": edge_cases["loop_zero_path_unknown"],
        "unreachable_return_path": edge_cases["unreachable_scalar_return"],
    }


def traced_outcome(program, *, mode="production", reverse_successors=False, native=None):
    """Emit a program and return its outcome plus the audit trace."""
    if native is None:
        import compiler.native as native
    from scripts.audit_normalized_closures import make_emitter

    emitter, trace = make_emitter(
        native, mode=mode, trace=True, reverse_successors=reverse_successors,
    )
    try:
        outcome = {"kind": "assembly", "assembly": emitter(program)}
    except native.NativeBackendError as error:
        outcome = {
            "kind": "native-error",
            "type": f"{type(error).__module__}.{type(error).__qualname__}",
            "text": str(error),
        }
    return outcome, trace
