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


def recursive_numeric_action_program():
    return (
        "Action CountDownInteger Value: Integers;\n"
        "If Value is equal to 0;\nReturn 1;\nElse;\n"
        "Value = Value - 1;\nCall CountDownInteger Value;\nReturn 1 + @_;\n"
        "Done.\nDone.\n"
        "Action ScaleToBase Value: Integers;\n"
        "If Value is equal to 0;\nReturn 1.25;\nElse;\n"
        "Value = Value - 1;\nCall ScaleToBase Value;\nReturn 1.5 * @_;\n"
        "Done.\nDone.\n"
        "Action VerifyDecimal Value: Decimals;\n"
        "If Value is equal to 1.875;\nReturn 42;\nElse;\nReturn 0;\n"
        "Done.\nDone.\n"
        "Call CountDownInteger 2;\nPrint @_.\n"
        "Call ScaleToBase 1;\nCall VerifyDecimal @_;\nPrint @_.\n"
    )


def four_parameter_action_program():
    return (
        "Action IntegerQuad First: Integers, Second: Integers, Third: Integers, Fourth: Integers;\n"
        "Fourth = Fourth + 1;\nReturn Fourth;\nDone.\n"
        "Action DecimalQuad First: Decimals, Second: Decimals, Third: Decimals, Fourth: Decimals;\n"
        "Return Fourth;\nDone.\n"
        "Action MixedQuad First: Integers, Fraction: Decimals, Word: Text, Last: Integers;\n"
        "Print Word.\nReturn First + Last;\nDone.\n"
        "Action TextQuad First: Integers, Second: Integers, Third: Integers, Message: Text;\n"
        "Print Message.\nReturn Third;\nDone.\n"
        "Fourth = 100;\n"
        "Call IntegerQuad 1, 2, 3, 4;\nPrint @_.\n"
        "Print Fourth.\n"
        "Action CheckDecimal Value: Decimals;\n"
        "If Value is equal to 2.0;\nReturn 1;\nElse;\nReturn 0;\nDone.\nDone.\n"
        "Call DecimalQuad 0.5, 1.0, 1.5, 2.0;\n"
        "Call CheckDecimal @_;\nPrint @_.\n"
        "Call DecimalQuad 0.5, 1.0, 1.5, 2;\n"
        "Call CheckDecimal @_;\nPrint @_.\n"
        'Call MixedQuad 2, 0.5, "mixed", 3;\nPrint @_.\n'
        'Call TextQuad 7, 8, 9, "tail-text";\nPrint @_.\n'
    )


def stack_spill_action_program():
    integers = [f"I{index}" for index in range(1, 10)]
    decimals = [f"D{index}" for index in range(1, 10)]
    texts = [f"Text{index}" for index in range(1, 10)]
    integer_parameters = ", ".join(f"{name}: Integers" for name in integers)
    decimal_parameters = ", ".join(f"{name}: Decimals" for name in decimals)
    text_parameters = ", ".join(f"{name}: Text" for name in texts)
    integer_values = ", ".join(str(index) for index in range(1, 10))
    decimal_values = ", ".join(f"{index}.0" for index in range(1, 10))
    decimal_spill_values = ", ".join([*(f"{index}.0" for index in range(1, 9)), "9"])
    text_values = ", ".join(f'"text{index}"' for index in range(1, 10))
    return (
        f"Action IntegerSpill {integer_parameters};\nReturn I9;\nDone.\n"
        f"Action DecimalSpill {decimal_parameters};\nReturn D9;\nDone.\n"
        f"Action MixedSpill {integer_parameters}, {decimal_parameters};\nReturn D9;\nDone.\n"
        f"Action TextSpill {text_parameters};\nPrint Text9.\nReturn 1;\nDone.\n"
        "Action CheckDecimal Value: Decimals;\n"
        "If Value is equal to 9.0;\nReturn 1;\nElse;\nReturn 0;\nDone.\nDone.\n"
        f"Call IntegerSpill {integer_values};\nPrint @_.\n"
        f"Call DecimalSpill {decimal_spill_values};\nCall CheckDecimal @_;\nPrint @_.\n"
        f"Call MixedSpill {integer_values}, {decimal_values};\nCall CheckDecimal @_;\nPrint @_.\n"
        f"Call TextSpill {text_values};\nPrint @_.\n"
    )


