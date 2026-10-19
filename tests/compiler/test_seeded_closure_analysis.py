"""Independent regression coverage for shallow closure-analysis state copies.

The reference emitter deliberately restores both full-state deep clones and
removes the seedless-function skip, so equality checks compare against the
unpruned legacy fixed point rather than inheriting the optimized implementation.
"""
from __future__ import annotations

import ast
from functools import lru_cache
import inspect
import platform
import shutil
import subprocess
import sys

import pytest

import compiler.native as native
from compiler.ir import IRFunction, IRProgram, Instr
from compiler.pipeline import compile_source
from scripts.profile_seeded_closures import instrumented_emitter, seeded_source


def _ins(op, *args, dest=None):
    return Instr(op, tuple(args), dest)


def _function(name, *body):
    return IRFunction(name, [], list(body))


def _outcome(emitter, program):
    try:
        return ("assembly", emitter(program))
    except native.NativeBackendError as error:
        return ("native-error", type(error), str(error))


@lru_cache(maxsize=1)
def _legacy_unpruned_emitter():
    """Restore exactly two deep clones and remove the one seedless guard."""
    tree = ast.parse(inspect.getsource(native.emit_x86_64_linux))

    class RestoreLegacyAnalysis(ast.NodeTransformer):
        in_analyzer = False
        restored_clones = 0
        removed_guards = 0

        def visit_FunctionDef(self, node):
            if node.name != "analyze_action_closure_returns":
                return self.generic_visit(node)
            previous = self.in_analyzer
            self.in_analyzer = True
            node = self.generic_visit(node)
            self.in_analyzer = previous
            return node

        def visit_Assign(self, node):
            if self.in_analyzer and len(node.targets) == 1:
                target = ast.unparse(node.targets[0])
                if target in {"state", "states[successor]"}:
                    source = None
                    if (
                        isinstance(node.value, ast.Call)
                        and isinstance(node.value.func, ast.Attribute)
                        and node.value.func.attr == "copy"
                        and not node.value.args
                        and not node.value.keywords
                    ):
                        source = ast.unparse(node.value.func.value)
                    elif isinstance(node.value, ast.DictComp):
                        source = ast.unparse(node.value.generators[0].iter.func.value)
                        expected = (
                            "{name: (set(targets), is_known) for name, "
                            "(targets, is_known) in " + source + ".items()}"
                        )
                        assert ast.unparse(node.value) == expected
                    assert source is None or source == (
                        "incoming" if target == "state" else "state"
                    ), f"unexpected clone source for {target}: {source}"
                    if source is not None:
                        self.restored_clones += 1
                        if isinstance(node.value, ast.Call):
                            replacement = ast.parse(
                                "{name: (set(targets), is_known) "
                                "for name, (targets, is_known) in "
                                + source + ".items()}"
                            ).body[0].value
                            node.value = ast.copy_location(replacement, node.value)
            return self.generic_visit(node)

        def visit_If(self, node):
            if any(
                isinstance(part, ast.Name)
                and part.id == "closure_return_constructors"
                for part in ast.walk(node.test)
            ):
                self.removed_guards += 1
                return None
            return self.generic_visit(node)

    transformer = RestoreLegacyAnalysis()
    tree = transformer.visit(tree)
    assert transformer.restored_clones == 2, (
        "reference emitter must restore exactly the incoming/state full clones; "
        f"found {transformer.restored_clones}"
    )
    assert transformer.removed_guards == 1, (
        "reference emitter must remove exactly the seedless skip guard; "
        f"found {transformer.removed_guards}"
    )
    namespace = vars(native).copy()
    exec(
        compile(ast.fix_missing_locations(tree), "<legacy-closure-analysis>", "exec"),
        namespace,
    )
    return namespace["emit_x86_64_linux"], transformer.restored_clones


