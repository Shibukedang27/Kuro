"""Regression coverage for Decimal globals in the Kuro native code generator."""

import json
import platform
import re
import shutil
import subprocess

import pytest

from test_native_codegen import compile_program_to_codegen, run_codegen


DECIMAL_PROGRAM = (
    "Balance = 1.25;\nCopy = Balance;\n"
    "Add 2 to Balance;\nAdd 0.5 to Balance;\n"
    "Print Balance.\nPrint Copy.\n"
    "Update Balance to Copy * 2;\nPrint Balance.\n"
    "Balance = Balance + 0.5;\nPrint Balance.\n"
    "Z = (0.0 - 1.0) * 0.0;\n"
    "Print Z.\n"
)
DECIMAL_STORAGE_OUTPUT = "3.75\n1.25\n2.5\n3.0\n-0.0\n"


def _tokens_for(source: str) -> list[str]:
    from compiler.self_host import compile_with_kuro_driver

    compiled = compile_with_kuro_driver(source)
    return [str(token) for token in compiled["CompilerOutput"]]


def decimal_storage_bytecode() -> list[str]:
    """Tokens for compiled-generator integration checks in test_native_codegen."""
    return _tokens_for(DECIMAL_PROGRAM)


def _bytecode(*tokens: str, target="x86_64-linux"):
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    return run_codegen(bytecode, target=target)


def _cross_assemble(tmp_path, assembly: str, target: str, triple: str):
    source = tmp_path / f"decimal-storage-{target}.s"
    obj = tmp_path / f"decimal-storage-{target}.o"
    source.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["clang", "-target", triple, "-c", "-x", "assembler", str(source), "-o", str(obj)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert obj.stat().st_size > 0


def test_source_decimal_globals_compile_through_selfhost_and_hosted_emitter():
    tokens, env = compile_program_to_codegen(DECIMAL_PROGRAM, target="x86_64-linux")

    assert env["NativeFailed"] == 0
    assert "BC_STORE_LIST" in tokens and "BC_LOADVAR" in tokens
    assert "BC_ADD" in tokens and "BC_BINOP" in tokens and "BC_PRINT" in tokens
    assert "_kuro_print_float" in env["NativeOut"]


@pytest.mark.parametrize(
    ("target", "triple"),
    [
        ("x86_64-linux", "x86_64-unknown-linux-gnu"),
        ("x86_64-macos", "x86_64-apple-macos"),
        ("aarch64-macos", "arm64-apple-macos11"),
    ],
)
def test_decimal_global_source_cross_assembles_for_supported_targets(tmp_path, target, triple):
    _, env = compile_program_to_codegen(DECIMAL_PROGRAM, target=target)
    assert env["NativeFailed"] == 0
    _cross_assemble(tmp_path, env["NativeOut"], target, triple)


def test_hosted_decimal_global_storage_copy_update_computed_and_signed_zero():
    env = _bytecode(
        "BC_CONST", "1.25", "BC_STORE_LIST", "D1",
        "BC_LOADVAR", "D1", "BC_STORE_LIST", "D2",
        "BC_CONST", "2", "BC_ADD", "D2",
        "BC_LOADVAR", "D2", "BC_CONST", "0.5", "BC_BINOP", "+", "BC_STORE_LIST", "D3",
        "BC_CONST", "-0.0", "BC_STORE_LIST", "Zero",
        "BC_LOADVAR", "D3", "BC_PRINT", "BC_LOADVAR", "Zero", "BC_PRINT",
    )
    assert env["NativeFailed"] == 0
    assert "_kuro_print_float" in env["NativeOut"]


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="executes a Linux x86-64 image",
)
def test_hosted_emitter_decimal_globals_link_and_run(tmp_path):
    _, env = compile_program_to_codegen(DECIMAL_PROGRAM, target="x86_64-linux")
    assembly = tmp_path / "decimal-globals-linux.s"
    executable = tmp_path / "decimal-globals-linux"
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
    assert result.stdout == DECIMAL_STORAGE_OUTPUT
    assert result.stderr == ""


