from pathlib import Path
import platform
import subprocess
import pytest

from compiler.pipeline import run_source


ROOT = Path(__file__).resolve().parents[2]
CODEGEN = ROOT / "self_host" / "native_codegen.kuro"


def run_codegen(bytecode: str):
    stage = f'BytecodeOut = {bytecode};\n' + CODEGEN.read_text(encoding="utf-8")
    result = run_source(stage)
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    return result.interpreter.env


def run_literal_codegen(value: str):
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return run_codegen(f'"BC_CONST", "{escaped}", "BC_PRINT"')


def test_kuro_native_codegen_emits_length_for_multichar_literal():
    env = run_codegen('"BC_CONST", "hello", "BC_PRINT"')

    assert env["NativeFailed"] == 0
    assert "mov x2, #5" in env["NativeOut"]
    assert '.asciz "hello"' in env["NativeOut"]


def test_kuro_native_codegen_rejects_unsupported_literal_length():
    env = run_literal_codegen("a" * 1000)

    assert env["NativeFailed"] == 1


def test_kuro_native_codegen_converts_three_digit_lengths():
    env = run_literal_codegen("x" * 137)

    assert env["NativeFailed"] == 0
    assert "mov x2, #137" in env["NativeOut"]


def test_kuro_native_codegen_escapes_assembly_string_characters():
    env = run_literal_codegen('a"b\\c\n')

    assert env["NativeFailed"] == 0
    assert '.asciz "a\\"b\\\\c\\n"' in env["NativeOut"]


def test_kuro_native_codegen_output_builds_and_runs(tmp_path):
    env = run_literal_codegen("Kuro native")
    assembly = tmp_path / "kuro-owned.s"
    executable = tmp_path / "kuro-owned"
    assembly.write_text(env["NativeOut"], encoding="utf-8")

    subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)
    result = subprocess.run([str(executable)], capture_output=True, text=True, check=True)

    assert result.stdout == "Kuro native"


@pytest.mark.parametrize(
    ("left", "operator", "right", "expected"),
    [("2", "+", "3", "5\n"), ("2", "-", "3", "-1\n"), ("7", "*", "6", "42\n"), ("8", "/", "2", "4\n")],
)
def test_kuro_native_codegen_builds_integer_arithmetic(tmp_path, left, operator, right, expected):
    env = run_codegen(
        f'"BC_CONST", "{left}", "BC_CONST", "{right}", "BC_BINOP", "{operator}", "BC_PRINT"'
    )
    assembly = tmp_path / "arithmetic.s"
    executable = tmp_path / "arithmetic"
    assembly.write_text(env["NativeOut"], encoding="utf-8")

    assert env["NativeFailed"] == 0
    subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == expected


@pytest.mark.parametrize(
    "bytecode",
    [
        '"BC_CONST", "x", "BC_CONST", "2", "BC_BINOP", "+", "BC_PRINT"',
        '"BC_CONST", "10000", "BC_CONST", "2", "BC_BINOP", "+", "BC_PRINT"',
    ],
)
def test_kuro_native_codegen_rejects_invalid_integer_arithmetic(bytecode):
    assert run_codegen(bytecode)["NativeFailed"] == 1


def test_kuro_native_codegen_traps_runtime_division_by_zero(tmp_path):
    env = run_codegen('"BC_CONST", "8", "BC_CONST", "0", "BC_BINOP", "/", "BC_PRINT"')
    assembly = tmp_path / "divide-zero.s"
    executable = tmp_path / "divide-zero"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)

    result = subprocess.run([str(executable)], capture_output=True, text=True)
    assert result.returncode == 1
    assert result.stdout == ""


def test_kuro_native_codegen_supports_named_integer_variables(tmp_path):
    env = run_codegen(
        '"BC_CONST", "2", "BC_CONST", "3", "BC_BINOP", "+", '
        '"BC_STORE_LIST", "Answer", "BC_LOADVAR", "Answer", "BC_PRINT"'
    )
    assembly = tmp_path / "variables.s"
    executable = tmp_path / "variables"
    assembly.write_text(env["NativeOut"], encoding="utf-8")

    assert env["NativeFailed"] == 0
    subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "5\n"


@pytest.mark.parametrize(("left", "right", "expected"), [("2", "3", "1\n"), ("4", "3", "0\n")])
def test_kuro_native_codegen_supports_comparisons_and_if(tmp_path, left, right, expected):
    env = run_codegen(
        f'"BC_CONST", "{left}", "BC_CONST", "{right}", "BC_CMP", "lt", '
        '"BC_IF_BEGIN", "BC_CONST", "1", "BC_PRINT", "BC_ELSE_BEGIN", '
        '"BC_CONST", "0", "BC_PRINT", "BC_IF_END"'
    )
    assembly = tmp_path / "conditional.s"
    executable = tmp_path / "conditional"
    assembly.write_text(env["NativeOut"], encoding="utf-8")

    assert env["NativeFailed"] == 0
    subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == expected


def test_kuro_native_codegen_rejects_duplicate_else():
    env = run_codegen(
        '"BC_CONST", "1", "BC_IF_BEGIN", "BC_ELSE_BEGIN", '
        '"BC_ELSE_BEGIN", "BC_IF_END"'
    )
    assert env["NativeFailed"] == 1


def test_kuro_native_codegen_supports_repeat(tmp_path):
    env = run_codegen(
        '"BC_CONST", "3", "BC_REPEAT_BEGIN", '
        '"BC_CONST", "1", "BC_PRINT", "BC_REPEAT_END"'
    )
    assembly = tmp_path / "repeat.s"
    executable = tmp_path / "repeat"
    assembly.write_text(env["NativeOut"], encoding="utf-8")

    assert env["NativeFailed"] == 0
    subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "1\n1\n1\n"


