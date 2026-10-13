from pathlib import Path
import json
import platform
import re
import subprocess
import pytest

from compiler.pipeline import run_source


ROOT = Path(__file__).resolve().parents[2]
CODEGEN = ROOT / "self_host" / "native_codegen.kuro"
NESTED_CHOICE_ACTION_TOKENS = [
    "BC_FUNC_BEGIN", "Choose", "BC_PARAM", "Value", "Integers",
    "BC_LOADVAR", "Value", "BC_CONST", "10", "BC_CMP", "lt", "BC_IF_BEGIN",
    "BC_LOADVAR", "Value", "BC_CONST", "5", "BC_CMP", "lt", "BC_IF_BEGIN",
    "BC_CONST", "11", "BC_RETURN", "BC_ELSE_BEGIN", "BC_CONST", "12", "BC_RETURN",
    "BC_IF_END", "BC_ELSE_BEGIN", "BC_LOADVAR", "Value", "BC_CONST", "20", "BC_CMP",
    "lt", "BC_IF_BEGIN", "BC_CONST", "13", "BC_RETURN", "BC_ELSE_BEGIN", "BC_CONST",
    "14", "BC_RETURN", "BC_IF_END", "BC_IF_END", "BC_FUNC_END",
]


def nested_choice_program(argument):
    return [
        *NESTED_CHOICE_ACTION_TOKENS,
        "BC_CALL_BEGIN", "Choose", "BC_CONST", str(argument), "BC_CALL_END",
        "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
    ]


def action_control_flow_program():
    return (
        "Action First;\n"
        "N = 0;\n"
        "If 1 is equal to 1;\nAdd 1 to N;\nDone.\n"
        "Repeat 1;\nAdd 1 to N;\nDone.\n"
        "While N is less than 3;\nAdd 1 to N;\nDone.\n"
        "Return N;\nDone.\n"
        "Action Second;\n"
        "M = 0;\n"
        "If 1 is equal to 1;\nAdd 1 to M;\nDone.\n"
        "Repeat 1;\nAdd 1 to M;\nDone.\n"
        "While M is less than 3;\nAdd 1 to M;\nDone.\n"
        "Return M;\nDone.\n"
        "Action RaiseToThree Value: Integers;\n"
        "While Value is less than 3;\nAdd 1 to Value;\nDone.\n"
        "Return Value;\nDone.\n"
        "T = 0;\nWhile T is less than 1;\nAdd 1 to T;\nDone.\n"
        "Call First;\nPrint @_.\n"
        "Call Second;\nPrint @_.\n"
        "Call RaiseToThree 0;\nPrint @_.\n"
        "Print T.\n"
    )


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


