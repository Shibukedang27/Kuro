from pathlib import Path
import json
import platform
import subprocess
import pytest

from compiler.pipeline import run_source


ROOT = Path(__file__).resolve().parents[2]
CODEGEN = ROOT / "self_host" / "native_codegen.kuro"

MACOS_ARM64_HOST = (
    platform.system() == "Darwin"
    and platform.machine().lower() in {"arm64", "aarch64"}
)
requires_macos_arm64 = pytest.mark.skipif(
    not MACOS_ARM64_HOST,
    reason="executes the default aarch64-macos native codegen target",
)


def run_codegen(bytecode: str, target: str = "aarch64-macos"):
    codegen = CODEGEN.read_text(encoding="utf-8").replace(
        'NativeTarget = "aarch64-macos";', f'NativeTarget = "{target}";', 1
    )
    stage = f'BytecodeOut = {bytecode};\n' + codegen
    result = run_source(stage)
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    return result.interpreter.env


def run_literal_codegen(value: str):
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return run_codegen(f'"BC_CONST", "{escaped}", "BC_PRINT"')


def compile_program_to_codegen(program: str, target: str = "aarch64-macos"):
    from compiler.self_host import compile_with_kuro_driver

    compiled = compile_with_kuro_driver(program)
    tokens = [str(token) for token in compiled["CompilerOutput"]]
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    return tokens, run_codegen(bytecode, target=target)


def test_kuro_native_codegen_emits_length_for_multichar_literal():
    env = run_codegen('"BC_CONST", "hello", "BC_PRINT"')

    assert env["NativeFailed"] == 0
    assert "mov x2, #5" in env["NativeOut"]
    assert '.asciz "hello"' in env["NativeOut"]


def test_kuro_native_codegen_preserves_numeric_looking_typed_text():
    env = run_codegen('"BC_CONST_TEXT", "1", "BC_PRINT"')

    assert env["NativeFailed"] == 0
    assert "mov x2, #1" in env["NativeOut"]
    assert '.asciz "1"' in env["NativeOut"]


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


