"""Regression coverage for one-shot Repeat initialization of native Decimal globals."""
import json
import platform
import subprocess

import pytest

from compiler.pipeline import run_source
from test_native_codegen import compile_program_to_codegen, run_codegen
from test_native_decimal_control_flow import _cross_assemble
from test_vm_cross import run_kuro_vm


EXACT_ONCE_REPEAT_PROGRAM = (
    "Counter = 1;\n"
    "Repeat 1;\n"
    "Fresh = 1.25;\n"
    "NegativeZero = (0.0 - 1.0) * 0.0;\n"
    "Fresh = Fresh + 0.25;\n"
    "If 1 is equal to 1;\n"
    "Repeat 1;\nFresh = Fresh + 0.5;\nDone.\n"
    "Done.\n"
    "AfterNested = 4.5;\n"
    "Add 1 to Counter;\n"
    "Done.\n"
    "Repeat 1;\nSibling = 2.0;\nSibling = Sibling + 1.0;\nDone.\n"
    "Print Fresh.\nPrint NegativeZero.\nPrint Sibling.\n"
    "Print Fresh + Sibling.\nPrint Counter.\nPrint AfterNested.\n"
)
EXACT_ONCE_REPEAT_OUTPUT = "2.0\n-0.0\n3.0\n5.0\n2\n4.5\n"

LOOP_SEMANTICS_PROGRAM = (
    "Counter = 2; Zero = 0; Pretest = 0; Rounds = 0;\n"
    "Repeat 0; Add 10 to Zero; Done.\n"
    "Repeat Counter; Add 1 to Counter; Done.\n"
    "While Pretest is less than 0; Add 1 to Pretest; Done.\n"
    "While Rounds is less than 2; Add 1 to Rounds; Done.\n"
    "Print Counter.\nPrint Zero.\nPrint Pretest.\nPrint Rounds.\n"
)
LOOP_SEMANTICS_OUTPUT = "4\n0\n0\n2\n"
NEGATIVE_REPEAT_PROGRAM = "N = 0; Repeat -1; Add 1 to N; Done. Print N."


def exact_once_repeat_bytecode() -> list[str]:
    """Return self-hosted bytecode for the shared exact-once Repeat fixture."""
    from compiler.self_host import compile_with_kuro_driver

    compiled = compile_with_kuro_driver(EXACT_ONCE_REPEAT_PROGRAM)
    return [str(token) for token in compiled["CompilerOutput"]]


def loop_init_rejection_cases() -> dict[str, list[str]]:
    """Raw bytecode cases outside the narrow direct Repeat-1 initialization rule."""
    cases = {
        "repeat-zero": [
            "BC_CONST", "0", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "repeat-negative": [
            "BC_CONST", "-1", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "repeat-two": [
            "BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "variable-count": [
            "BC_CONST", "1", "BC_STORE_LIST", "N", "BC_LOADVAR", "N",
            "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
            "BC_REPEAT_END",
        ],
        "expression-count": [
            "BC_CONST", "0", "BC_CONST", "1", "BC_BINOP", "+", "BC_REPEAT_BEGIN",
            "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "while-true": [
            "BC_WHILE_BEGIN", "BC_CONST", "1", "BC_WHILE_TEST", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_WHILE_END",
        ],
        "while-false": [
            "BC_WHILE_BEGIN", "BC_CONST", "0", "BC_WHILE_TEST", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_WHILE_END",
        ],
        "while-condition-first-store": [
            "BC_WHILE_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
            "BC_CONST", "0", "BC_WHILE_TEST", "BC_WHILE_END",
        ],
        "nested-repeat": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1",
            "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
            "BC_REPEAT_END", "BC_REPEAT_END",
        ],
        "under-if": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1",
            "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
            "BC_REPEAT_END", "BC_IF_END",
        ],
        "nested-if-arms": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1", "BC_IF_BEGIN",
            "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_ELSE_BEGIN",
            "BC_CONST", "2.5", "BC_STORE_LIST", "D", "BC_IF_END", "BC_REPEAT_END",
        ],
        "one-sided-if-in-repeat": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "0", "BC_IF_BEGIN",
            "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_IF_END", "BC_REPEAT_END",
        ],
        "repeat-under-skipped-while": [
            "BC_WHILE_BEGIN", "BC_CONST", "0", "BC_WHILE_TEST",
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_REPEAT_END", "BC_WHILE_END",
        ],
        "stale-sibling-permission": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_REPEAT_END",
            "BC_CONST", "0", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "stale-literal-provenance": [
            "BC_CONST", "0", "BC_CONST", "1", "BC_PRINT", "BC_REPEAT_BEGIN",
            "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "text-count-one": [
            "BC_CONST_TEXT", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "decimal-count-one": [
            "BC_CONST", "1.0", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "action-present": [
            "BC_FUNC_BEGIN", "A", "BC_CONST", "1", "BC_RETURN", "BC_FUNC_END",
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "underscore-target": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "_", "BC_REPEAT_END",
        ],
        "mixed-kind": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "D", "BC_CONST", "1", "BC_STORE_LIST", "D",
            "BC_REPEAT_END",
        ],
        "read-before-init": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_LOADVAR", "D", "BC_PRINT",
            "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "integer-to-decimal-inside-exact-once": [
            "BC_CONST", "1", "BC_STORE_LIST", "D", "BC_CONST", "1",
            "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "decimal-to-integer-inside-exact-once": [
            "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "1",
            "BC_REPEAT_BEGIN", "BC_CONST", "1", "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
        "return-after-decimal-store": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
            "BC_CONST", "0", "BC_RETURN", "BC_REPEAT_END",
        ],
        "break-after-decimal-store": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
            "BC_BREAK", "BC_REPEAT_END",
        ],
        "continue-after-decimal-store": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
            "BC_CONTINUE", "BC_REPEAT_END",
        ],
        "fresh-store-in-while-under-repeat": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_WHILE_BEGIN", "BC_CONST", "0",
            "BC_WHILE_TEST", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
            "BC_WHILE_END", "BC_REPEAT_END",
        ],
        "residual-stack": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "9",
            "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_REPEAT_END",
        ],
    }
    return cases