@pytest.mark.parametrize(
    ("target", "function_label", "zero_return_instruction"),
    [
        ("x86_64-linux", ".Lkuro_fn_0:", "xor %eax, %eax"),
        ("aarch64-macos", "L_kuro_fn_0:", "mov x0, #0"),
    ],
)
@pytest.mark.parametrize(
    "source",
    [
        "Action Show;\nPrint 42.\nDone.\nCall Show;\nPrint @_.\n",
        "Action Echo N: Integers;\nPrint N.\nDone.\nCall Echo 42;\nPrint @_.\n",
    ],
)
def test_kuro_native_codegen_compiles_zero_return_integer_action(
    source, target, function_label, zero_return_instruction
):
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens.count("BC_FUNC_END") == 1
    assert tokens.count("BC_RETURN") == 0
    assert "BC_CALL_END" in tokens
    assert env["NativeFailed"] == 0
    function_start = env["NativeOut"].index(function_label)
    function_end = env["NativeOut"].find("_kuro_print_int:", function_start)
    if function_end < 0:
        function_end = len(env["NativeOut"])
    function_assembly = env["NativeOut"][function_start:function_end]
    assert zero_return_instruction in function_assembly
    assert "ret\n" in function_assembly


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


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_supports_nested_conditional_integer_action_returns(target):
    source = (
        "Action Choose Value: Integers;\n"
        "If Value is less than 10;\n"
        "If Value is less than 5;\n"
        "Return 11;\n"
        "Else;\n"
        "Return 12;\n"
        "Done.\n"
        "Else;\n"
        "If Value is less than 20;\n"
        "Return 13;\n"
        "Else;\n"
        "Return 14;\n"
        "Done.\n"
        "Done.\n"
        "Done.\n"
        "Call Choose 7;\n"
        "Print @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens.count("BC_IF_BEGIN") == 3
    assert tokens.count("BC_RETURN") == 4
    assert env["NativeFailed"] == 0
    assert env["NativeOut"].count("ret\n") >= 4


@pytest.mark.parametrize(
    ("target", "triple"),
    [("x86_64-linux", "x86_64-unknown-linux-gnu"), ("aarch64-macos", "arm64-apple-macos")],
)
def test_kuro_native_codegen_keeps_action_control_flow_labels_unique(target, triple, tmp_path):
    tokens, env = compile_program_to_codegen(action_control_flow_program(), target=target)

    assert tokens.count("BC_FUNC_BEGIN") == 3
    assert tokens.count("BC_IF_BEGIN") == 2
    assert tokens.count("BC_REPEAT_BEGIN") == 2
    assert tokens.count("BC_WHILE_BEGIN") == 4
    assert env["NativeFailed"] == 0
    labels = re.findall(
        r"^L_kuro_(?:else|endif|repeat|endrepeat|while|endwhile)_\d+:$",
        env["NativeOut"],
        re.MULTILINE,
    )
    assert len(labels) == 16
    assert len(labels) == len(set(labels))
    object_file = tmp_path / f"action-control-flow-{target}.o"
    subprocess.run(
        ["clang", "-target", triple, "-c", "-x", "assembler", "-", "-o", str(object_file)],
        input=env["NativeOut"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert object_file.stat().st_size > 0


def test_kuro_native_codegen_rejects_one_sided_conditional_action_return():
    env = run_codegen(
        '"BC_FUNC_BEGIN", "Broken", "BC_PARAM", "N", "Integers", '
        '"BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "7", "BC_RETURN", '
        '"BC_ELSE_BEGIN", "BC_CONST", "9", "BC_IF_END", "BC_FUNC_END"',
        target="x86_64-linux",
    )

    assert env["NativeFailed"] == 1


def test_kuro_native_codegen_rejects_nested_action_with_fallthrough_path():
    env = run_codegen(
        '"BC_FUNC_BEGIN", "Unsafe", "BC_CONST", "1", "BC_IF_BEGIN", '
        '"BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "11", "BC_RETURN", '
        '"BC_CONST", "12", "BC_RETURN", "BC_ELSE_BEGIN", "BC_CONST", "13", '
        '"BC_RETURN", "BC_CONST", "14", "BC_RETURN", "BC_IF_END", '
        '"BC_ELSE_BEGIN", "BC_CONST", "1", "BC_IF_BEGIN", "BC_ELSE_BEGIN", '
        '"BC_IF_END", "BC_IF_END", "BC_FUNC_END"',
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


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_compiles_two_parameter_integer_action(target, tmp_path):
    source = (
        "Action FortyTwo;\n"
        "Return 42;\n"
        "Done.\n"
        "Action Combine A: Integers, B: Integers;\n"
        "Return A * 10 + B;\n"
        "Done.\n"
        "Call Combine 4, 2;\n"
        "Print @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens == [
        "BC_FUNC_BEGIN", "FortyTwo", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END",
        "BC_FUNC_BEGIN", "Combine", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers",
        "BC_LOADVAR", "A", "BC_CONST", "10", "BC_BINOP", "*", "BC_LOADVAR", "B",
        "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Combine",
        "BC_CONST", "4", "BC_CONST", "2", "BC_CALL_END", "BC_STORE_LIST", "_",
        "BC_LOADVAR", "_", "BC_PRINT",
    ]
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert ".Lkuro_fn_1:" in env["NativeOut"]
        assert "mov %rdi, 1024(%rsp)\n    mov %rsi, 1032(%rsp)\n" in env["NativeOut"]
        assert "mov 1024(%rsp), %rax" in env["NativeOut"]
        assert "mov 1032(%rsp), %rax" in env["NativeOut"]
        assert "mov 0(%rsp), %rdi\n    mov 8(%rsp), %rsi\n" in env["NativeOut"]
        assert "call .Lkuro_fn_1" in env["NativeOut"]
    else:
        assert "L_kuro_fn_1:" in env["NativeOut"]
        assert "str x0, [sp, #1024]\n    str x1, [sp, #1032]\n" in env["NativeOut"]
        assert "ldr x0, [sp, #1024]" in env["NativeOut"]
        assert "ldr x0, [sp, #1032]" in env["NativeOut"]
        assert "ldr x0, [sp, #0]\n    ldr x1, [sp, #8]\n" in env["NativeOut"]
        assert "bl L_kuro_fn_1" in env["NativeOut"]
        assembly = tmp_path / "two-parameter-arm64.s"
        object_file = tmp_path / "two-parameter-arm64.o"
        assembly.write_text(env["NativeOut"], encoding="utf-8")
        subprocess.run(
            ["clang", "-target", "arm64-apple-macos11", "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert object_file.stat().st_size > 0
        if MACOS_ARM64_HOST:
            executable = tmp_path / "two-parameter-arm64"
            subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)
            result = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
            assert result.stdout == "42\n"


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_compiles_three_parameter_integer_action(target, tmp_path):
    source = (
        "Action FortyTwo;\n"
        "Return 42;\n"
        "Done.\n"
        "Action Combine A: Integers, B: Integers, C: Integers;\n"
        "Return A * 100 + B * 10 + C;\n"
        "Done.\n"
        "Call Combine 1, 2, 3;\n"
        "Print @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens == [
        "BC_FUNC_BEGIN", "FortyTwo", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END",
        "BC_FUNC_BEGIN", "Combine", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers",
        "BC_PARAM", "C", "Integers", "BC_LOADVAR", "A", "BC_CONST", "100", "BC_BINOP", "*",
        "BC_LOADVAR", "B", "BC_CONST", "10", "BC_BINOP", "*", "BC_BINOP", "+",
        "BC_LOADVAR", "C", "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END",
        "BC_CALL_BEGIN", "Combine", "BC_CONST", "1", "BC_CONST", "2", "BC_CONST", "3",
        "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
    ]
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert ".Lkuro_fn_1:" in env["NativeOut"]
        assert "mov %rdi, 1024(%rsp)\n    mov %rsi, 1032(%rsp)\n    mov %rdx, 1040(%rsp)\n" in env["NativeOut"]
        assert "mov 1040(%rsp), %rax" in env["NativeOut"]
        assert "mov 0(%rsp), %rdi\n    mov 8(%rsp), %rsi\n    mov 16(%rsp), %rdx\n" in env["NativeOut"]
        assert "call .Lkuro_fn_1" in env["NativeOut"]
    else:
        assert "L_kuro_fn_1:" in env["NativeOut"]
        assert "str x0, [sp, #1024]\n    str x1, [sp, #1032]\n    str x2, [sp, #1040]\n" in env["NativeOut"]
        assert "ldr x0, [sp, #1040]" in env["NativeOut"]
        assert "ldr x0, [sp, #0]\n    ldr x1, [sp, #8]\n    ldr x2, [sp, #16]\n" in env["NativeOut"]
        assert "bl L_kuro_fn_1" in env["NativeOut"]
        assembly = tmp_path / "three-parameter-arm64.s"
        object_file = tmp_path / "three-parameter-arm64.o"
        assembly.write_text(env["NativeOut"], encoding="utf-8")
        subprocess.run(
            ["clang", "-target", "arm64-apple-macos11", "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert object_file.stat().st_size > 0
        if MACOS_ARM64_HOST:
            executable = tmp_path / "three-parameter-arm64"
            subprocess.run(["clang", str(assembly), "-o", str(executable)], check=True)
            result = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
            assert result.stdout == "123\n"


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
@pytest.mark.parametrize(
    ("source", "text_parameter_offset", "x86_register", "arm_register"),
    [
        (
            "Action EchoPair Count: Integers, Word: Text;\n"
            "Print Word.\nReturn Count;\nDone.\n"
            'Call EchoPair 7, "hello";\nPrint @_.\n',
            "1032",
            "rsi",
            "x1",
        ),
        (
            "Action EchoPair Word: Text, Count: Integers;\n"
            "Print Word.\nReturn Count;\nDone.\n"
            'Call EchoPair "world", 9;\nPrint @_.\n',
            "1024",
            "rdi",
            "x0",
        ),
        (
            "Action EchoTriple First: Integers, Count: Integers, Last: Text;\n"
            "Print Last.\nReturn First + Count;\nDone.\n"
            'Call EchoTriple 2, 3, "tail";\nPrint @_.\n',
            "1040",
            "rdx",
            "x2",
        ),
    ],
)
def test_kuro_native_codegen_compiles_mixed_integer_text_action_parameters(
    target, source, text_parameter_offset, x86_register, arm_register, tmp_path
):
    tokens, env = compile_program_to_codegen(source, target=target)

    assert "BC_CONST_TEXT" in tokens
    assert "Text" in tokens
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert f"mov %{x86_register}, {text_parameter_offset}(%rsp)" in env["NativeOut"]
        assert "lea L_kuro_text_constant_0(%rip), %rax" in env["NativeOut"]
        assert "L_kuro_text_len_0:" in env["NativeOut"]
        clang_target = "x86_64-unknown-linux-gnu"
    else:
        assert f"str {arm_register}, [sp, #{text_parameter_offset}]" in env["NativeOut"]
        assert "adrp x0, L_kuro_text_constant_0@PAGE" in env["NativeOut"]
        assert "L_kuro_text_len_0:" in env["NativeOut"]
        clang_target = "arm64-apple-macos11"

    assembly = tmp_path / f"mixed-text-{target}.s"
    object_file = tmp_path / f"mixed-text-{target}.o"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", clang_target, "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_file.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
@pytest.mark.parametrize(
    ("source", "x86_prologue", "x86_call", "arm_prologue", "arm_call"),
    [
        (
            "Action Select Middle: Integers, First: Decimals, Last: Decimals;\n"
            "Return Middle;\nDone.\nCall Select 42, 0.5, 2.25;\nPrint @_.\n",
            "mov %rdi, 1024(%rsp)\n    movsd %xmm0, 1032(%rsp)\n    movsd %xmm1, 1040(%rsp)",
            "mov 0(%rsp), %rdi\n    movsd 8(%rsp), %xmm0\n    movsd 16(%rsp), %xmm1",
            "str x0, [sp, #1024]\n    str d0, [sp, #1032]\n    str d1, [sp, #1040]",
            "ldr x0, [sp, #0]\n    ldr d0, [sp, #8]\n    ldr d1, [sp, #16]",
        ),
        (
            "Action Select First: Decimals, Middle: Integers, Last: Decimals;\n"
            "Return Middle;\nDone.\nCall Select 0.5, 42, 2.25;\nPrint @_.\n",
            "movsd %xmm0, 1024(%rsp)\n    mov %rdi, 1032(%rsp)\n    movsd %xmm1, 1040(%rsp)",
            "movsd 0(%rsp), %xmm0\n    mov 8(%rsp), %rdi\n    movsd 16(%rsp), %xmm1",
            "str d0, [sp, #1024]\n    str x0, [sp, #1032]\n    str d1, [sp, #1040]",
            "ldr d0, [sp, #0]\n    ldr x0, [sp, #8]\n    ldr d1, [sp, #16]",
        ),
    ],
)
def test_kuro_native_codegen_mixes_decimal_and_integer_abi_registers(
    target, source, x86_prologue, x86_call, arm_prologue, arm_call, tmp_path
):
    tokens, env = compile_program_to_codegen(source, target=target)

    assert "Decimals" in tokens
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert x86_prologue in env["NativeOut"]
        assert x86_call in env["NativeOut"]
        clang_target = "x86_64-unknown-linux-gnu"
    else:
        assert arm_prologue in env["NativeOut"]
        assert arm_call in env["NativeOut"]
        clang_target = "arm64-apple-macos11"
    assert ".double 0.5" in env["NativeOut"]
    assert ".double 2.25" in env["NativeOut"]

    assembly = tmp_path / f"mixed-decimal-{target}.s"
    object_file = tmp_path / f"mixed-decimal-{target}.o"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", clang_target, "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_file.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_forwards_decimal_action_parameter(target):
    source = (
        "Action Sink Value: Decimals;\nReturn 7;\nDone.\n"
        "Action Forward Value: Decimals;\nCall Sink Value;\nReturn 42;\nDone.\n"
        "Call Forward 2.5;\nPrint @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens.count("Decimals") == 2
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "movsd %xmm0, 1024(%rsp)" in env["NativeOut"]
        assert "movsd 0(%rsp), %xmm0" in env["NativeOut"]
        assert "call .Lkuro_fn_0" in env["NativeOut"]
    else:
        assert "str d0, [sp, #1024]" in env["NativeOut"]
        assert "ldr d0, [sp, #0]" in env["NativeOut"]
        assert "bl L_kuro_fn_0" in env["NativeOut"]


def test_kuro_native_codegen_rejects_decimal_return_until_float_returns_supported():
    source = (
        "Action Echo Value: Decimals;\nReturn Value;\nDone.\n"
        "Call Echo 1.25;\nPrint @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target="x86_64-linux")

    assert "Decimals" in tokens
    assert env["NativeFailed"] == 1
    assert env["NativeOut"] == ""


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_compiles_one_integer_action_local(target, tmp_path):
    source = (
        "Action Local A: Integers;\n"
        "N = A + 1;\n"
        "N = N + 1;\n"
        "Return N;\n"
        "Done.\n"
        "Call Local 41;\n"
        "Print @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens == [
        "BC_FUNC_BEGIN", "Local", "BC_PARAM", "A", "Integers", "BC_LOADVAR", "A",
        "BC_CONST", "1", "BC_BINOP", "+", "BC_STORE_LIST", "N", "BC_LOADVAR", "N",
        "BC_CONST", "1", "BC_BINOP", "+", "BC_STORE_LIST", "N", "BC_LOADVAR", "N",
        "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Local", "BC_CONST", "41",
        "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
    ]
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "mov %rdi, 1024(%rsp)\n" in env["NativeOut"]
        assert "mov %rsp, %r15\n" in env["NativeOut"]
        assert "mov %rax, 1024(%r15)\n" in env["NativeOut"]
        assert "mov 1024(%r15), %rax" in env["NativeOut"]
    else:
        assert "str x0, [sp, #1024]\n" in env["NativeOut"]
        assert "mov x19, sp\n" in env["NativeOut"]
        assert "str x0, [x19, #1024]\n" in env["NativeOut"]
        assert "ldr x0, [x19, #1024]" in env["NativeOut"]
        assembly = tmp_path / "action-local-arm64.s"
        object_file = tmp_path / "action-local-arm64.o"
        assembly.write_text(env["NativeOut"], encoding="utf-8")
        subprocess.run(
            ["clang", "-target", "arm64-apple-macos11", "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert object_file.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_compiles_two_integer_action_locals(target, tmp_path):
    source = (
        "Action Mix A: Integers;\n"
        "Left = A + 1;\n"
        "Right = Left + 1;\n"
        "Left = Right + Left;\n"
        "Return Left + Right;\n"
        "Done.\n"
        "Call Mix 40;\n"
        "Print @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens == [
        "BC_FUNC_BEGIN", "Mix", "BC_PARAM", "A", "Integers", "BC_LOADVAR", "A", "BC_CONST", "1",
        "BC_BINOP", "+", "BC_STORE_LIST", "Left", "BC_LOADVAR", "Left", "BC_CONST", "1",
        "BC_BINOP", "+", "BC_STORE_LIST", "Right", "BC_LOADVAR", "Right", "BC_LOADVAR", "Left",
        "BC_BINOP", "+", "BC_STORE_LIST", "Left", "BC_LOADVAR", "Left", "BC_LOADVAR", "Right",
        "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Mix", "BC_CONST", "40",
        "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
    ]
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        for slot in (1024, 1032):
            assert f"mov %rax, {slot}(%r15)\n" in env["NativeOut"]
            assert f"mov {slot}(%r15), %rax" in env["NativeOut"]
    else:
        for slot in (1024, 1032):
            assert f"str x0, [x19, #{slot}]\n" in env["NativeOut"]
            assert f"ldr x0, [x19, #{slot}]" in env["NativeOut"]
        assembly = tmp_path / "two-action-locals-arm64.s"
        object_file = tmp_path / "two-action-locals-arm64.o"
        assembly.write_text(env["NativeOut"], encoding="utf-8")
        subprocess.run(
            ["clang", "-target", "arm64-apple-macos11", "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert object_file.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_shares_nonparameter_action_variables_with_caller(target, tmp_path):
    source = (
        "Action Remember Value: Integers;\n"
        "Saved = Value;\n"
        "Done.\n"
        "Call Remember 9;\n"
        "Print Saved.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert "BC_STORE_LIST" in tokens and "Saved" in tokens
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "mov %rax, 1024(%r15)\n" in env["NativeOut"]
        assert "mov 1024(%rsp), %rax" in env["NativeOut"]
    else:
        assert "str x0, [x19, #1024]\n" in env["NativeOut"]
        assert "ldr x0, [sp, #1024]" in env["NativeOut"]
        assembly = tmp_path / "shared-action-global-arm64.s"
        object_file = tmp_path / "shared-action-global-arm64.o"
        assembly.write_text(env["NativeOut"], encoding="utf-8")
        subprocess.run(
            ["clang", "-target", "arm64-apple-macos11", "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert object_file.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_compiles_action_parameter_writeback(target, tmp_path):
    source = (
        "Action Adjust A: Integers, B: Integers, C: Integers;\n"
        "A = A + 1;\n"
        "B = B + 2;\n"
        "C = C + 3;\n"
        "Return A + B + C;\n"
        "Done.\n"
        "Call Adjust 1, 2, 3;\n"
        "Print @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens == [
        "BC_FUNC_BEGIN", "Adjust", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers",
        "BC_PARAM", "C", "Integers", "BC_LOADVAR", "A", "BC_CONST", "1", "BC_BINOP", "+",
        "BC_STORE_LIST", "A", "BC_LOADVAR", "B", "BC_CONST", "2", "BC_BINOP", "+",
        "BC_STORE_LIST", "B", "BC_LOADVAR", "C", "BC_CONST", "3", "BC_BINOP", "+",
        "BC_STORE_LIST", "C", "BC_LOADVAR", "A", "BC_LOADVAR", "B", "BC_BINOP", "+",
        "BC_LOADVAR", "C", "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN",
        "Adjust", "BC_CONST", "1", "BC_CONST", "2", "BC_CONST", "3", "BC_CALL_END",
        "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
    ]
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        for slot in (1024, 1032, 1040):
            assert f"mov %rax, {slot}(%rsp)\n" in env["NativeOut"]
    else:
        for slot in (1024, 1032, 1040):
            assert f"str x0, [sp, #{slot}]\n" in env["NativeOut"]
        assembly = tmp_path / "action-parameter-writeback-arm64.s"
        object_file = tmp_path / "action-parameter-writeback-arm64.o"
        assembly.write_text(env["NativeOut"], encoding="utf-8")
        subprocess.run(
            ["clang", "-target", "arm64-apple-macos11", "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert object_file.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_updates_action_parameter_and_local_slots(target, tmp_path):
    tokens = [
        "BC_FUNC_BEGIN", "Mutate", "BC_PARAM", "A", "Integers",
        "BC_LOADVAR", "A", "BC_STORE_LIST", "Local", "BC_CONST", "1", "BC_ADD", "Local",
        "BC_CONST", "42", "BC_UPDATE", "A", "BC_LOADVAR", "Local", "BC_LOADVAR", "A",
        "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Mutate", "BC_CONST",
        "41", "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
    ]
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    env = run_codegen(bytecode, target=target)

    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "add 1024(%r15), %rax\n" in env["NativeOut"]
        assert "mov %rax, 1024(%r15)\n" in env["NativeOut"]
        assert "mov %rax, 1024(%rsp)\n" in env["NativeOut"]
    else:
        assert "ldr x1, [x19, #1024]\n    add x0, x1, x0\n" in env["NativeOut"]
        assert "str x0, [x19, #1024]\n" in env["NativeOut"]
        assert "str x0, [sp, #1024]\n" in env["NativeOut"]
        assembly = tmp_path / "action-update-add-arm64.s"
        object_file = tmp_path / "action-update-add-arm64.o"
        assembly.write_text(env["NativeOut"], encoding="utf-8")
        subprocess.run(
            ["clang", "-target", "arm64-apple-macos11", "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert object_file.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
@pytest.mark.parametrize("opcode", ["BC_ADD", "BC_UPDATE"])
def test_kuro_native_codegen_initializes_action_local_from_update_or_add(opcode, target, tmp_path):
    tokens = [
        "BC_FUNC_BEGIN", "Seed", "BC_CONST", "41", opcode, "N", "BC_LOADVAR", "N", "BC_RETURN",
        "BC_FUNC_END", "BC_CALL_BEGIN", "Seed", "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR",
        "_", "BC_PRINT",
    ]
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    env = run_codegen(bytecode, target=target)

    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "movq $0, 1024(%rsp)\n" in env["NativeOut"]
        assert "mov %rax, 1024(%r15)\n" in env["NativeOut"]
        if opcode == "BC_ADD":
            assert "add 1024(%r15), %rax\n" in env["NativeOut"]
    else:
        assert "str xzr, [sp, #1024]\n" in env["NativeOut"]
        assert "str x0, [x19, #1024]\n" in env["NativeOut"]
        if opcode == "BC_ADD":
            assert "ldr x1, [x19, #1024]\n" in env["NativeOut"]
        assembly = tmp_path / f"action-{opcode.lower()}-local-arm64.s"
        object_file = tmp_path / f"action-{opcode.lower()}-local-arm64.o"
        assembly.write_text(env["NativeOut"], encoding="utf-8")
        subprocess.run(
            ["clang", "-target", "arm64-apple-macos11", "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert object_file.stat().st_size > 0


def test_kuro_native_codegen_rejects_undeclared_action_local_read():
    tokens = [
        "BC_FUNC_BEGIN", "Local", "BC_LOADVAR", "N", "BC_RETURN", "BC_FUNC_END",
        "BC_CALL_BEGIN", "Local", "BC_CALL_END", "BC_PRINT",
    ]
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    env = run_codegen(bytecode, target="x86_64-linux")

    assert env["NativeFailed"] == 1


@pytest.mark.parametrize("global_count, expected_failed", [(64, 0), (65, 1)])
def test_kuro_native_codegen_bounds_globals_before_reserved_loop_storage(global_count, expected_failed):
    tokens = []
    for index in range(global_count):
        tokens.extend(["BC_CONST", str(index), "BC_STORE_LIST", f"G{index}"])
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    env = run_codegen(bytecode, target="x86_64-linux")

    assert env["NativeFailed"] == expected_failed
    if global_count == 64:
        assert "movq $0, 1528(%rsp)\n" in env["NativeOut"]
        assert "mov %rax, 1528(%rsp)\n" in env["NativeOut"]
    else:
        assert env["NativeOut"] == ""


@pytest.mark.parametrize(
    "bytecode",
    [
        '"BC_FUNC_BEGIN", "Inc", "BC_PARAM", "N", "Integers", "BC_LOADVAR", "N", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Inc", "BC_CALL_END", "BC_PRINT"',
        '"BC_FUNC_BEGIN", "FortyTwo", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "FortyTwo", "BC_CONST", "1", "BC_CALL_END", "BC_PRINT"',
        '"BC_FUNC_BEGIN", "Add", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers", "BC_PARAM", "C", "Integers", "BC_PARAM", "D", "Integers", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Add", "BC_CONST", "4", "BC_CONST", "2", "BC_CONST", "1", "BC_CONST", "0", "BC_CALL_END", "BC_PRINT"',
        '"BC_FUNC_BEGIN", "Add", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers", "BC_PARAM", "C", "Integers", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Add", "BC_CONST", "4", "BC_CONST", "2", "BC_CALL_END", "BC_PRINT"',
        '"BC_FUNC_BEGIN", "Add", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Add", "BC_CONST", "4", "BC_CALL_END", "BC_PRINT"',
        '"BC_FUNC_BEGIN", "Add", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers", "BC_LOADVAR", "Missing", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Add", "BC_CONST", "4", "BC_CONST", "2", "BC_CALL_END", "BC_PRINT"',
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


def test_native_codegen_source_emits_with_macos_arm64_backend():
    from compiler.native import emit_macos_arm64
    from compiler.pipeline import compile_source
    from compiler.self_host import native_codegen_source

    result = compile_source(native_codegen_source("aarch64-macos"))
    assert result.ok, result.diags.render_all()
    assembly = emit_macos_arm64(result.ir)

    assert assembly.startswith(".section __TEXT,__text")
    assert "_kuro_print_int:" in assembly


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
            (
                [
                    "BC_FUNC_BEGIN", "FortyTwo", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END",
                    "BC_FUNC_BEGIN", "Combine", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers",
                    "BC_LOADVAR", "A", "BC_CONST", "10", "BC_BINOP", "*", "BC_LOADVAR", "B",
                    "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Combine",
                    "BC_CONST", "4", "BC_CONST", "2", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "42\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Combine", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers",
                    "BC_PARAM", "C", "Integers", "BC_LOADVAR", "A", "BC_CONST", "100", "BC_BINOP", "*",
                    "BC_LOADVAR", "B", "BC_CONST", "10", "BC_BINOP", "*", "BC_BINOP", "+",
                    "BC_LOADVAR", "C", "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Combine", "BC_CONST", "1", "BC_CONST", "2", "BC_CONST", "3",
                    "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "123\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Adjust", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers",
                    "BC_PARAM", "C", "Integers", "BC_LOADVAR", "A", "BC_CONST", "1", "BC_BINOP", "+",
                    "BC_STORE_LIST", "A", "BC_LOADVAR", "B", "BC_CONST", "2", "BC_BINOP", "+",
                    "BC_STORE_LIST", "B", "BC_LOADVAR", "C", "BC_CONST", "3", "BC_BINOP", "+",
                    "BC_STORE_LIST", "C", "BC_LOADVAR", "A", "BC_LOADVAR", "B", "BC_BINOP", "+",
                    "BC_LOADVAR", "C", "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN",
                    "Adjust", "BC_CONST", "1", "BC_CONST", "2", "BC_CONST", "3", "BC_CALL_END",
                    "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "12\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "First", "BC_CONST", "40", "BC_STORE_LIST", "N", "BC_LOADVAR", "N",
                    "BC_RETURN", "BC_FUNC_END",
                    "BC_FUNC_BEGIN", "Second", "BC_CONST", "2", "BC_STORE_LIST", "N", "BC_LOADVAR", "N",
                    "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "First", "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                    "BC_CALL_BEGIN", "Second", "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "40\n2\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Mix", "BC_PARAM", "A", "Integers", "BC_LOADVAR", "A", "BC_CONST", "1",
                    "BC_BINOP", "+", "BC_STORE_LIST", "Left", "BC_LOADVAR", "Left", "BC_CONST", "1",
                    "BC_BINOP", "+", "BC_STORE_LIST", "Right", "BC_LOADVAR", "Left", "BC_LOADVAR", "Right",
                    "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Mix", "BC_CONST", "40",
                    "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "83\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Increase", "BC_PARAM", "A", "Integers", "BC_LOADVAR", "A",
                    "BC_STORE_LIST", "Local", "BC_CONST", "1", "BC_ADD", "Local", "BC_LOADVAR", "Local",
                    "BC_RETURN", "BC_FUNC_END", "BC_FUNC_BEGIN", "Replace", "BC_PARAM", "B", "Integers",
                    "BC_CONST", "73", "BC_UPDATE", "B", "BC_LOADVAR", "B", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Increase", "BC_CONST", "41", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT", "BC_CALL_BEGIN", "Replace", "BC_CONST", "41",
                    "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "42\n73\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "SeedAdd", "BC_CONST", "41", "BC_ADD", "Count", "BC_LOADVAR", "Count",
                    "BC_RETURN", "BC_FUNC_END", "BC_FUNC_BEGIN", "SeedUpdate", "BC_CONST", "73", "BC_UPDATE",
                    "Answer", "BC_LOADVAR", "Answer", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "SeedAdd",
                    "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT", "BC_CALL_BEGIN",
                    "SeedUpdate", "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "41\n73\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Remember", "BC_PARAM", "Value", "Integers",
                    "BC_LOADVAR", "Value", "BC_STORE_LIST", "Saved", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Remember", "BC_CONST", "9", "BC_CALL_END",
                    "BC_STORE_LIST", "_", "BC_LOADVAR", "Saved", "BC_PRINT",
                ],
                "9\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Seed", "BC_CONST", "40", "BC_STORE_LIST", "Count",
                    "BC_LOADVAR", "Count", "BC_RETURN", "BC_FUNC_END",
                    "BC_FUNC_BEGIN", "Increment", "BC_CONST", "1", "BC_ADD", "Count",
                    "BC_LOADVAR", "Count", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Seed", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                    "BC_CALL_BEGIN", "Increment", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                    "BC_CALL_BEGIN", "Increment", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "40\n41\n42\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Seed", "BC_CONST", "100", "BC_STORE_LIST", "A",
                    "BC_LOADVAR", "A", "BC_RETURN", "BC_FUNC_END",
                    "BC_FUNC_BEGIN", "Change", "BC_PARAM", "A", "Integers",
                    "BC_LOADVAR", "A", "BC_CONST", "1", "BC_BINOP", "+",
                    "BC_STORE_LIST", "A", "BC_LOADVAR", "A", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Seed", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                    "BC_CALL_BEGIN", "Change", "BC_CONST", "5", "BC_CALL_END",
                    "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                    "BC_LOADVAR", "A", "BC_PRINT",
                ],
                "100\n6\n100\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "EchoPair", "BC_PARAM", "Count", "Integers",
                    "BC_PARAM", "Word", "Text", "BC_LOADVAR", "Word", "BC_PRINT",
                    "BC_LOADVAR", "Count", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "EchoPair", "BC_CONST", "7", "BC_CONST_TEXT", "hello",
                    "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "hello\n7\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "EchoPair", "BC_PARAM", "Word", "Text",
                    "BC_PARAM", "Count", "Integers", "BC_LOADVAR", "Word", "BC_PRINT",
                    "BC_LOADVAR", "Count", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "EchoPair", "BC_CONST_TEXT", "world", "BC_CONST", "9",
                    "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "world\n9\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "EchoTriple", "BC_PARAM", "First", "Integers",
                    "BC_PARAM", "Count", "Integers", "BC_PARAM", "Last", "Text",
                    "BC_LOADVAR", "Last", "BC_PRINT", "BC_LOADVAR", "First", "BC_LOADVAR",
                    "Count", "BC_BINOP", "+", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "EchoTriple", "BC_CONST", "2", "BC_CONST", "3",
                    "BC_CONST_TEXT", "tail", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "tail\n5\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Select", "BC_PARAM", "First", "Decimals",
                    "BC_PARAM", "Middle", "Integers", "BC_PARAM", "Last", "Decimals",
                    "BC_LOADVAR", "Middle", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Select", "BC_CONST", "0.5", "BC_CONST", "42",
                    "BC_CONST", "2.25", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "42\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Sink", "BC_PARAM", "Value", "Decimals",
                    "BC_CONST", "7", "BC_RETURN", "BC_FUNC_END",
                    "BC_FUNC_BEGIN", "Forward", "BC_PARAM", "Value", "Decimals",
                    "BC_CALL_BEGIN", "Sink", "BC_LOADVAR", "Value", "BC_CALL_END",
                    "BC_STORE_LIST", "_", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Forward", "BC_CONST", "2.5", "BC_CALL_END",
                    "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "42\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Echo", "BC_PARAM", "Message", "Text",
                    "BC_LOADVAR", "Message", "BC_PRINT", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Echo", "BC_CONST_TEXT", r'quoted: "hi" \\end',
                    "BC_CALL_END", "BC_STORE_LIST", "_",
                ],
                'quoted: "hi" \\end\n',
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


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
@pytest.mark.parametrize(
    ("argument", "expected"),
    [(1, "11\n"), (7, "12\n"), (15, "13\n"), (25, "14\n")],
)
def test_kuro_owned_x86_linux_codegen_runs_every_nested_action_return_path(
    tmp_path, argument, expected, x86_linux_codegen
):
    generated = subprocess.run(
        [str(x86_linux_codegen)],
        input="kuro.bytecode/1\n" + "\n".join(nested_choice_program(argument)) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    executable = tmp_path / "nested-action-linux"
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


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
@pytest.mark.parametrize(
    "tokens",
    [
        [
            "BC_FUNC_BEGIN", "Show", "BC_CONST", "42", "BC_PRINT", "BC_FUNC_END",
            "BC_CALL_BEGIN", "Show", "BC_CALL_END", "BC_STORE_LIST", "_",
            "BC_LOADVAR", "_", "BC_PRINT",
        ],
        [
            "BC_FUNC_BEGIN", "Echo", "BC_PARAM", "N", "Integers", "BC_LOADVAR",
            "N", "BC_PRINT", "BC_FUNC_END", "BC_CALL_BEGIN", "Echo", "BC_CONST",
            "42", "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
        ],
    ],
)
def test_kuro_owned_x86_linux_codegen_runs_zero_return_integer_actions(
    tmp_path, tokens, x86_linux_codegen
):
    generated = subprocess.run(
        [str(x86_linux_codegen)],
        input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    executable = tmp_path / "zero-return-action-linux"
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
    assert result.stdout == "42\n0\n"
    assert result.stderr == ""


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
def test_kuro_owned_x86_linux_codegen_runs_action_control_flow_without_label_collisions(
    tmp_path, x86_linux_codegen
):
    tokens, env = compile_program_to_codegen(action_control_flow_program(), target="x86_64-linux")
    assert env["NativeFailed"] == 0

    generated = subprocess.run(
        [str(x86_linux_codegen)],
        input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    labels = re.findall(
        r"^(L_kuro_(?:else|endif|repeat|endrepeat|while|endwhile)_\d+):$",
        generated.stdout,
        re.MULTILINE,
    )
    assert len(labels) == 16
    assert len(labels) == len(set(labels))

    executable = tmp_path / "action-control-flow-linux"
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
    assert result.stdout == "3\n3\n3\n1\n"
    assert result.stderr == ""


def test_native_kuro_codegen_rejects_unknown_output_target(tmp_path):
    from compiler.self_host import SelfHostError, build_native_codegen

    with pytest.raises(SelfHostError, match="unsupported code-generation output target"):
        build_native_codegen(tmp_path / "bad", output_target="x86_64-windows")