@pytest.mark.skipif(
    not all(shutil.which(tool) for tool in ("clang", "ld.lld", "qemu-aarch64")),
    reason="requires clang, lld and qemu-aarch64",
)
def test_decimal_global_storage_executes_arm64_instructions(tmp_path):
    from test_decimal_formatter import _elfize_macho_assembly

    _, env = compile_program_to_codegen(DECIMAL_PROGRAM, target="aarch64-macos")
    assert env["NativeFailed"] == 0
    # Adapt Mach-O sections/relocations and syscall numbers, not storage/math.
    assembly = _elfize_macho_assembly(env["NativeOut"])
    assembly = re.sub(r"(?m)^\.globl _main$", ".global _start", assembly)
    assembly = re.sub(r"(?m)^_main:$", "_start:", assembly)
    obj = tmp_path / "storage-arm64.o"
    image = tmp_path / "storage-arm64"
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
    assert result.stdout == DECIMAL_STORAGE_OUTPUT
    assert result.stderr == ""
    undefined = subprocess.run(
        ["nm", "-u", str(image)], capture_output=True, text=True, check=True,
    )
    assert undefined.stdout.strip() == ""


def test_decimal_global_update_opcode_accepts_decimal_slot():
    env = _bytecode(
        "BC_CONST", "1.25", "BC_STORE_LIST", "Balance",
        "BC_CONST", "0.25", "BC_UPDATE", "Balance",
        "BC_LOADVAR", "Balance", "BC_PRINT",
    )
    assert env["NativeFailed"] == 0


@pytest.mark.parametrize(
    "tokens",
    [
        # A previously unseen load is an integer slot until proved otherwise.
        ("BC_LOADVAR", "D", "BC_PRINT", "BC_CONST", "1.5", "BC_STORE_LIST", "D", "BC_LOADVAR", "D", "BC_PRINT"),
        # A previously integer slot cannot change to decimal, nor vice versa.
        ("BC_CONST", "1", "BC_STORE_LIST", "Slot", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_CONST", "1", "BC_STORE_LIST", "Slot"),
        ("BC_CONST_TEXT", "text", "BC_STORE_LIST", "Slot", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot"),
        ("BC_CONST", "1.5", "BC_ADD", "Slot"),
        ("BC_CONST", "1.5", "BC_UPDATE", "Slot"),
        # Text writes and nonnumeric arithmetic cannot mutate a decimal slot.
        ("BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_CONST_TEXT", "text", "BC_STORE_LIST", "Slot"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_CONST_TEXT", "text", "BC_ADD", "Slot"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_CONST_TEXT", "text", "BC_UPDATE", "Slot"),
        ("BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_CONST", "1", "BC_UPDATE", "Slot"),
    ],
)
@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_decimal_global_storage_rejects_prior_type_conflicts_and_invalid_mutations(tokens, target):
    env = _bytecode(*tokens, target=target)
    assert env["NativeFailed"] == 1
    assert env["NativeOut"] == ""


@pytest.mark.parametrize(
    "suffix",
    [
        ("BC_FUNC_BEGIN", "DoNothing", "BC_FUNC_END"),
    ],
)
@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_decimal_global_storage_is_rejected_with_actions_even_after_store(suffix, target):
    env = _bytecode("BC_CONST", "1.5", "BC_STORE_LIST", "D", *suffix, target=target)
    assert env["NativeFailed"] == 1
    assert env["NativeOut"] == ""


def test_decimal_action_parameters_keep_legacy_support():
    env = _bytecode(
        "BC_FUNC_BEGIN", "Echo", "BC_PARAM", "Value", "Decimals",
        "BC_LOADVAR", "Value", "BC_RETURN", "BC_FUNC_END",
    )
    assert env["NativeFailed"] == 0


def test_integer_global_addition_remains_compatible():
    tokens, env = compile_program_to_codegen(
        "I = 2;\nAdd 3 to I;\nPrint I.\n", target="x86_64-linux"
    )
    assert env["NativeFailed"] == 0
    assert "BC_ADD" in tokens


@pytest.mark.parametrize("count, expected_failed", [(64, 0), (65, 0), (266, 0), (267, 1)])
def test_decimal_global_capacity_is_bounded(count, expected_failed):
    tokens = ["BC_CONST", "0.5", "BC_STORE_LIST", "D0"]
    for index in range(1, count):
        tokens.extend(("BC_LOADVAR", "D0", "BC_STORE_LIST", f"D{index}"))
    env = _bytecode(*tokens)
    assert env["NativeFailed"] == expected_failed
    if expected_failed == 0:
        assert env["NativeGlobalVariableCount"] == count
    else:
        assert env["NativeOut"] == ""