@requires_macos_arm64
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
@requires_macos_arm64
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
    ("target", "function_label", "call_instruction", "parameter_store"),
    [
        ("x86_64-linux", ".Lkuro_fn_0:", "call .Lkuro_fn_0", "mov %rdi, 1024(%rsp)"),
        ("aarch64-macos", "L_kuro_fn_0:", "bl L_kuro_fn_0", "str x0, [sp, #1024]"),
    ],
)
def test_kuro_native_codegen_compiles_zero_parameter_integer_action(
    target, function_label, call_instruction, parameter_store
):
    source = "Action FortyTwo;\nReturn 42;\nDone.\nCall FortyTwo;\nPrint @_.\n"
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens == [
        "BC_FUNC_BEGIN", "FortyTwo", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END",
        "BC_CALL_BEGIN", "FortyTwo", "BC_CALL_END", "BC_STORE_LIST", "_",
        "BC_LOADVAR", "_", "BC_PRINT",
    ]
    assert env["NativeFailed"] == 0
    assert function_label in env["NativeOut"]
    assert call_instruction in env["NativeOut"]
    function_start = env["NativeOut"].index(function_label)
    assert parameter_store not in env["NativeOut"][function_start:]


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_supports_conditional_integer_action_returns(target):
    source = (
        "Action Choose Value: Integers;\n"
        "If Value is greater than 0;\n"
        "Return 7;\n"
        "Else;\n"
        "Return 9;\n"
        "Done.\n"
        "Done.\n"
        "Call Choose 1;\n"
        "Print @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens.count("BC_RETURN") == 2
    assert env["NativeFailed"] == 0
    assert env["NativeOut"].count("ret\n") >= 2


def test_kuro_native_codegen_rejects_one_sided_conditional_action_return():
    env = run_codegen(
        '"BC_FUNC_BEGIN", "Broken", "BC_PARAM", "N", "Integers", '
        '"BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "7", "BC_RETURN", '
        '"BC_ELSE_BEGIN", "BC_CONST", "9", "BC_IF_END", "BC_FUNC_END"',
        target="x86_64-linux",
    )

    assert env["NativeFailed"] == 1


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
def test_kuro_native_codegen_compiles_one_parameter_integer_action(tmp_path):
    source = (
        "Action Inc N: Integers;\n"
        "Return N + 1;\n"
        "Done.\n"
        "Call Inc 41;\n"
        "Print @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target="x86_64-linux")

    assert tokens == [
        "BC_FUNC_BEGIN", "Inc", "BC_PARAM", "N", "Integers",
        "BC_LOADVAR", "N", "BC_CONST", "1", "BC_BINOP", "+", "BC_RETURN",
        "BC_FUNC_END", "BC_CALL_BEGIN", "Inc", "BC_CONST", "41", "BC_CALL_END",
        "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
    ]
    assert env["NativeFailed"] == 0
    assert ".Lkuro_fn_0:" in env["NativeOut"]
    assert "call .Lkuro_fn_0" in env["NativeOut"]

    assembly = tmp_path / "action.s"
    executable = tmp_path / "action"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        [
            "clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib",
            "-Wl,-e,_start", "-x", "assembler", str(assembly), "-o", str(executable),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert result.stdout == "42\n"
    assert result.stderr == ""


@pytest.mark.parametrize(
        "bytecode",
    [
        '"BC_FUNC_BEGIN", "Inc", "BC_PARAM", "N", "Text", "BC_CONST", "1", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Inc", "BC_CONST", "41", "BC_CALL_END", "BC_PRINT"',
        '"BC_FUNC_BEGIN", "Inc", "BC_PARAM", "N", "Integers", "BC_LOADVAR", "N", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Inc", "BC_CALL_END", "BC_PRINT"',
        '"BC_FUNC_BEGIN", "FortyTwo", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "FortyTwo", "BC_CONST", "1", "BC_CALL_END", "BC_PRINT"',
    ],
)
def test_kuro_native_codegen_rejects_unsupported_action_signatures(bytecode):
    env = run_codegen(bytecode, target="x86_64-linux")

    assert env["NativeFailed"] == 1


@pytest.mark.parametrize(
    "bytecode",
    [
        '"BC_CONST", "x", "BC_CONST", "2", "BC_BINOP", "+", "BC_PRINT"',
        '"BC_CONST", "10000", "BC_CONST", "2", "BC_BINOP", "+", "BC_PRINT"',
    ],
)
def test_kuro_native_codegen_rejects_invalid_integer_arithmetic(bytecode):
    assert run_codegen(bytecode)["NativeFailed"] == 1


@requires_macos_arm64
def test_kuro_native_codegen_traps_runtime_division_by_zero(tmp_path):
    env = run_codegen('"BC_CONST", "8", "BC_CONST", "0", "BC_BINOP", "/", "BC_PRINT"')
    assembly = tmp_path / "divide-zero.s"
    executable = tmp_path / "divide-zero"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)

    result = subprocess.run([str(executable)], capture_output=True, text=True)
    assert result.returncode == 1
    assert result.stdout == ""


@requires_macos_arm64
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


def test_kuro_native_codegen_rejects_multi_value_collection_assignment():
    env = run_codegen(
        '"BC_MULTI_BEGIN", "BC_CONST", "a", "BC_CONST", "b", '
        '"BC_STORE_MULTI", "Items"'
    )
    assert env["NativeFailed"] == 1


@pytest.mark.parametrize(("left", "right", "expected"), [("2", "3", "1\n"), ("4", "3", "0\n")])
@requires_macos_arm64
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


@requires_macos_arm64
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


@requires_macos_arm64
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


@requires_macos_arm64
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


@pytest.fixture(scope="module")
def x86_linux_codegen(tmp_path_factory):
    from compiler.self_host import build_native_codegen

    # Build once: the generator runs on the local host; output ABI is independent.
    generator = tmp_path_factory.mktemp("kuro-codegen-linux") / "kuro-codegen-linux"
    build_native_codegen(generator, output_target="x86_64-linux")
    return generator


def test_kuro_owned_x86_linux_codegen_cross_assembles(tmp_path, x86_linux_codegen):
    generator = x86_linux_codegen
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


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        (["BC_CONST", "6", "BC_CONST", "7", "BC_BINOP", "*", "BC_PRINT"], "42\n"),
        (["BC_CONST", "2", "BC_CONST", "3", "BC_BINOP", "-", "BC_PRINT"], "-1\n"),
        (["BC_CONST", "8", "BC_CONST", "2", "BC_BINOP", "/", "BC_PRINT"], "4\n"),
        (
            [
                "BC_CONST", "2", "BC_CONST", "3", "BC_CMP", "lt", "BC_IF_BEGIN",
                "BC_CONST", "1", "BC_PRINT", "BC_ELSE_BEGIN", "BC_CONST", "0",
                "BC_PRINT", "BC_IF_END",
            ],
            "1\n",
        ),
        (
            [
                "BC_CONST", "3", "BC_CONST", "2", "BC_CMP", "lt", "BC_IF_BEGIN",
                "BC_CONST", "1", "BC_PRINT", "BC_ELSE_BEGIN", "BC_CONST", "0",
                "BC_PRINT", "BC_IF_END",
            ],
            "0\n",
        ),
        (
            [
                "BC_CONST", "3", "BC_REPEAT_BEGIN", "BC_CONST", "7", "BC_PRINT",
                "BC_REPEAT_END",
            ],
            "7\n7\n7\n",
        ),
        (["BC_CONST", "Kuro Linux", "BC_PRINT"], "Kuro Linux"),
        (
            ["BC_CONST", r"line\nnext", "BC_PRINT"],
            "line\nnext",
        ),
        (
            [
                "BC_CONST", "0", "BC_STORE_LIST", "N", "BC_WHILE_BEGIN",
                "BC_LOADVAR", "N", "BC_CONST", "3", "BC_CMP", "lt", "BC_WHILE_TEST",
                "BC_LOADVAR", "N", "BC_PRINT", "BC_CONST", "1", "BC_ADD", "N", "BC_WHILE_END",
                ],
                "0\n1\n2\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Inc", "BC_PARAM", "N", "Integers",
                    "BC_LOADVAR", "N", "BC_CONST", "1", "BC_BINOP", "+",
                    "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Inc",
                    "BC_CONST", "41", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "42\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "FortyTwo", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "FortyTwo", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "42\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Choose", "BC_PARAM", "Value", "Integers",
                    "BC_LOADVAR", "Value", "BC_CONST", "0", "BC_CMP", "gt", "BC_IF_BEGIN",
                    "BC_CONST", "7", "BC_RETURN", "BC_ELSE_BEGIN", "BC_CONST", "9",
                    "BC_RETURN", "BC_IF_END", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Choose", "BC_CONST", "1", "BC_CALL_END",
                    "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                    "BC_CALL_BEGIN", "Choose", "BC_CONST", "0", "BC_CONST", "1",
                    "BC_BINOP", "-", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "7\n9\n",
            ),
        ],
    )
def test_kuro_owned_x86_linux_codegen_links_and_runs(tmp_path, tokens, expected, x86_linux_codegen):
    generator = x86_linux_codegen
    executable = tmp_path / "kuro-generated-linux"
    generated = subprocess.run(
        [str(generator)],
        input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    subprocess.run(
        [
            "clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib",
            "-Wl,-e,_start", "-x", "assembler", "-", "-o", str(executable),
        ],
        input=generated.stdout,
        capture_output=True,
        text=True,
        check=True,
    )
    result = subprocess.run(
        [str(executable)], capture_output=True, text=True, timeout=5, check=False
    )
    assert result.returncode == 0
    assert result.stdout == expected
    assert result.stderr == ""


def test_native_kuro_codegen_rejects_unknown_output_target(tmp_path):
    from compiler.self_host import SelfHostError, build_native_codegen

    with pytest.raises(SelfHostError, match="unsupported code-generation output target"):
        build_native_codegen(tmp_path / "bad", output_target="x86_64-windows")
