"""Regression coverage for Decimal globals across native control-flow regions."""
import json
import platform
import re
import shutil
import subprocess

import pytest

from test_native_codegen import compile_program_to_codegen, run_codegen


DECIMAL_CONTROL_FLOW_PROGRAM = (
    "Balance = 1.5;\nChoice = 2.25;\nNoElse = 3.5;\n"
    "RepeatValue = 4.5;\nWhileValue = 0.5;\nNested = 1.25;\n"
    "Counter = 0;\nZero = (0.0 - 1.0) * 0.0;\n"
    "If 1 is equal to 1;\nBalance = Balance + 0.5;\n"
    "Else;\nBalance = Balance + 1.0;\nDone.\n"
    "If 1 is equal to 2;\nChoice = Choice + 0.25;\n"
    "Else;\nChoice = Choice + 0.75;\nDone.\n"
    "If 1 is equal to 2;\nNoElse = NoElse + 9.0;\nDone.\n"
    "Repeat 0;\nAdd 10.0 to RepeatValue;\nDone.\n"
    "Repeat 2;\nAdd 0.25 to RepeatValue;\nDone.\n"
    "While WhileValue is less than 2.0;\nAdd 0.5 to WhileValue;\nDone.\n"
    "If 1 is equal to 1;\n"
    "Repeat 2;\n"
    "While Nested is less than 1.75;\nAdd 0.25 to Nested;\nDone.\n"
    "Done.\nDone.\n"
    "While Counter is less than 2;\nAdd 1 to Counter;\nDone.\n"
    "Print Balance.\nPrint Choice.\nPrint NoElse.\nPrint RepeatValue.\n"
    "Print WhileValue.\nPrint Nested.\nPrint Counter.\nPrint Zero.\n"
)
DECIMAL_CONTROL_FLOW_OUTPUT = "2.0\n3.0\n3.5\n5.0\n2.0\n1.75\n2\n-0.0\n"


def _tokens_for(source: str) -> list[str]:
    from compiler.self_host import compile_with_kuro_driver

    compiled = compile_with_kuro_driver(source)
    return [str(token) for token in compiled["CompilerOutput"]]


def decimal_control_flow_bytecode() -> list[str]:
    """Tokens for the shared Decimal control-flow source program."""
    return _tokens_for(DECIMAL_CONTROL_FLOW_PROGRAM)


def _bytecode(*tokens: str, target="x86_64-linux"):
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    return run_codegen(bytecode, target=target)


def _cross_assemble(tmp_path, assembly: str, target: str, triple: str):
    source = tmp_path / f"decimal-control-flow-{target}.s"
    obj = tmp_path / f"decimal-control-flow-{target}.o"
    source.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["clang", "-target", triple, "-c", "-x", "assembler", str(source), "-o", str(obj)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert obj.stat().st_size > 0


def test_decimal_control_flow_source_compiles_through_selfhost_and_hosted_emitter():
    tokens, env = compile_program_to_codegen(DECIMAL_CONTROL_FLOW_PROGRAM, target="x86_64-linux")

    assert env["NativeFailed"] == 0
    assert tokens.count("BC_IF_BEGIN") >= 3
    assert "BC_REPEAT_BEGIN" in tokens and "BC_WHILE_BEGIN" in tokens
    assert "_kuro_print_float" in env["NativeOut"]


@pytest.mark.parametrize(
    ("target", "triple"),
    [
        ("x86_64-linux", "x86_64-unknown-linux-gnu"),
        ("x86_64-macos", "x86_64-apple-macos"),
        ("aarch64-macos", "arm64-apple-macos11"),
    ],
)
def test_decimal_control_flow_source_cross_assembles_for_supported_targets(tmp_path, target, triple):
    _, env = compile_program_to_codegen(DECIMAL_CONTROL_FLOW_PROGRAM, target=target)
    assert env["NativeFailed"] == 0
    _cross_assemble(tmp_path, env["NativeOut"], target, triple)


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="executes a Linux x86-64 image",
)
def test_hosted_emitter_decimal_control_flow_globals_link_and_run(tmp_path):
    _, env = compile_program_to_codegen(DECIMAL_CONTROL_FLOW_PROGRAM, target="x86_64-linux")
    assembly = tmp_path / "decimal-control-flow-linux.s"
    executable = tmp_path / "decimal-control-flow-linux"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib", "-Wl,-e,_start",
         "-x", "assembler", str(assembly), "-o", str(executable)],
        check=True,
        capture_output=True,
        text=True,
    )
    result = subprocess.run([str(executable)], capture_output=True, text=True, timeout=5)
    assert result.returncode == 0
    assert result.stdout == DECIMAL_CONTROL_FLOW_OUTPUT
    assert result.stderr == ""