def _analysis_program():
    """Exercise aliases, a reconverging diamond, loops, call chains and recursion."""
    functions = {
        # Reverse dependency order forces fixed-point propagation across calls.
        "ChainTop": _function(
            "ChainTop", _ins("CALL", "ChainMiddle", dest="got"), _ins("RETURN", "got")
        ),
        "ChainMiddle": _function(
            "ChainMiddle", _ins("CALL", "ChainLeaf", dest="got"), _ins("RETURN", "got")
        ),
        "ChainLeaf": _function(
            "ChainLeaf",
            _ins("CONST", "TargetA", dest="target_name"),
            _ins("CALL", "MakeClosure", "target_name", dest="closure"),
            _ins("RETURN", "closure"),
        ),
        "TargetA": _function("TargetA", _ins("CONST", 17, dest="n"), _ins("RETURN", "n")),
        "TargetB": _function("TargetB", _ins("CONST", 27, dest="n"), _ins("RETURN", "n")),
        # The two CFG arms carry distinct targets through LOADVAR, STORE_LIST,
        # and UPDATE before they reconverge; merging must retain both targets.
        "Diamond": _function(
            "Diamond",
            _ins("CONST", 1, dest="condition"),
            _ins("JUMPF", "right", "condition"),
            _ins("CONST", "TargetA", dest="left_name"),
            _ins("CALL", "MakeClosure", "left_name", dest="candidate"),
            _ins("LOADVAR", "candidate", dest="alias"),
            _ins("STORE_LIST", "box", ["alias"]),
            _ins("UPDATE", "saved", "box"),
            _ins("JUMP", "join"),
            _ins("LABEL", dest="right"),
            _ins("CONST", "TargetB", dest="right_name"),
            _ins("CALL", "MakeClosure", "right_name", dest="candidate"),
            _ins("LOADVAR", "candidate", dest="alias"),
            _ins("STORE_LIST", "box", ["alias"]),
            _ins("UPDATE", "saved", "box"),
            _ins("LABEL", dest="join"),
            _ins("LOADVAR", "saved", dest="result"),
            _ins("RETURN", "result"),
        ),
        # A known closure fact flows around a CFG loop and exits via RETURN.
        "LoopSeeded": _function(
            "LoopSeeded",
            _ins("CONST", "TargetA", dest="target_name"),
            _ins("CALL", "MakeClosure", "target_name", dest="closure"),
            _ins("UPDATE", "saved", "closure"),
            _ins("LABEL", dest="again"),
            _ins("CONST", 1, dest="condition"),
            _ins("JUMPF", "done", "condition"),
            _ins("LOADVAR", "saved", dest="alias"),
            _ins("UPDATE", "saved", "alias"),
            _ins("JUMP", "again"),
            _ins("LABEL", dest="done"),
            _ins("RETURN", "saved"),
        ),
        # A seeded loop can return a closure, but a reconverging scalar return
        # path must invalidate the closure-return summary.
        "LoopUnknown": _function(
            "LoopUnknown",
            _ins("CONST", "TargetA", dest="target_name"),
            _ins("CALL", "MakeClosure", "target_name", dest="closure"),
            _ins("CONST", 1, dest="condition"),
            _ins("JUMPF", "scalar", "condition"),
            _ins("LABEL", dest="again"),
            _ins("CONST", 1, dest="loop_condition"),
            _ins("JUMPF", "known_return", "loop_condition"),
            _ins("JUMP", "again"),
            _ins("LABEL", dest="known_return"),
            _ins("RETURN", "closure"),
            _ins("LABEL", dest="scalar"),
            _ins("CONST", 9, dest="number"),
            _ins("RETURN", "number"),
        ),
        # Each recursive participant has a direct closure seed; call order and
        # recursion must not hide either returned target.
        "SeedRecursiveA": _function(
            "SeedRecursiveA",
            _ins("CALL", "SeedRecursiveB", dest="ignored"),
            _ins("CONST", "TargetA", dest="target_name"),
            _ins("CALL", "MakeClosure", "target_name", dest="closure"),
            _ins("RETURN", "closure"),
        ),
        "SeedRecursiveB": _function(
            "SeedRecursiveB",
            _ins("CALL", "SeedRecursiveA", dest="ignored"),
            _ins("CONST", "TargetB", dest="target_name"),
            _ins("CALL", "MakeClosure", "target_name", dest="closure"),
            _ins("RETURN", "closure"),
        ),
    }
    main = []
    for name in ("ChainTop", "Diamond", "LoopSeeded", "SeedRecursiveA"):
        main.extend((_ins("CALL", name, dest=f"closure_{name}"),
                     _ins("CALL", "Invoke", f"closure_{name}", dest=f"value_{name}")))
    return IRProgram(main=main, functions=functions)


def test_unpruned_deep_clone_reference_matches_control_flow_and_errors():
    program = _analysis_program()
    actual = _outcome(native.emit_x86_64_linux, program)
    assert actual[0] == "assembly"
    legacy_emitter, restored_deep_clones = _legacy_unpruned_emitter()
    assert restored_deep_clones == 2
    assert actual == _outcome(legacy_emitter, program)

    counted_emitter, metrics = instrumented_emitter(native)
    assert counted_emitter(program) == actual[1]
    assert metrics["merge_updates"] > 0, "diamond/loop paths must install merged states"

    # The known closure return mixed with a scalar is rejected at the Invoke
    # consumer; compare complete NativeBackendError type and text as well.
    invalid = IRProgram(
        main=[_ins("CALL", "LoopUnknown", dest="possibly_closure"),
              _ins("CALL", "Invoke", "possibly_closure", dest="result")],
        functions=program.functions,
    )
    outcome = _outcome(native.emit_x86_64_linux, invalid)
    assert outcome[0] == "native-error"
    assert "statically known targets" in outcome[2]
    assert outcome == _outcome(legacy_emitter, invalid)


def test_seeded_source_workload_is_byte_identical_and_has_no_deep_target_copies():
    result = compile_source(seeded_source(200))
    assert result.ok, result.diags.render_all()

    reference, restored_deep_clones = _legacy_unpruned_emitter()
    assert restored_deep_clones == 2
    expected = reference(result.ir)
    actual = native.emit_x86_64_linux(result.ir)
    assert actual == expected

    counted_emitter, metrics = instrumented_emitter(native)
    assert counted_emitter(result.ir) == actual
    assert metrics["analyzer_calls"] >= 2
    assert metrics["body_visits"] > 0
    assert metrics["copied_names"] > 0
    # The analyzer's transfer operations replace local tuples, merges allocate
    # new target sets, and RETURN updates a separate accumulator. Consequently
    # shallow state-map copies must never require a set(targets) full-state clone.
    assert metrics["deep_target_copies"] == 0


@pytest.mark.skipif(
    not (
        sys.platform.startswith("linux")
        and platform.machine().lower() in {"x86_64", "amd64"}
        and shutil.which("gcc")
    ),
    reason="captured-closure native smoke test requires x86-64 Linux and gcc",
)
def test_seeded_source_native_runtime_invokes_both_captured_closures(tmp_path):
    result = compile_source(seeded_source(200))
    assert result.ok, result.diags.render_all()
    assembly = native.emit_x86_64_linux(result.ir)
    asm_path = tmp_path / "seeded_closures.s"
    exe_path = tmp_path / "seeded_closures"
    asm_path.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["gcc", "-nostdlib", "-no-pie", str(asm_path), "-o", str(exe_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    completed = subprocess.run([str(exe_path)], check=True, capture_output=True, text=True)
    assert completed.stdout == "17\n27\n"