def loop_init_boundary_bytecode(depth=16, global_count=64):
    """Nested empty loops must retain only the outer direct-store permission."""
    tokens = ["BC_CONST", "1", "BC_REPEAT_BEGIN"]
    tokens += ["BC_CONST", "0", "BC_REPEAT_BEGIN"] * (depth - 1)
    tokens += ["BC_REPEAT_END"] * (depth - 1)
    for index in range(global_count):
        tokens += ["BC_CONST", "1.5", "BC_STORE_LIST", f"Slot{index}"]
    return [*tokens, "BC_REPEAT_END", "BC_LOADVAR", f"Slot{global_count - 1}", "BC_PRINT"]


def _bytecode_env(tokens: list[str], target: str):
    encoded = ", ".join(json.dumps(token) for token in tokens)
    return run_codegen(encoded, target=target)


def test_exact_once_repeat_bytecode_has_adjacent_literal_header_and_direct_body_stores():
    tokens = exact_once_repeat_bytecode()
    assert any(tokens[index:index + 3] == ["BC_CONST", "1", "BC_REPEAT_BEGIN"]
               for index in range(len(tokens) - 2))
    assert tokens.count("BC_REPEAT_BEGIN") == 3
    assert tokens.count("BC_STORE_LIST") >= 5


@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_native_codegen_rejects_unsupported_repeat_initialization_shapes(target):
    for case, tokens in loop_init_rejection_cases().items():
        env = _bytecode_env(tokens, target)
        assert env["NativeFailed"] == 1, f"{case} unexpectedly accepted for {target}"
        assert env["NativeOut"] == "", f"{case} emitted assembly for {target}"


@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_exact_once_repeat_keeps_sixteen_loop_and_sixty_four_slot_bounds(target):
    accepted = _bytecode_env(loop_init_boundary_bytecode(), target)
    assert accepted["NativeFailed"] == 0
    for tokens in (loop_init_boundary_bytecode(depth=17),
                   loop_init_boundary_bytecode(global_count=65)):
        rejected = _bytecode_env(tokens, target)
        assert rejected["NativeFailed"] == 1
        assert rejected["NativeOut"] == ""


@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_native_codegen_accepts_one_sided_if_and_retained_repeat_permission(target):
    one_sided_if = [
        "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "7", "BC_PRINT", "BC_IF_END",
    ]
    fresh_after_nested_regions = [
        "BC_CONST", "1", "BC_REPEAT_BEGIN",
        "BC_CONST", "0", "BC_REPEAT_BEGIN", "BC_REPEAT_END",
        "BC_CONST", "1", "BC_IF_BEGIN", "BC_IF_END",
        "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_REPEAT_END",
        "BC_LOADVAR", "D", "BC_PRINT",
    ]
    for label, tokens in (("one-sided-if", one_sided_if),
                          ("fresh-store-after-nested-regions", fresh_after_nested_regions)):
        env = _bytecode_env(tokens, target)
        assert env["NativeFailed"] == 0, f"{label} unexpectedly rejected for {target}"