def test_kuro_native_codegen_rejects_repeat_stack_imbalance():
    env = run_codegen(
        '"BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1", "BC_REPEAT_END"'
    )
    assert env["NativeFailed"] == 1


def test_kuro_native_codegen_supports_while_and_variable_add(tmp_path):
    env = run_codegen(
        '"BC_CONST", "0", "BC_STORE_LIST", "N", "BC_WHILE_BEGIN", '
        '"BC_LOADVAR", "N", "BC_CONST", "3", "BC_CMP", "lt", '
        '"BC_WHILE_TEST", "BC_LOADVAR", "N", "BC_PRINT", '
        '"BC_CONST", "1", "BC_ADD", "N", "BC_WHILE_END"'
    )
    assembly = tmp_path / "while.s"
    executable = tmp_path / "while"
    assembly.write_text(env["NativeOut"], encoding="utf-8")

    assert env["NativeFailed"] == 0
    subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "0\n1\n2\n"


@pytest.mark.parametrize(
    "bytecode",
    [
        '"BC_WHILE_BEGIN", "BC_WHILE_END"',
        '"BC_WHILE_BEGIN", "BC_CONST", "1", "BC_CONST", "2", '
        '"BC_WHILE_TEST", "BC_WHILE_END"',
        '"BC_CONST", "1", "BC_WHILE_TEST"',
    ],
)
def test_kuro_native_codegen_rejects_malformed_while(bytecode):
    assert run_codegen(bytecode)["NativeFailed"] == 1


def test_native_kuro_codegen_image_consumes_artifact(tmp_path):
    from compiler.self_host import build_native_codegen

    codegen = tmp_path / "kuro-codegen"
    assembly = tmp_path / "generated.s"
    executable = tmp_path / "generated"
    build_native_codegen(codegen)

    generated = subprocess.run(
        [str(codegen)],
        input="kuro.bytecode/1\nBC_CONST\nKuro image\nBC_PRINT\n",
        capture_output=True,
        text=True,
        check=True,
    )
    assembly.write_text(generated.stdout, encoding="utf-8")
    subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "Kuro image"

    rejected = subprocess.run(
        [str(codegen)], input="wrong\nBC_PRINT\n", capture_output=True, text=True
    )
    assert rejected.returncode == 1
    assert rejected.stdout == ""


@pytest.mark.skipif(platform.system() != "Darwin", reason="requires macOS x86-64 linking")
@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        (["BC_CONST", "Hello Kuro", "BC_PRINT"], "Hello Kuro"),
        (["BC_CONST", "6", "BC_CONST", "7", "BC_BINOP", "*", "BC_PRINT"], "42\n"),
        (["BC_CONST", "2", "BC_CONST", "3", "BC_BINOP", "-", "BC_PRINT"], "-1\n"),
        (["BC_CONST", "3", "BC_REPEAT_BEGIN", "BC_CONST", "1", "BC_PRINT", "BC_REPEAT_END"], "1\n1\n1\n"),
        (["BC_CONST", "0", "BC_STORE_LIST", "N", "BC_WHILE_BEGIN",
          "BC_LOADVAR", "N", "BC_CONST", "3", "BC_CMP", "lt", "BC_WHILE_TEST",
          "BC_LOADVAR", "N", "BC_PRINT", "BC_CONST", "1", "BC_ADD", "N",
          "BC_WHILE_END"], "0\n1\n2\n"),
    ],
)
def test_native_kuro_codegen_image_emits_executable_x86_macos(tmp_path, tokens, expected):
    from compiler.self_host import build_native_codegen

    generator = tmp_path / "kuro-codegen-x86"
    executable = tmp_path / "kuro-generated-x86"
    build_native_codegen(generator, target="x86_64-macos", output_target="x86_64-macos")
    generated = subprocess.run(
        [str(generator)], input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
        capture_output=True, text=True, timeout=10, check=True,
    )
    assert ".globl _start" in generated.stdout
    subprocess.run(
        ["clang", "-target", "x86_64-apple-macos", "-nostdlib",
         "-Wl,-e,_start", "-x", "assembler", "-", "-lSystem", "-o", str(executable)],
        input=generated.stdout, capture_output=True, text=True, check=True,
    )
    assert subprocess.run(
        [str(executable)], capture_output=True, text=True, timeout=5, check=True,
    ).stdout == expected


def test_kuro_owned_x86_linux_codegen_cross_assembles(tmp_path):
    from compiler.self_host import build_native_codegen

    # The generator runs on the local host; its output target is independent.
    generator = tmp_path / "kuro-codegen-linux"
    build_native_codegen(generator, output_target="x86_64-linux")
    generated = subprocess.run(
        [str(generator)],
        input="kuro.bytecode/1\nBC_CONST\n6\nBC_CONST\n7\nBC_BINOP\n*\nBC_PRINT\n",
        capture_output=True, text=True, timeout=10, check=True,
    )
    assert "mov $60, %rax" in generated.stdout
    object_file = tmp_path / "generated-linux.o"
    subprocess.run(
        ["clang", "-target", "x86_64-unknown-linux-gnu", "-c",
         "-x", "assembler", "-", "-o", str(object_file)],
        input=generated.stdout, capture_output=True, text=True, check=True,
    )
    assert object_file.read_bytes()[:4] == b"\x7fELF"


def test_native_kuro_codegen_rejects_unknown_output_target(tmp_path):
    from compiler.self_host import SelfHostError, build_native_codegen

    with pytest.raises(SelfHostError, match="unsupported code-generation output target"):
        build_native_codegen(tmp_path / "bad", output_target="x86_64-windows")