@pytest.mark.skipif(
    not all(shutil.which(tool) for tool in ("clang", "ld.lld", "qemu-aarch64")),
    reason="requires clang, lld and qemu-aarch64",
)
def test_decimal_control_flow_executes_arm64_instructions(tmp_path):
    from test_decimal_formatter import _elfize_macho_assembly

    _, env = compile_program_to_codegen(DECIMAL_CONTROL_FLOW_PROGRAM, target="aarch64-macos")
    assert env["NativeFailed"] == 0
    # Adapt Mach-O sections/relocations and syscall numbers, not storage/math.
    assembly = _elfize_macho_assembly(env["NativeOut"])
    assembly = re.sub(r"(?m)^\.globl _main$", ".global _start", assembly)
    assembly = re.sub(r"(?m)^_main:$", "_start:", assembly)
    obj = tmp_path / "control-flow-arm64.o"
    image = tmp_path / "control-flow-arm64"
    subprocess.run(
        ["clang", "--target=aarch64-linux-gnu", "-c", "-x", "assembler", "-", "-o", str(obj)],
        input=assembly, text=True, capture_output=True, check=True,
    )
    subprocess.run(
        ["ld.lld", "-m", "aarch64elf", "-static", "-e", "_start", str(obj), "-o", str(image)],
        capture_output=True, text=True, check=True,
    )
    result = subprocess.run(
        ["qemu-aarch64", str(image)], capture_output=True, text=True, timeout=10, check=True,
    )
    assert result.stdout == DECIMAL_CONTROL_FLOW_OUTPUT
    assert result.stderr == ""
    undefined = subprocess.run(["nm", "-u", str(image)], capture_output=True, text=True, check=True)
    assert undefined.stdout.strip() == ""


@pytest.mark.parametrize(
    "tokens",
    [
        # A first Decimal store inside a conditional is rejected even when both arms assign it.
        ("BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
         "BC_ELSE_BEGIN", "BC_CONST", "2.5", "BC_STORE_LIST", "D", "BC_IF_END"),
        # A zero-count loop still cannot establish the Decimal representation.
        ("BC_CONST", "0", "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
         "BC_REPEAT_END"),
        # Nor may the first Decimal store be hidden in nested regions.
        ("BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1", "BC_REPEAT_BEGIN",
         "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_REPEAT_END", "BC_IF_END"),
        # While includes its condition evaluation in the invariant region.
        ("BC_WHILE_BEGIN", "BC_CONST", "0", "BC_WHILE_TEST",
         "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_WHILE_END"),
        ("BC_WHILE_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
         "BC_CONST", "0", "BC_WHILE_TEST", "BC_WHILE_END"),
        # Closing an inner region must not make the outer body unconditional.
        ("BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "0", "BC_REPEAT_BEGIN",
         "BC_REPEAT_END", "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_IF_END"),
        # Conservative non-Decimal joins block promotion after the region.
        ("BC_CONST", "0", "BC_IF_BEGIN", "BC_CONST", "1", "BC_STORE_LIST", "D",
         "BC_IF_END", "BC_CONST", "1.5", "BC_STORE_LIST", "D"),
        ("BC_CONST", "0", "BC_IF_BEGIN", "BC_LOADVAR", "D", "BC_PRINT",
         "BC_IF_END", "BC_CONST", "1.5", "BC_STORE_LIST", "D"),
        # The special result slot must not leak the last emitted arm's kind.
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "1", "BC_IF_BEGIN",
         "BC_CONST", "1.5", "BC_STORE_LIST", "_", "BC_ELSE_BEGIN",
         "BC_CONST", "2", "BC_STORE_LIST", "_", "BC_IF_END", "BC_LOADVAR", "_", "BC_PRINT"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "0", "BC_REPEAT_BEGIN",
         "BC_CONST", "1.5", "BC_STORE_LIST", "_", "BC_REPEAT_END", "BC_LOADVAR", "_", "BC_PRINT"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_WHILE_BEGIN", "BC_CONST", "0", "BC_WHILE_TEST",
         "BC_CONST", "1.5", "BC_STORE_LIST", "_", "BC_WHILE_END", "BC_LOADVAR", "_", "BC_PRINT"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "1.5", "BC_STORE_LIST", "_",
         "BC_CONST", "0", "BC_IF_BEGIN", "BC_CONST", "2", "BC_STORE_LIST", "_", "BC_IF_END"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "1.5", "BC_STORE_LIST", "_",
         "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "2", "BC_UPDATE", "_", "BC_IF_END"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "1", "BC_STORE_LIST", "_",
         "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST_TEXT", "text", "BC_UPDATE", "_", "BC_IF_END"),
        # Raw bytecode may not carry operand values across statement-region joins.
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_LOADVAR", "D",
         "BC_CONST", "1", "BC_IF_BEGIN", "BC_IF_END", "BC_PRINT"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_LOADVAR", "D",
         "BC_CONST", "0", "BC_REPEAT_BEGIN", "BC_REPEAT_END", "BC_PRINT"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_LOADVAR", "D",
         "BC_WHILE_BEGIN", "BC_CONST", "0", "BC_WHILE_TEST", "BC_WHILE_END", "BC_PRINT"),
        # An untaken arm/loop cannot reinterpret a residual Integer as Decimal.
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "2", "BC_CONST", "0", "BC_IF_BEGIN",
         "BC_CONST", "1.5", "BC_BINOP", "+", "BC_ELSE_BEGIN", "BC_IF_END", "BC_PRINT"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "2", "BC_CONST", "0", "BC_REPEAT_BEGIN",
         "BC_CONST", "1.5", "BC_BINOP", "+", "BC_REPEAT_END", "BC_PRINT"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "2", "BC_WHILE_BEGIN",
         "BC_CONST", "0", "BC_WHILE_TEST", "BC_CONST", "1.5", "BC_BINOP", "+", "BC_WHILE_END", "BC_PRINT"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "1", "BC_STORE_LIST", "_",
         "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_ADD", "_", "BC_IF_END"),
        # Conflicting representations are rejected from either arm, even if unreachable.
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "0", "BC_IF_BEGIN",
         "BC_CONST", "1", "BC_STORE_LIST", "D", "BC_ELSE_BEGIN", "BC_IF_END"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_CONST", "1", "BC_IF_BEGIN",
         "BC_ELSE_BEGIN", "BC_CONST", "1", "BC_STORE_LIST", "D", "BC_IF_END"),
        # A loop cannot switch an established integer to Decimal or Decimal to integer.
        ("BC_CONST", "1", "BC_STORE_LIST", "Slot", "BC_CONST", "0", "BC_REPEAT_BEGIN",
         "BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_REPEAT_END"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_CONST", "0", "BC_REPEAT_BEGIN",
         "BC_CONST", "1", "BC_STORE_LIST", "Slot", "BC_REPEAT_END"),
        # Reading an unknown name first conservatively establishes its non-Decimal kind.
        ("BC_LOADVAR", "D", "BC_PRINT", "BC_CONST", "1.5", "BC_STORE_LIST", "D"),
        # Actions remain unsupported when a Decimal global is present.
        ("BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_FUNC_BEGIN", "Action", "BC_FUNC_END"),
    ],
)
@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_decimal_globals_reject_unsafe_control_flow_and_representation_changes(tokens, target):
    env = _bytecode(*tokens, target=target)
    assert env["NativeFailed"] == 1
    assert env["NativeOut"] == ""