@pytest.mark.parametrize(
    ("target", "triple"),
    [
        ("x86_64-linux", "x86_64-unknown-linux-gnu"),
        ("x86_64-macos", "x86_64-apple-macos"),
        ("aarch64-macos", "arm64-apple-macos11"),
    ],
)
def test_exact_once_repeat_positive_cross_assembles_for_supported_targets(tmp_path, target, triple):
    _, env = compile_program_to_codegen(EXACT_ONCE_REPEAT_PROGRAM, target=target)
    assert env["NativeFailed"] == 0
    assert "_kuro_print_float" in env["NativeOut"]
    _cross_assemble(tmp_path, env["NativeOut"], target, triple)


def test_exact_once_repeat_matches_interpreter_and_kuro_vm():
    hosted = run_source(EXACT_ONCE_REPEAT_PROGRAM)
    assert hosted.ok, hosted.compile.diags.render_all() if not hosted.compile.ok else hosted.runtime_error
    vm_output, failed = run_kuro_vm(EXACT_ONCE_REPEAT_PROGRAM)
    assert failed in (None, 0)
    assert "".join(f"{value}\n" for value in vm_output) == EXACT_ONCE_REPEAT_OUTPUT
    assert hosted.stdout == EXACT_ONCE_REPEAT_OUTPUT


def test_source_repeat_semantics_evaluate_bounds_once_and_while_pretests():
    hosted = run_source(LOOP_SEMANTICS_PROGRAM)
    assert hosted.ok, hosted.compile.diags.render_all() if not hosted.compile.ok else hosted.runtime_error
    vm_output, failed = run_kuro_vm(LOOP_SEMANTICS_PROGRAM)
    assert failed in (None, 0)
    assert vm_output == [4, 0, 0, 2]
    assert hosted.stdout == LOOP_SEMANTICS_OUTPUT


def test_negative_repeat_vm_skips_but_host_interpreter_rejects_count():
    hosted = run_source(NEGATIVE_REPEAT_PROGRAM)
    assert not hosted.ok
    assert "Repeat count cannot be negative" in str(hosted.runtime_error)
    vm_output, failed = run_kuro_vm(NEGATIVE_REPEAT_PROGRAM)
    assert failed in (None, 0)
    assert vm_output == [0]


def _run_hosted_linux_native(tmp_path, program: str, name: str):
    """Compile and execute one generated x86-64 Linux image without a C runtime."""
    _, env = compile_program_to_codegen(program, target="x86_64-linux")
    assert env["NativeFailed"] == 0
    assembly = tmp_path / f"{name}.s"
    executable = tmp_path / name
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib", "-Wl,-e,_start",
         "-x", "assembler", str(assembly), "-o", str(executable)],
        check=True, capture_output=True, text=True,
    )
    return subprocess.run([str(executable)], check=True, capture_output=True, text=True, timeout=5)


requires_hosted_linux_x86_64 = pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="executes a Linux x86-64 native image",
)


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="executes a Linux x86-64 native image",
)
def test_exact_once_repeat_hosted_linux_native_executes(tmp_path):
    result = _run_hosted_linux_native(tmp_path, EXACT_ONCE_REPEAT_PROGRAM, "exact-once-repeat")
    assert result.stdout == EXACT_ONCE_REPEAT_OUTPUT
    assert result.stderr == ""


@requires_hosted_linux_x86_64
def test_loop_semantics_hosted_linux_native_executes(tmp_path):
    result = _run_hosted_linux_native(tmp_path, LOOP_SEMANTICS_PROGRAM, "loop-semantics")
    assert result.stdout == LOOP_SEMANTICS_OUTPUT
    assert result.stderr == ""


@requires_hosted_linux_x86_64
def test_negative_repeat_hosted_linux_native_skips_body(tmp_path):
    # The host interpreter rejects negative bounds; the VM and generated native
    # program treat this repeat as zero iterations, so assert each behavior separately.
    result = _run_hosted_linux_native(tmp_path, NEGATIVE_REPEAT_PROGRAM, "negative-repeat")
    assert result.stdout == "0\n"
    assert result.stderr == ""