def nan_decimal_comparison_program():
    comparisons = (
        ("Equal", "equal to"),
        ("NotEqual", "not equal to"),
        ("Less", "less than"),
        ("LessEqual", "less than or equal to"),
        ("Greater", "greater than"),
        ("GreaterEqual", "greater than or equal to"),
    )
    actions = "".join(
        f"Action Check{name} Value: Decimals;\n"
        f"If Value is {operator} Value;\nReturn 1;\nElse;\nReturn 0;\nDone.\nDone.\n"
        for name, operator in comparisons
    )
    calls = "".join(
        "Call OverflowCount 1024;\nCall MakeNaN @_;\n"
        f"Call Check{name} @_;\nPrint @_.\n"
        for name, _ in comparisons
    )
    return (
        "Action OverflowCount Count: Integers;\n"
        "If Count is equal to 0;\nReturn 1.0;\nElse;\n"
        "Count = Count - 1;\nCall OverflowCount Count;\nReturn 2.0 * @_;\n"
        "Done.\nDone.\n"
        "Action MakeNaN Value: Decimals;\nReturn Value - Value;\nDone.\n"
        + actions
        + calls
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


def _bytecode_for_token_limit(if_count: int, print_count: int) -> list[str]:
    return (
        ["BC_CONST", "1", "BC_IF_BEGIN", "BC_IF_END"] * if_count
        + ["BC_CONST", "1", "BC_PRINT"] * print_count
    )


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


def test_kuro_native_codegen_enforces_exact_4096_token_boundary():
    accepted_tokens = _bytecode_for_token_limit(if_count=1021, print_count=4)
    rejected_tokens = _bytecode_for_token_limit(if_count=1022, print_count=3)
    assert len(accepted_tokens) == 4096
    assert len(rejected_tokens) == 4097

    accepted_bytecode = ", ".join(json.dumps(token) for token in accepted_tokens)
    accepted = run_codegen(accepted_bytecode)
    assert accepted["NativeFailed"] == 0
    assert "L_kuro_else_1020:" in accepted["NativeOut"]

    rejected_bytecode = ", ".join(json.dumps(token) for token in rejected_tokens)
    rejected = run_codegen(rejected_bytecode)
    assert rejected["NativeFailed"] == 1
    assert rejected["NativeOut"] == ""


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


@pytest.mark.parametrize(
    "target", ["x86_64-linux", "aarch64-macos"], ids=["linux-x86-64", "apple-arm64"]
)
def test_kuro_native_codegen_supports_four_action_parameters(target, tmp_path):
    tokens, env = compile_program_to_codegen(four_parameter_action_program(), target=target)

    assert "BC_PARAM" in tokens
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        expected = (
            "mov %rcx, 1048(%rsp)",
            "mov 24(%rsp), %rcx",
            "movsd %xmm3, 1048(%rsp)",
            "movsd 24(%rsp), %xmm3",
            "cvtsi2sd %rax, %xmm3",
            "mov %rsi, 1040(%rsp)",
        )
        clang_target = "x86_64-unknown-linux-gnu"
    else:
        expected = (
            "str x3, [sp, #1048]",
            "ldr x3, [sp, #24]",
            "str d3, [sp, #1048]",
            "ldr d3, [sp, #24]",
            "scvtf d3, x9",
            "str x1, [sp, #1040]",
        )
        clang_target = "arm64-apple-macos11"
    for fragment in expected:
        assert fragment in env["NativeOut"]

    assembly = tmp_path / f"four-parameters-{target}.s"
    object_file = tmp_path / f"four-parameters-{target}.o"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", clang_target, "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_file.stat().st_size > 0


@pytest.mark.parametrize(
    "target", ["x86_64-linux", "aarch64-macos"], ids=["linux-x86-64", "apple-arm64"]
)
def test_kuro_native_codegen_marshals_abi_stack_spills(target, tmp_path):
    tokens, env = compile_program_to_codegen(stack_spill_action_program(), target=target)

    assert tokens.count("BC_PARAM") == 46
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        expected = (
            "mov 2064(%rsp), %rax",
            "mov 2080(%rsp), %rax",
            "movsd 2088(%rsp), %xmm15",
            "movsd %xmm15, 24(%rsp)",
            "cvtsi2sd %rax, %xmm15",
            "sub $32, %rsp",
            "add $32, %rsp",
        )
        clang_target = "x86_64-unknown-linux-gnu"
    else:
        expected = (
            "ldr x9, [sp, #2064]",
            "ldr d31, [sp, #2072]",
            "str d31, [sp, #8]",
            "scvtf d31, x9",
            "sub sp, sp, #16",
            "add sp, sp, #16",
        )
        clang_target = "arm64-apple-macos11"
    for fragment in expected:
        assert fragment in env["NativeOut"]

    assembly = tmp_path / f"stack-spills-{target}.s"
    object_file = tmp_path / f"stack-spills-{target}.o"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", clang_target, "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_file.stat().st_size > 0


@pytest.mark.parametrize(
    "target", ["x86_64-linux", "aarch64-macos"], ids=["linux-x86-64", "apple-arm64"]
)
def test_kuro_native_codegen_rejects_more_than_eighteen_action_parameters(target):
    names = [f"P{index}" for index in range(1, 20)]
    parameters = ", ".join(f"{name}: Integers" for name in names)
    values = ", ".join(str(index) for index in range(1, 20))
    source = f"Action Nineteen {parameters};\nReturn P1;\nDone.\nCall Nineteen {values};\nPrint @_.\n"
    _, env = compile_program_to_codegen(source, target=target)

    assert env["NativeFailed"] == 1


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


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_returns_decimal_action_values_in_float_registers(target, tmp_path):
    source = (
        "Action Echo Value: Decimals;\nReturn Value;\nDone.\n"
        "Action Consume Value: Decimals;\nReturn 42;\nDone.\n"
        "Call Echo 1.25;\nCall Consume @_;\nPrint @_.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens.count("Decimals") == 2
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "movsd %xmm0, 1024(%rsp)" in env["NativeOut"]
        assert "movsd 0(%rsp), %xmm0" in env["NativeOut"]
        assert "movsd %xmm0, 0(%rsp)" in env["NativeOut"]
        assert "call .Lkuro_fn_0" in env["NativeOut"]
        clang_target = "x86_64-unknown-linux-gnu"
    else:
        assert "str d0, [sp, #1024]" in env["NativeOut"]
        assert "ldr d0, [sp, #0]" in env["NativeOut"]
        assert "str d0, [sp, #0]" in env["NativeOut"]
        assert "bl L_kuro_fn_0" in env["NativeOut"]
        clang_target = "arm64-apple-macos11"
    assembly = tmp_path / f"decimal-return-{target}.s"
    object_file = tmp_path / f"decimal-return-{target}.o"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", clang_target, "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_file.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_returns_decimal_across_if_branches(target):
    source = (
        "Action Choose Flag: Integers;\n"
        "If Flag is equal to 1;\nReturn 1.25;\nElse;\nReturn 2.0;\nDone.\nDone.\n"
        "Action Consume Value: Decimals;\nReturn 42;\nDone.\n"
        "Call Choose 0;\nCall Consume @_;\nPrint @_.\n"
    )
    _, env = compile_program_to_codegen(source, target=target)

    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "movsd 0(%rsp), %xmm0" in env["NativeOut"]
        assert ".double 1.25" in env["NativeOut"]
        assert ".double 2.0" in env["NativeOut"]
    else:
        assert "ldr d0, [sp, #0]" in env["NativeOut"]
        assert ".double 1.25" in env["NativeOut"]
        assert ".double 2.0" in env["NativeOut"]


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_lowers_mixed_decimal_arithmetic_and_comparisons(target, tmp_path):
    source = (
        "Action Calculate Left: Decimals, Right: Integers;\n"
        "Return (Left + Right) - (Left * Right) / Right;\nDone.\n"
        "Action Check Value: Decimals;\n"
        "If Value is equal to 2.0;\nReturn 1;\nElse;\nReturn 0;\nDone.\nDone.\n"
        "Call Calculate 1.5, 2;\nCall Check @_;\nPrint @_.\n"
    )
    _, env = compile_program_to_codegen(source, target=target)

    assert env["NativeFailed"] == 0
    assembly = env["NativeOut"]
    if target == "x86_64-linux":
        for instruction in ("addsd %xmm1, %xmm0", "subsd %xmm1, %xmm0", "mulsd %xmm1, %xmm0", "divsd %xmm1, %xmm0"):
            assert instruction in assembly
        assert "cvtsi2sd %rcx, %xmm1" in assembly
        assert "ucomisd %xmm1, %xmm0" in assembly
        assert "sete %al" in assembly
        clang_target = "x86_64-unknown-linux-gnu"
    else:
        for instruction in ("fadd d0, d0, d1", "fsub d0, d0, d1", "fmul d0, d0, d1", "fdiv d0, d0, d1"):
            assert instruction in assembly
        assert "scvtf d1, x1" in assembly
        assert "fcmp d0, d1" in assembly
        assert "cset w0, eq" in assembly
        clang_target = "arm64-apple-macos11"

    asm_path = tmp_path / f"decimal-ops-{target}.s"
    object_path = tmp_path / f"decimal-ops-{target}.o"
    asm_path.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["clang", "-target", clang_target, "-c", "-x", "assembler", str(asm_path), "-o", str(object_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_path.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_uses_ieee_ordered_decimal_comparison_conditions(target, tmp_path):
    _, env = compile_program_to_codegen(nan_decimal_comparison_program(), target=target)
    assert env["NativeFailed"] == 0
    assembly = env["NativeOut"]
    if target == "x86_64-linux":
        for instruction in ("setnp %cl", "setp %cl", "andb %cl, %al", "orb %cl, %al", "setbe %al"):
            assert instruction in assembly
        clang_target = "x86_64-unknown-linux-gnu"
    else:
        assert "cset w0, mi" in assembly
        assert "cset w0, ls" in assembly
        clang_target = "arm64-apple-macos11"

    asm_path = tmp_path / f"decimal-nan-comparisons-{target}.s"
    object_path = tmp_path / f"decimal-nan-comparisons-{target}.o"
    asm_path.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["clang", "-target", clang_target, "-c", "-x", "assembler", str(asm_path), "-o", str(object_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_path.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_infers_recursive_integer_and_decimal_return_kinds(target):
    tokens, env = compile_program_to_codegen(recursive_numeric_action_program(), target=target)

    assert tokens.count("BC_FUNC_BEGIN") == 3
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "call .Lkuro_fn_0" in env["NativeOut"]
        assert "call .Lkuro_fn_1" in env["NativeOut"]
        assert "mulsd %xmm1, %xmm0" in env["NativeOut"]
    else:
        assert "bl L_kuro_fn_0" in env["NativeOut"]
        assert "bl L_kuro_fn_1" in env["NativeOut"]
        assert "fmul d0, d0, d1" in env["NativeOut"]


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_rejects_recursive_only_unknown_return_kind(target):
    source = (
        "Action Loop Value: Integers;\n"
        "Call Loop Value;\nReturn 1 + @_;\nDone.\n"
        "Call Loop 0;\nPrint @_.\n"
    )
    _, env = compile_program_to_codegen(source, target=target)

    assert env["NativeFailed"] == 1
    assert env["NativeOut"] == ""


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_rejects_mixed_integer_and_decimal_return_kinds(target):
    tokens = [
        "BC_FUNC_BEGIN", "Choose", "BC_PARAM", "Flag", "Integers",
        "BC_LOADVAR", "Flag", "BC_CONST", "1", "BC_CMP", "eq", "BC_IF_BEGIN",
        "BC_CONST", "1.25", "BC_RETURN", "BC_ELSE_BEGIN", "BC_CONST", "2",
        "BC_RETURN", "BC_IF_END", "BC_FUNC_END",
        "BC_CONST", "0", "BC_PRINT",
    ]
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    env = run_codegen(bytecode, target=target)

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


def decimal_parameter_assignment_bytecode():
    return [
        "BC_FUNC_BEGIN", "Adjust", "BC_PARAM", "Balance", "Decimals",
        "BC_LOADVAR", "Balance", "BC_CONST", "2.5", "BC_BINOP", "+", "BC_STORE_LIST", "Balance",
        "BC_LOADVAR", "Balance", "BC_RETURN", "BC_FUNC_END",
        "BC_CALL_BEGIN", "Adjust", "BC_CONST", "1.25", "BC_CALL_END",
        "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_CONST", "3.75", "BC_CMP", "eq", "BC_PRINT",
    ]


def decimal_parameter_mutation_bytecode(opcode, operand, expected):
    return [
        "BC_FUNC_BEGIN", "MutateDecimal", "BC_PARAM", "Balance", "Decimals",
        "BC_CONST", operand, opcode, "Balance", "BC_LOADVAR", "Balance", "BC_RETURN", "BC_FUNC_END",
        "BC_CALL_BEGIN", "MutateDecimal", "BC_CONST", "1.25", "BC_CALL_END",
        "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_CONST", expected, "BC_CMP", "eq", "BC_PRINT",
    ]


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_assigns_decimal_action_parameter(target, tmp_path):
    source = (
        "Action Adjust Balance: Decimals;\n"
        "Balance = Balance + 2.5;\n"
        "Return Balance;\n"
        "Done.\n"
        "Call Adjust 1.25;\n"
        "If @_ is equal to 3.75;\nPrint 1.\nElse;\nPrint 0.\nDone.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert "BC_STORE_LIST" in tokens
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "addsd" in env["NativeOut"]
        assert "mov %rax, 1024(%rsp)\n" in env["NativeOut"]
        clang_target = "x86_64-unknown-linux-gnu"
    else:
        assert "fadd d0, d0, d1" in env["NativeOut"]
        assert "str x0, [sp, #1024]\n" in env["NativeOut"]
        clang_target = "arm64-apple-macos11"
    assembly = tmp_path / f"decimal-action-assignment-{target}.s"
    object_file = tmp_path / f"decimal-action-assignment-{target}.o"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", clang_target, "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_file.stat().st_size > 0


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_kuro_native_codegen_compiles_decimal_action_parameter_add_and_update(target, tmp_path):
    source = (
        "Action AddBalance Balance: Decimals;\n"
        "Add 2 to Balance;\n"
        "Return Balance;\n"
        "Done.\n"
        "Action AddDecimalBalance Balance: Decimals;\n"
        "Add 2.5 to Balance;\n"
        "Return Balance;\n"
        "Done.\n"
        "Action SetBalance Balance: Decimals;\n"
        "Update Balance to 6.25;\n"
        "Return Balance;\n"
        "Done.\n"
        "Call AddBalance 1.25;\n"
        "If @_ is equal to 3.25;\nPrint 1.\nElse;\nPrint 0.\nDone.\n"
        "Call AddDecimalBalance 1.25;\n"
        "If @_ is equal to 3.75;\nPrint 1.\nElse;\nPrint 0.\nDone.\n"
        "Call SetBalance 1.25;\n"
        "If @_ is equal to 6.25;\nPrint 1.\nElse;\nPrint 0.\nDone.\n"
    )
    tokens, env = compile_program_to_codegen(source, target=target)

    assert tokens.count("BC_ADD") == 2
    assert tokens.count("BC_UPDATE") == 1
    assert env["NativeFailed"] == 0
    if target == "x86_64-linux":
        assert "cvtsi2sd" in env["NativeOut"]
        assert "addsd" in env["NativeOut"]
        clang_target = "x86_64-unknown-linux-gnu"
    else:
        assert "scvtf d0, x0" in env["NativeOut"]
        assert "fadd d0, d1, d0" in env["NativeOut"]
        clang_target = "arm64-apple-macos11"
    assembly = tmp_path / f"decimal-action-add-update-{target}.s"
    object_file = tmp_path / f"decimal-action-add-update-{target}.o"
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
    ("parameter_type", "literal"),
    [("Decimals", "1"), ("Integers", "1.5"), ("Text", "1.5")],
)
def test_kuro_native_codegen_rejects_mismatched_decimal_action_parameter_store(
    target, parameter_type, literal
):
    tokens = [
        "BC_FUNC_BEGIN", "Mismatch", "BC_PARAM", "Value", parameter_type,
        "BC_CONST", literal, "BC_STORE_LIST", "Value", "BC_LOADVAR", "Value", "BC_RETURN", "BC_FUNC_END",
    ]
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    env = run_codegen(bytecode, target=target)

    assert env["NativeFailed"] == 1


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
@pytest.mark.parametrize(
    ("opcode", "parameter_type", "literal"),
    [
        ("BC_UPDATE", "Decimals", "1"),
        ("BC_ADD", "Integers", "1.5"),
        ("BC_UPDATE", "Integers", "1.5"),
    ],
)
def test_kuro_native_codegen_rejects_mismatched_decimal_action_parameter_mutation(
    target, opcode, parameter_type, literal
):
    tokens = [
        "BC_FUNC_BEGIN", "Mismatch", "BC_PARAM", "Balance", parameter_type,
        "BC_CONST", literal, opcode, "Balance", "BC_LOADVAR", "Balance", "BC_RETURN", "BC_FUNC_END",
    ]
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    env = run_codegen(bytecode, target=target)

    assert env["NativeFailed"] == 1


@pytest.mark.parametrize(
    ("target", "triple", "text_section", "data_section"),
    [
        ("x86_64-linux", "x86_64-unknown-linux-gnu", ".section .text", ".section .rodata"),
        ("x86_64-macos", "x86_64-apple-macos", ".section __TEXT,__text", ".section __TEXT,__const"),
        ("aarch64-macos", "arm64-apple-macos11", ".section __TEXT,__text", ".section __TEXT,__const"),
    ],
)
def test_kuro_native_codegen_emits_freestanding_decimal_printing(target, triple, text_section, data_section, tmp_path):
    source = (
        "Action Echo Value: Decimals;\nPrint Value.\nReturn Value;\nDone.\n"
        "Call Echo 2.5;\nPrint @_ + 0.0.\n"
    )
    _, env = compile_program_to_codegen(source, target=target)

    assert env["NativeFailed"] == 0
    call = "bl" if target == "aarch64-macos" else "call"
    assert f"{call} _kuro_print_float" in env["NativeOut"]
    assert env["NativeOut"].count("_kuro_print_float:") == 1
    assert text_section in env["NativeOut"]
    assert data_section in env["NativeOut"]
    if target == "aarch64-macos":
        assert "bl _kuro_decimal_format" in env["NativeOut"]
        assert "_printf" not in env["NativeOut"]
        assert "_malloc" not in env["NativeOut"]
    else:
        assert ".Lkuro_float_pow10_ext:" in env["NativeOut"]
    assembly = tmp_path / f"decimal-print-{target}.s"
    object_file = tmp_path / f"decimal-print-{target}.o"
    assembly.write_text(env["NativeOut"], encoding="utf-8")
    subprocess.run(
        ["clang", "-target", triple, "-c", "-x", "assembler", str(assembly), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_file.stat().st_size > 0


def test_kuro_native_codegen_uses_arm64_decimal_printer_for_computed_values():
    _, env = compile_program_to_codegen("Print 1.25 + 0.0.\n", target="aarch64-macos")

    assert env["NativeFailed"] == 0
    assert "bl _kuro_print_float" in env["NativeOut"]
    assert "mov x16, #4\n    svc #0x80" in env["NativeOut"]


def decimal_printing_bytecode():
    return [
        "BC_FUNC_BEGIN", "Echo", "BC_PARAM", "Value", "Decimals",
        "BC_LOADVAR", "Value", "BC_PRINT", "BC_LOADVAR", "Value", "BC_RETURN", "BC_FUNC_END",
        "BC_CALL_BEGIN", "Echo", "BC_CONST", "2.5", "BC_CALL_END",
        "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
        "BC_CONST", "1.25", "BC_CONST", "0.0", "BC_BINOP", "+", "BC_PRINT",
        "BC_CONST", "1.0", "BC_CONST", "0.0", "BC_BINOP", "+", "BC_PRINT",
        "BC_CONST", "0.1", "BC_CONST", "0.2", "BC_BINOP", "+", "BC_PRINT",
        "BC_CONST", "1.0", "BC_CONST", "100000.0", "BC_BINOP", "/", "BC_PRINT",
        "BC_CONST", "10000000000000000.0", "BC_CONST", "0.0", "BC_BINOP", "+", "BC_PRINT",
        "BC_CONST", "0.0", "BC_CONST", "1.5", "BC_BINOP", "-", "BC_PRINT",
        "BC_CONST", "0.0", "BC_CONST", "1.0", "BC_BINOP", "-", "BC_CONST", "0.0", "BC_BINOP", "*", "BC_PRINT",
        "BC_CONST", "1.0", "BC_CONST", "0.0", "BC_BINOP", "/", "BC_PRINT",
        "BC_CONST", "0.0", "BC_CONST", "1.0", "BC_BINOP", "-", "BC_CONST", "0.0", "BC_BINOP", "/", "BC_PRINT",
        "BC_CONST", "0.0", "BC_CONST", "0.0", "BC_BINOP", "/", "BC_PRINT",
    ]


DECIMAL_PRINTING_OUTPUT = (
    "2.5\n2.5\n1.25\n1.0\n0.30000000000000004\n1e-05\n1e+16\n-1.5\n"
    "-0.0\ninf\n-inf\nnan\n"
)


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
def test_kuro_owned_x86_linux_codegen_runs_decimal_printing(tmp_path, x86_linux_codegen):
    tokens = decimal_printing_bytecode()
    generated = subprocess.run(
        [str(x86_linux_codegen)],
        input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    executable = tmp_path / "decimal-print-linux"
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
    result = subprocess.run([str(executable)], capture_output=True, text=True, timeout=5, check=True)

    assert result.stdout == DECIMAL_PRINTING_OUTPUT
    assert result.stderr == ""


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
def test_kuro_owned_x86_linux_codegen_runs_decimal_parameter_assignment(tmp_path, x86_linux_codegen):
    tokens = decimal_parameter_assignment_bytecode()
    generated = subprocess.run(
        [str(x86_linux_codegen)],
        input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert generated.returncode == 0, f"generator exited {generated.returncode}: {generated.stderr!r}"
    executable = tmp_path / "decimal-action-mutations-linux"
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
    assert result.stdout == "1\n"
    assert result.stderr == ""


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
@pytest.mark.parametrize(
    ("opcode", "operand", "expected"),
    [("BC_ADD", "2.5", "3.75"), ("BC_ADD", "2", "3.25"), ("BC_UPDATE", "6.25", "6.25")],
)
def test_kuro_owned_x86_linux_codegen_runs_decimal_parameter_mutation(
    tmp_path, x86_linux_codegen, opcode, operand, expected
):
    tokens = decimal_parameter_mutation_bytecode(opcode, operand, expected)
    generated = subprocess.run(
        [str(x86_linux_codegen)],
        input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert generated.returncode == 0, (
        f"{opcode} operand {operand}: generator exited {generated.returncode}; "
        f"stdout={generated.stdout[:200]!r}; stderr={generated.stderr[:200]!r}"
    )
    assert generated.stdout
    executable = tmp_path / f"decimal-{opcode.lower()}-{operand.replace('.', '-')}-linux"
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
    assert result.stdout == "1\n"
    assert result.stderr == ""


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
        '"BC_FUNC_BEGIN", "Add", "BC_PARAM", "A", "Integers", "BC_PARAM", "B", "Integers", "BC_PARAM", "C", "Integers", "BC_PARAM", "D", "Integers", "BC_PARAM", "E", "Integers", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Add", "BC_CONST", "4", "BC_CONST", "2", "BC_CONST", "1", "BC_CONST", "0", "BC_CONST", "-1", "BC_CALL_END", "BC_PRINT"',
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


def test_native_codegen_source_emits_with_macos_arm64_backend(tmp_path):
    from compiler.native import emit_macos_arm64
    from compiler.pipeline import compile_source
    from compiler.self_host import native_codegen_source

    result = compile_source(native_codegen_source("aarch64-macos"))
    assert result.ok, result.diags.render_all()
    assembly = emit_macos_arm64(result.ir)

    assert assembly.startswith(".section __TEXT,__text")
    assert "_kuro_print_int:" in assembly
    assert "_kuro_concat_text:" in assembly
    assert "bl _kuro_concat_text" in assembly
    assert "add x0, x0, #1" in assembly

    object_file = tmp_path / "native-codegen-arm64.o"
    subprocess.run(
        [
            "clang", "-target", "arm64-apple-macos11", "-c", "-x",
            "assembler", "-", "-o", str(object_file),
        ],
        input=assembly,
        capture_output=True,
        text=True,
        check=True,
    )
    assert object_file.stat().st_size > 0


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

    # This uses the same fresh Kuro generator image, not the Python emitter.
    decimal = subprocess.run(
        [str(codegen)],
        input="kuro.bytecode/1\n" + "\n".join(decimal_printing_bytecode()) + "\n",
        capture_output=True, text=True, timeout=60, check=True,
    )
    assert "bl _kuro_decimal_format" in decimal.stdout
    assert "_printf" not in decimal.stdout
    decimal_image = tmp_path / "generated-decimal"
    subprocess.run(
        ["clang", "-nostdlib", "-Wl,-e,_main", "-x", "assembler", "-",
         "-lSystem", "-o", str(decimal_image)],
        input=decimal.stdout, capture_output=True, text=True, check=True,
    )
    printed = subprocess.run(
        [str(decimal_image)], capture_output=True, text=True, timeout=5, check=True,
    )
    assert printed.stdout == DECIMAL_PRINTING_OUTPUT
    assert printed.stderr == ""
    # No libc import is allowed even though the development linker is hosted.
    imports = subprocess.run(
        ["nm", "-u", str(decimal_image)], capture_output=True, text=True, check=True,
    ).stdout
    assert imports.strip() == ""
    accepted_tokens = _bytecode_for_token_limit(if_count=1021, print_count=4)
    boundary = subprocess.run(
        [str(codegen)],
        input="kuro.bytecode/1\n" + "\n".join(accepted_tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert boundary.returncode == 0, boundary.stderr
    assert "L_kuro_else_1020:" in boundary.stdout
    boundary_assembly = tmp_path / "generated-boundary.s"
    boundary_executable = tmp_path / "generated-boundary"
    boundary_assembly.write_text(boundary.stdout, encoding="utf-8")
    subprocess.run(
        ["clang", str(boundary_assembly), "-o", str(boundary_executable)],
        check=True,
    )

    rejected_tokens = _bytecode_for_token_limit(if_count=1022, print_count=3)
    assert len(rejected_tokens) == 4097
    rejected_boundary = subprocess.run(
        [str(codegen)],
        input="kuro.bytecode/1\n" + "\n".join(rejected_tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert rejected_boundary.returncode == 1
    assert rejected_boundary.stdout == ""

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
        (["BC_FUNC_BEGIN", "Echo", "BC_PARAM", "Value", "Decimals", "BC_LOADVAR", "Value", "BC_PRINT",
          "BC_LOADVAR", "Value", "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Echo", "BC_CONST", "2.5",
          "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT"], "2.5\n2.5\n"),
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


def test_kuro_owned_x86_linux_codegen_enforces_4096_token_boundary(tmp_path, x86_linux_codegen):
    accepted_tokens = _bytecode_for_token_limit(if_count=1021, print_count=4)
    rejected_tokens = _bytecode_for_token_limit(if_count=1022, print_count=3)
    assert len(accepted_tokens) == 4096
    assert len(rejected_tokens) == 4097

    def generate(tokens: list[str]):
        return subprocess.run(
            [str(x86_linux_codegen)],
            input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    accepted = generate(accepted_tokens)
    assert accepted.returncode == 0, accepted.stderr
    assert accepted.stderr == ""
    assert "L_kuro_else_1020:" in accepted.stdout
    object_file = tmp_path / "native-codegen-4096-tokens.o"
    subprocess.run(
        [
            "clang", "-target", "x86_64-unknown-linux-gnu", "-c",
            "-x", "assembler", "-", "-o", str(object_file),
        ],
        input=accepted.stdout,
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    assert object_file.read_bytes()[:4] == b"\x7fELF"

    rejected = generate(rejected_tokens)
    assert rejected.returncode == 1
    assert rejected.stdout == ""
    assert rejected.stderr == ""


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
                    "BC_FUNC_BEGIN", "EchoDecimal", "BC_CONST", "2.5", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "EchoDecimal", "BC_CALL_END", "BC_CONST", "2.5",
                    "BC_CMP", "eq", "BC_PRINT",
                ],
                "1\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Choose", "BC_PARAM", "Flag", "Integers",
                    "BC_LOADVAR", "Flag", "BC_CONST", "1", "BC_CMP", "eq", "BC_IF_BEGIN",
                    "BC_CONST", "1.25", "BC_RETURN", "BC_ELSE_BEGIN", "BC_CONST", "2.0", "BC_RETURN",
                    "BC_IF_END", "BC_FUNC_END",
                    "BC_FUNC_BEGIN", "Consume", "BC_PARAM", "Value", "Decimals",
                    "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Choose", "BC_CONST", "0", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_CALL_BEGIN", "Consume", "BC_LOADVAR", "_", "BC_CALL_END", "BC_STORE_LIST", "_",
                    "BC_LOADVAR", "_", "BC_PRINT",
                ],
                "42\n",
            ),
            (
                [
                    "BC_FUNC_BEGIN", "Arithmetic", "BC_PARAM", "Left", "Decimals",
                    "BC_PARAM", "Right", "Integers", "BC_LOADVAR", "Left",
                    "BC_LOADVAR", "Right", "BC_BINOP", "+", "BC_LOADVAR", "Left",
                    "BC_LOADVAR", "Right", "BC_BINOP", "*", "BC_LOADVAR", "Right",
                    "BC_BINOP", "/", "BC_BINOP", "-", "BC_RETURN", "BC_FUNC_END",
                    "BC_CALL_BEGIN", "Arithmetic", "BC_CONST", "1.5", "BC_CONST", "2",
                    "BC_CALL_END", "BC_CONST", "2.0", "BC_CMP", "eq", "BC_PRINT",
                    "BC_CONST", "1.5", "BC_CONST", "2.5", "BC_CMP", "lt", "BC_PRINT",
                    "BC_CONST", "2.5", "BC_CONST", "1.5", "BC_CMP", "gt", "BC_PRINT",
                    "BC_CONST", "2.5", "BC_CONST", "2.5", "BC_CMP", "le", "BC_PRINT",
                    "BC_CONST", "2.5", "BC_CONST", "2.5", "BC_CMP", "ge", "BC_PRINT",
                    "BC_CONST", "2.5", "BC_CONST", "2.5", "BC_CMP", "eq", "BC_PRINT",
                    "BC_CONST", "2.5", "BC_CONST", "2.75", "BC_CMP", "ne", "BC_PRINT",
                    "BC_CONST", "2.5", "BC_CONST", "2.5", "BC_CMP", "ne", "BC_PRINT",
                    "BC_CONST", "2.5", "BC_CONST", "2", "BC_CMP", "gt", "BC_PRINT",
                    "BC_CONST", "2", "BC_CONST", "2.5", "BC_CMP", "lt", "BC_PRINT",
                    "BC_CONST", "-1.5", "BC_CONST", "-0.5", "BC_CMP", "lt", "BC_PRINT",
                ],
                "1\n1\n1\n1\n1\n1\n1\n0\n1\n1\n1\n",
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


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
def test_kuro_owned_x86_linux_codegen_runs_recursive_numeric_actions(tmp_path, x86_linux_codegen):
    tokens, env = compile_program_to_codegen(recursive_numeric_action_program(), target="x86_64-linux")
    assert env["NativeFailed"] == 0
    generated = subprocess.run(
        [str(x86_linux_codegen)],
        input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    executable = tmp_path / "recursive-numeric-actions-linux"
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
    assert result.stdout == "3\n42\n"
    assert result.stderr == ""


def test_native_kuro_codegen_rejects_unknown_output_target(tmp_path):
    from compiler.self_host import SelfHostError, build_native_codegen

    with pytest.raises(SelfHostError, match="unsupported code-generation output target"):
        build_native_codegen(tmp_path / "bad", output_target="x86_64-windows")


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
def test_kuro_owned_x86_linux_codegen_uses_ieee_nan_decimal_comparisons(tmp_path, x86_linux_codegen):
    tokens, env = compile_program_to_codegen(nan_decimal_comparison_program(), target="x86_64-linux")
    assert env["NativeFailed"] == 0
    generated = subprocess.run(
        [str(x86_linux_codegen)],
        input="kuro.bytecode/1\n" + "\n".join(tokens) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    executable = tmp_path / "decimal-nan-comparisons-linux"
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
    assert result.stdout.splitlines() == ["0", "1", "0", "0", "0", "0"]
    assert result.stderr == ""


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
def test_kuro_owned_x86_linux_codegen_runs_four_parameter_actions(tmp_path, x86_linux_codegen):
    tokens, env = compile_program_to_codegen(four_parameter_action_program(), target="x86_64-linux")
    assert env["NativeFailed"] == 0

    executable = tmp_path / "kuro-generated-four-parameters"
    generated = subprocess.run(
        [str(x86_linux_codegen)],
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
    assert result.stdout == "5\n100\n1\n1\nmixed\n5\ntail-text\n9\n"
    assert result.stderr == ""


@pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires a Linux x86-64 execution host",
)
def test_kuro_owned_x86_linux_codegen_runs_abi_stack_spills(tmp_path, x86_linux_codegen):
    tokens, env = compile_program_to_codegen(stack_spill_action_program(), target="x86_64-linux")
    assert env["NativeFailed"] == 0

    executable = tmp_path / "kuro-generated-abi-stack-spills"
    generated = subprocess.run(
        [str(x86_linux_codegen)],
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
    assert result.stdout == "9\n1\n1\ntext9\n1\n"
    assert result.stderr == ""
