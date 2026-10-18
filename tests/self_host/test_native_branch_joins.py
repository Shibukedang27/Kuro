"""Native definite-initialization joins for bounded top-level If/Else regions."""
import json
import platform
import re
import shutil
import subprocess

import pytest

from test_native_codegen import compile_program_to_codegen, run_codegen
from test_native_decimal_control_flow import _cross_assemble


BRANCH_JOIN_PROGRAM = (
    "Zero = (0.0 - 1.0) * 0.0;\n"
    "If 1 is equal to 1;\nTaken = 1.25;\nElse;\nTaken = 2.5;\nDone.\n"
    "If 1 is equal to 2;\nUntaken = 3.5;\nElse;\nUntaken = 4.75;\nDone.\n"
    "Taken = Taken + 0.75;\nUntaken = Untaken + 0.25;\n"
    "Repeat 2;\nAdd 0.25 to Taken;\nDone.\n"
    "While Untaken is less than 5.5;\nAdd 0.25 to Untaken;\nDone.\n"
    "If 1 is equal to 1;\nCounter = 3;\nElse;\nCounter = 4;\nDone.\n"
    "Print Taken.\nPrint Untaken.\nPrint Zero.\nPrint Counter.\n"
)
BRANCH_JOIN_OUTPUT = "2.5\n5.5\n-0.0\n3\n"


def branch_join_bytecode() -> list[str]:
    """Self-hosted bytecode emitted for the shared positive branch-join fixture."""
    from compiler.self_host import compile_with_kuro_driver

    compiled = compile_with_kuro_driver(BRANCH_JOIN_PROGRAM)
    return [str(token) for token in compiled["CompilerOutput"]]


def branch_join_rejection_cases() -> dict[str, list[str]]:
    """Representative malformed or unsupported raw programs for generator gates."""
    return {
        "then-only-decimal": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot",
            "BC_ELSE_BEGIN", "BC_IF_END",
        ],
        "else-only-decimal": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_ELSE_BEGIN", "BC_CONST", "1.5",
            "BC_STORE_LIST", "Slot", "BC_IF_END",
        ],
        "decimal-without-else": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot",
            "BC_IF_END",
        ],
        "decimal-integer-join": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot",
            "BC_ELSE_BEGIN", "BC_CONST", "2", "BC_STORE_LIST", "Slot", "BC_IF_END",
        ],
        "integer-decimal-join": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "2", "BC_STORE_LIST", "Slot",
            "BC_ELSE_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_IF_END",
        ],
        "decimal-text-join": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot",
            "BC_ELSE_BEGIN", "BC_CONST_TEXT", "word", "BC_STORE_LIST", "Slot", "BC_IF_END",
        ],
        "text-decimal-join": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST_TEXT", "word", "BC_STORE_LIST", "Slot",
            "BC_ELSE_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_IF_END",
        ],
        "integer-text-join": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "2", "BC_STORE_LIST", "Slot",
            "BC_ELSE_BEGIN", "BC_CONST_TEXT", "word", "BC_STORE_LIST", "Slot", "BC_IF_END",
        ],
        "text-integer-join": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST_TEXT", "word", "BC_STORE_LIST", "Slot",
            "BC_ELSE_BEGIN", "BC_CONST", "2", "BC_STORE_LIST", "Slot", "BC_IF_END",
        ],
        "read-before-definite-init": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_LOADVAR", "Slot", "BC_PRINT",
            "BC_ELSE_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_IF_END",
        ],
        "nested-first-decimal": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1", "BC_IF_BEGIN",
            "BC_CONST", "1.5", "BC_STORE_LIST", "Slot", "BC_ELSE_BEGIN",
            "BC_CONST", "2.5", "BC_STORE_LIST", "Slot", "BC_IF_END",
            "BC_ELSE_BEGIN", "BC_CONST", "3.5", "BC_STORE_LIST", "Slot", "BC_IF_END",
        ],
        "loop-first-decimal": [
            "BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot",
            "BC_REPEAT_END",
        ],
        "action-with-decimal-join": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot",
            "BC_ELSE_BEGIN", "BC_CONST", "2.5", "BC_STORE_LIST", "Slot", "BC_IF_END",
            "BC_FUNC_BEGIN", "Unused", "BC_FUNC_END",
        ],
        "residual-stack-across-join": [
            "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_ELSE_BEGIN",
            "BC_CONST", "2.5", "BC_IF_END", "BC_PRINT",
        ],
    }


def _run_raw(tokens, target="x86_64-linux"):
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    return run_codegen(bytecode, target=target)


def test_branch_join_program_selfhosts_and_emits_native_code():
    tokens, env = compile_program_to_codegen(BRANCH_JOIN_PROGRAM, target="x86_64-linux")
    assert env["NativeFailed"] == 0
    assert tokens.count("BC_IF_BEGIN") >= 2
    assert tokens.count("BC_ELSE_BEGIN") >= 2
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
def test_branch_join_program_cross_assembles_for_supported_targets(tmp_path, target, triple):
    _, env = compile_program_to_codegen(BRANCH_JOIN_PROGRAM, target=target)
    assert env["NativeFailed"] == 0
    _cross_assemble(tmp_path, env["NativeOut"], target, triple)


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="executes a Linux x86-64 image",
)
def test_branch_join_program_runs_on_linux(tmp_path):
    _, env = compile_program_to_codegen(BRANCH_JOIN_PROGRAM, target="x86_64-linux")
    assert env["NativeFailed"] == 0
    assembly = tmp_path / "branch-joins-linux.s"
    executable = tmp_path / "branch-joins-linux"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib", "-Wl,-e,_start",
         "-x", "assembler", str(assembly), "-o", str(executable)],
        check=True, capture_output=True, text=True,
    )
    result = subprocess.run([str(executable)], capture_output=True, text=True, timeout=5)
    assert result.returncode == 0
    assert result.stdout == BRANCH_JOIN_OUTPUT
    assert result.stderr == ""


@pytest.mark.skipif(
    not all(shutil.which(tool) for tool in ("clang", "ld.lld", "qemu-aarch64")),
    reason="requires clang, lld and qemu-aarch64",
)
def test_branch_join_program_executes_arm64_instructions(tmp_path):
    from test_decimal_formatter import _elfize_macho_assembly

    _, env = compile_program_to_codegen(BRANCH_JOIN_PROGRAM, target="aarch64-macos")
    assert env["NativeFailed"] == 0
    assembly = _elfize_macho_assembly(env["NativeOut"])
    assembly = re.sub(r"(?m)^\.globl _main$", ".global _start", assembly)
    assembly = re.sub(r"(?m)^_main:$", "_start:", assembly)
    obj = tmp_path / "branch-joins-arm64.o"
    image = tmp_path / "branch-joins-arm64"
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
    assert result.stdout == BRANCH_JOIN_OUTPUT
    assert result.stderr == ""
    undefined = subprocess.run(["nm", "-u", str(image)], capture_output=True, text=True, check=True)
    assert undefined.stdout.strip() == ""


@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
@pytest.mark.parametrize("name,tokens", branch_join_rejection_cases().items(), ids=lambda x: x if isinstance(x, str) else None)
def test_native_branch_join_rejects_unsafe_raw_bytecode(target, name, tokens):
    env = _run_raw(tokens, target=target)
    assert env["NativeFailed"] == 1, name
    assert env["NativeOut"] == "", name