def test_decimal_global_after_empty_control_flow_is_accepted():
    tokens, env = compile_program_to_codegen(
        "If 1 is equal to 2;\nPrint 0.\nDone.\nAmount = 1.5;\nPrint Amount.\n",
        target="x86_64-linux",
    )
    assert env["NativeFailed"] == 0
    assert "BC_IF_BEGIN" in tokens and "_kuro_print_float" in env["NativeOut"]


def test_hosted_decimal_control_flow_bytecode_contains_expected_storage_and_regions():
    env = _bytecode(*decimal_control_flow_bytecode())
    assert env["NativeFailed"] == 0
    assert "_kuro_print_float" in env["NativeOut"]


@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_decimal_update_remains_kind_matched_inside_regions(target):
    env = _bytecode(
        "BC_CONST", "1.5", "BC_STORE_LIST", "D",
        "BC_CONST", "1", "BC_IF_BEGIN",
        "BC_CONST", "2.5", "BC_UPDATE", "D", "BC_IF_END",
        "BC_LOADVAR", "D", "BC_PRINT", target=target,
    )
    assert env["NativeFailed"] == 0
    assert "_kuro_print_float" in env["NativeOut"]
    rejected = _bytecode(
        "BC_CONST", "1.5", "BC_STORE_LIST", "D",
        "BC_CONST", "0", "BC_IF_BEGIN",
        "BC_CONST", "2", "BC_UPDATE", "D", "BC_IF_END", target=target,
    )
    assert rejected["NativeFailed"] == 1
    assert rejected["NativeOut"] == ""


@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_decimal_result_slot_accepts_same_kind_writes_through_regions(target):
    env = _bytecode(
        "BC_CONST", "1.5", "BC_STORE_LIST", "D",
        "BC_CONST", "1.5", "BC_STORE_LIST", "_",
        "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "2.5", "BC_STORE_LIST", "_",
        "BC_ELSE_BEGIN", "BC_CONST", "3.5", "BC_STORE_LIST", "_", "BC_IF_END",
        "BC_CONST", "0", "BC_REPEAT_BEGIN", "BC_CONST", "4.5", "BC_STORE_LIST", "_", "BC_REPEAT_END",
        "BC_LOADVAR", "_", "BC_PRINT", target=target,
    )
    assert env["NativeFailed"] == 0
    assert "_kuro_print_float" in env["NativeOut"]


@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_integer_result_slot_mutations_remain_compatible_inside_regions(target):
    env = _bytecode(
        "BC_CONST", "1.5", "BC_STORE_LIST", "D",
        "BC_CONST", "1", "BC_STORE_LIST", "_",
        "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "2", "BC_ADD", "_",
        "BC_CONST", "3", "BC_UPDATE", "_", "BC_IF_END",
        "BC_LOADVAR", "_", "BC_PRINT", target=target,
    )
    assert env["NativeFailed"] == 0
