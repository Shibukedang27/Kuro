import platform
import subprocess
from pathlib import Path

import pytest

from compiler.native import NativeBackendError, build_native, emit_x86_64_linux, emit_x86_64_macos
from compiler.pipeline import compile_source


requires_linux_x86_64 = pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires the Linux x86-64 native backend",
)


def _native_dependency_report(executable: Path) -> str:
    inspector = ["otool", "-L"] if platform.system() == "Darwin" else ["readelf", "-l", "-d"]
    return subprocess.run(
        [*inspector, str(executable)], capture_output=True, text=True, check=True
    ).stdout


def test_native_backend_builds_and_runs_literal_print(tmp_path):
    result = compile_source('Print "native kuro".')
    assert result.ok
    executable = tmp_path / "hello"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "native kuro\n"


@requires_linux_x86_64
def test_x86_64_linux_native_image_has_no_dynamic_loader(tmp_path):
    result = compile_source("Print 2 + 3.")
    assert result.ok
    executable = tmp_path / "static-linux-image"
    build_native(result.ir, executable, target="x86_64-linux")

    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "5\n"
    dependencies = _native_dependency_report(executable)
    assert "INTERP" not in dependencies
    assert "NEEDED" not in dependencies


def test_x86_64_linux_backend_emits_linux_syscall_assembly():
    result = compile_source('N = 2 + 3;\nPrint N.')
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert "syscall" in assembly
    assert ".globl main" in assembly
    assert ".globl _start" in assembly
    assert "mov $60, %eax" in assembly  # Linux exit syscall, no libc startup
    assert "portable" not in assembly  # data is emitted as UTF-8 byte values


def test_x86_64_linux_backend_lowers_variables_and_control_flow():
    result = compile_source(
        'N is Integers;\nN = 0;\nWhile N is less than 2;\nPrint N.\nAdd 1 to N;\nDone.'
    )
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert "sub $" in assembly and "(%rbp)" in assembly
    assert "cmp %rcx, %rax" in assembly
    assert "jz .Lkuro_" in assembly
    assert "jmp .Lkuro_" in assembly
    assert "call _kuro_print_int" in assembly


def test_x86_64_linux_backend_assembles_dynamic_ir(tmp_path):
    result = compile_source(
        'N is Integers;\nN = 0;\nWhile N is less than 2;\nAdd 1 to N;\nDone.'
    )
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    source = tmp_path / "kuro-x86-dynamic.s"
    object_file = tmp_path / "kuro-x86-dynamic.o"
    source.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["clang", "-target", "x86_64-unknown-linux-gnu", "-c", str(source), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert object_file.read_bytes()[:4] == b"\x7fELF"


def test_x86_64_macos_backend_uses_darwin_syscalls_and_assembles(tmp_path):
    result = compile_source('N = 2 + 3;\nPrint N.')
    assert result.ok
    assembly = emit_x86_64_macos(result.ir)
    assert "mov $0x2000001, %eax" in assembly  # Darwin exit
    assert "mov $0x2000004, %rax" in assembly  # Darwin write
    assert ".section __TEXT,__text" in assembly
    source = tmp_path / "kuro-x86-darwin.s"
    object_file = tmp_path / "kuro-x86-darwin.o"
    source.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["clang", "-target", "x86_64-apple-macos", "-c", str(source), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )


def test_x86_64_backend_lowers_stdin_input_and_dynamic_length(tmp_path):
    result = compile_source('Name is Text;\nTake user Name;\nLength Name;\nPrint @_.')
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert "mov $1048575, %rdx" in assembly
    assert ".Lkuro_input_0: .zero 1048576" in assembly
    assert "js .Lkuro_runtime_error" in assembly
    assert ".Lkuro_input_0_read_0:" in assembly
    assert "add %rax, .Lkuro_input_len_0(%rip)" in assembly
    assert ".Lkuro_input_len_0: .zero 8" in assembly
    source = tmp_path / "kuro-input.s"
    object_file = tmp_path / "kuro-input.o"
    source.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["clang", "-target", "x86_64-unknown-linux-gnu", "-c", str(source), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )


def test_x86_64_backend_lowers_runtime_text_concat_and_equality(tmp_path):
    result = compile_source('A = "Ku";\nB = "ro";\nCompare Same A equal to B;\nPrint Same.\nPrint A + B.')
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert "rep movsb" in assembly
    assert ".Lkuro_concat_" in assembly
    source = tmp_path / "kuro-text.s"
    object_file = tmp_path / "kuro-text.o"
    source.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["clang", "-target", "x86_64-unknown-linux-gnu", "-c", str(source), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )


def test_x86_64_backend_emits_recursive_action_frames(tmp_path):
    result = compile_source(
        'Action Fact N;\n'
        'If N is less than 2;\nReturn 1;\n'
        'Else;\nM = N - 1;\nCall Fact M;\nR = @_;\nReturn N * R;\n'
        'Done.\nDone.\nCall Fact 5;\nPrint @_.\n'
    )
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert ".Lkuro_fn_Fact:" in assembly
    assert "call .Lkuro_fn_Fact" in assembly
    assert "push %rbp" in assembly and "leave" in assembly
    source = tmp_path / "kuro-fn.s"
    object_file = tmp_path / "kuro-fn.o"
    source.write_text(assembly, encoding="utf-8")
    subprocess.run(
        ["clang", "-target", "x86_64-unknown-linux-gnu", "-c", str(source), "-o", str(object_file)],
        check=True,
        capture_output=True,
        text=True,
    )
def test_x86_64_linux_backend_emits_collection_storage_and_bounds():
    result = compile_source(
        'Items = 1, 2;\nAppend 3 to Items;\nGet Items 1;\nPrint @_.\n'
    )
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert ".Lkuro_collection_0: .zero 524288" in assembly
    assert ".Lkuro_collection_len_0: .zero 8" in assembly
    assert ".Lkuro_bounds:" in assembly
    assert "(%rax,%rcx,8)" in assembly


def test_x86_64_linux_backend_emits_text_collection_lengths_and_newlines():
    result = compile_source('Items = "A", "B";\nPrint Items.')
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert ".Lkuro_collection_item_len_0: .zero 524288" in assembly
    assert ".Lkuro_newline: .byte 10" in assembly
    assert ".Lkuro_print_text_collection:" in assembly


def test_x86_64_linux_backend_emits_map_storage_and_presence_bits():
    result = compile_source(
        'Store = 0;\nCall MakeMap;\nUpdate Store to @_;\n'
        'Call MapSet Store, "answer", 42;\n'
        'Call MapHas Store, "answer";\nPrint @_.\n'
    )
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert ".Lkuro_map_0: .zero 8192" in assembly
    assert "movq $1, 4096(%rax)" in assembly
    assert "cmpq $0, 4096(%rax)" in assembly


def test_x86_64_linux_backend_propagates_map_text_value_kind():
    result = compile_source(
        'Store = 0;\nCall MakeMap;\nUpdate Store to @_;\n'
        'Call MapSet Store, "message", "hello";\n'
        'Call MapGet Store, "message";\nPrint @_.\n'
    )
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert "cmpq $0, 4096(%rax)" not in assembly or "syscall" in assembly
    assert ".Lkuro_map_0: .zero 8192" in assembly


def test_x86_64_linux_backend_emits_tagged_optional_result_cells():
    result = compile_source(
        'Value = 0;\nCall Some 7;\nUpdate Value to @_;\n'
        'Call IsSome Value;\nPrint @_.\n'
        'Call Unwrap Value;\nPrint @_.\n'
        'Failure = 0;\nCall Err 9;\nUpdate Failure to @_;\n'
        'Call IsErr Failure;\nPrint @_.\n'
    )
    assert result.ok
    assembly = emit_x86_64_linux(result.ir)
    assert ".Lkuro_tagged_0: .zero 16" in assembly
    assert "movq $1, .Lkuro_tagged_0(%rip)" in assembly
    assert "cmpq $1, (%rax)" in assembly
    assert "mov 8(%rax), %rax" in assembly


def test_native_backend_builds_numeric_constants_and_folding(tmp_path):
    result = compile_source("Print 12 + 30.")
    assert result.ok
    executable = tmp_path / "number"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "42\n"


def test_native_backend_propagates_constant_variables(tmp_path):
    result = compile_source('Name = "Ku";\nUpdate Name to "Kuro";\nPrint Name.')
    assert result.ok
    executable = tmp_path / "variable"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "Kuro\n"


def test_native_backend_resolves_constant_action_calls(tmp_path):
    result = compile_source(
        "Action Add A, B;\nReturn A + B;\nDone.\nCall Add 3, 4;\nPrint @_."
    )
    assert result.ok
    executable = tmp_path / "action"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "7\n"


def test_native_backend_executes_dynamic_if(tmp_path):
    result = compile_source(
        'N = 1;\nIf N is equal to 1;\nPrint "yes".\nElse;\nPrint "no".\nDone.'
    )
    assert result.ok
    executable = tmp_path / "if_program"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "yes\n"


def test_native_backend_executes_dynamic_while(tmp_path):
    result = compile_source(
        'N is Integers;\nN = 0;\nWhile N is less than 3;\nPrint "tick".\nAdd 1 to N;\nDone.'
    )
    assert result.ok
    executable = tmp_path / "while_program"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "tick\ntick\ntick\n"


def test_native_backend_prints_dynamic_integer_values(tmp_path):
    result = compile_source(
        'N is Integers;\nN = 0;\nWhile N is less than 3;\nPrint N.\nAdd 1 to N;\nDone.'
    )
    assert result.ok
    executable = tmp_path / "numbers"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "0\n1\n2\n"


def test_native_backend_executes_recursive_actions(tmp_path):
    result = compile_source(
        "Action Fact N;\nIf N is less than or equal to 1;\nReturn 1;\nElse;\n"
        "Call Fact N - 1;\nReturn N * @_;\nDone.\nDone.\n"
        "Call Fact 5;\nPrint @_."
    )
    assert result.ok
    executable = tmp_path / "factorial"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "120\n"


def test_native_backend_handles_constant_collections_and_indexing(tmp_path):
    result = compile_source('Names = "A", "B", "C";\nSet Names 1 to "Long";\nPrint Names.')
    assert result.ok
    executable = tmp_path / "collection"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "A\nLong\nC\n"


def test_native_backend_executes_dynamic_boolean_combinations(tmp_path):
    result = compile_source(
        'A = 1;\nB = 1;\nIf A is equal to 1 and B is equal to 1;\n'
        'Print "yes".\nElse;\nPrint "no".\nDone.'
    )
    assert result.ok
    executable = tmp_path / "boolean"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "yes\n"


def test_native_backend_executes_dynamic_collection_mutation(tmp_path):
    result = compile_source(
        'Items = "a";\nAppend "b" to Items;\nSet Items 1 to "x";\nGet Items 1;\nPrint @_.'
    )
    assert result.ok
    executable = tmp_path / "dynamic_collection"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "x\n"


def test_native_backend_reports_dynamic_collection_length(tmp_path):
    result = compile_source('Items = "a";\nAppend "b" to Items;\nLength Items;\nPrint @_.')
    assert result.ok
    executable = tmp_path / "dynamic_length"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "2\n"


def test_native_backend_executes_repeat_scoping(tmp_path):
    result = compile_source('Repeat 3;\nPrint "x".\nDone.')
    assert result.ok
    executable = tmp_path / "repeat"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "x\nx\nx\n"


def test_native_backend_executes_character_class_predicates(tmp_path):
    result = compile_source(
        'C = "5";\nIf C is digit;\nPrint "yes".\nElse;\nPrint "no".\nDone.'
    )
    assert result.ok
    executable = tmp_path / "class"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "yes\n"


def test_native_backend_concatenates_dynamic_text(tmp_path):
    result = compile_source(
        'A = "Ku";\nB = "ro";\nIf 1 is equal to 1;\nPrint A + B.\nDone.'
    )
    assert result.ok
    executable = tmp_path / "concat"
    build_native(result.ir, executable)
    assert subprocess.run([str(executable)], capture_output=True, text=True, check=True).stdout == "Kuro\n"


def test_native_backend_runs_kuro_authored_compiler_probe(tmp_path):
    """The native image must execute the Kuro-authored compiler path."""
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    files = [root / "self_host" / name for name in ("lexer.kuro", "parser.kuro", "lower.kuro", "bytecode.kuro", "compiler.kuro")]
    source = 'Print "native bootstrap".'
    escaped = source.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    lexer = re.sub(r'^Source = ".*";$', f'Source = "{escaped}";', files[0].read_text(), count=1, flags=re.M)
    parser = re.sub(r"^# --- BEGIN_STANDALONE_TOKENS.*?^# --- END_STANDALONE_TOKENS.*?$\n?", "", files[1].read_text(), count=1, flags=re.M | re.S)
    lower = re.sub(r"^# --- BEGIN_STANDALONE_AST.*?^# --- END_STANDALONE_AST.*?$\n?", "", files[2].read_text(), count=1, flags=re.M | re.S)
    encoder = re.sub(r"^# --- BEGIN_STANDALONE_IR.*?^# --- END_STANDALONE_IR.*?$\n?", "", files[3].read_text(), count=1, flags=re.M | re.S)
    result = compile_source("\n".join((lexer, parser, lower, encoder, files[4].read_text(), "Print CompilerFailed.", "Print CompilerInstructionCount.")))
    assert result.ok
    executable = tmp_path / "kuro-native-compiler"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout.splitlines()[:6] == ["IDENT", "Print", "STRING", "native bootstrap", "DOT", "."]
    assert run.stdout.splitlines()[-2:] == ["0", "3"]
    linked = _native_dependency_report(executable)
    assert "Python" not in linked


def test_native_backend_runs_kuro_authored_runtime(tmp_path):
    from compiler.self_host import build_native_runtime

    executable = tmp_path / "kuro-native-runtime"
    build_native_runtime('Print "native runtime".', executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout.endswith("native runtime\n")


def test_native_backend_runtime_decodes_decimal_constants(tmp_path):
    from compiler.self_host import build_native_runtime

    executable = tmp_path / "kuro-native-runtime-decimal"
    build_native_runtime("Print 12.5.", executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout.endswith("12.5\n")
    linked = _native_dependency_report(executable)
    assert "Python" not in linked


def test_native_backend_runtime_preserves_decimal_after_assignment(tmp_path):
    from compiler.self_host import build_native_runtime

    executable = tmp_path / "kuro-native-runtime-decimal-assignment"
    build_native_runtime("Amount = 3.25; Print Amount.", executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout.endswith("3.25\n")
    linked = _native_dependency_report(executable)
    assert "Python" not in linked


def test_native_backend_runtime_preserves_decimal_through_action_argument(tmp_path):
    from compiler.self_host import build_native_runtime

    executable = tmp_path / "kuro-native-runtime-decimal-action-argument"
    source = "Action Echo Value; Print Value. Done. Call Echo 3.25;"
    build_native_runtime(source, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout.endswith("3.25\n")


def test_native_backend_runtime_preserves_decimal_through_action_return(tmp_path):
    from compiler.self_host import build_native_runtime

    executable = tmp_path / "kuro-native-runtime-decimal-action-return"
    source = "Action Echo Value; Return Value; Done. Call Echo 3.25; Print @_."
    build_native_runtime(source, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout.endswith("3.25\n")


def test_native_backend_runtime_prints_decimal_collection_items(tmp_path):
    from compiler.self_host import build_native_runtime

    executable = tmp_path / "kuro-native-runtime-decimal-collection"
    build_native_runtime("Amounts = 3.25, 4.5; Print Amounts.", executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "3.25\n4.5\n"


def test_native_backend_runtime_clears_stale_decimal_display_on_overwrite(tmp_path):
    from compiler.self_host import build_native_runtime

    executable = tmp_path / "kuro-native-runtime-decimal-overwrite"
    source = "Amount = 3.25; Amount = 4; Print Amount.\nAmounts = 1.25, 2.5; Set Amounts 0 to 7; Print Amounts."
    build_native_runtime(source, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "4\n7\n2.5\n"


@requires_linux_x86_64
def test_native_backend_formats_computed_floats_and_mixed_division(tmp_path):
    result = compile_source(
        "Left = 1.5; Right = 2.25; Print Left + Right.\n"
        "Dividend = 5.5; Divisor = 2; Print Dividend / Divisor.\n"
        "Total = 5.5; Add 0.5 to Total; Print Total.\n"
        "Third = 1.0; Three = 3.0; Print Third / Three.\n"
        "OneTenth = 0.1; TwoTenths = 0.2; Print OneTenth + TwoTenths."
    )
    assert result.ok
    executable = tmp_path / "computed-floats"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "3.75\n2.75\n6.0\n0.3333333333333333\n0.30000000000000004\n"


@requires_linux_x86_64
def test_native_backend_formats_float_collection_items(tmp_path):
    result = compile_source("Amounts = 1.25, 2.5, 3.0; Print Amounts.")
    assert result.ok
    executable = tmp_path / "float-collection"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "1.25\n2.5\n3.0\n"


@requires_linux_x86_64
def test_native_backend_formats_float_action_argument(tmp_path):
    result = compile_source("Action Echo Value; Print Value. Done. Call Echo 1.25;")
    assert result.ok
    executable = tmp_path / "float-action"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "1.25\n"


def test_native_backend_supports_enum_value_abi(tmp_path):
    result = compile_source('Enum Color Red, Green;\nCall MakeEnum "Color", "Green";\nPrint @_.')
    assert result.ok
    executable = tmp_path / "enum"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "Color.Green\n"


def test_native_backend_supports_numeric_optional_result_abi(tmp_path):
    result = compile_source(
        'Call Some 7;\nCall IsSome @_;\nPrint @_.\n'
        'Call Some 9;\nCall Unwrap @_;\nPrint @_.\n'
        'Call Ok 11;\nCall Unwrap @_;\nPrint @_.\n'
    )
    assert result.ok
    executable = tmp_path / "tagged"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "1\n9\n11\n"


def test_native_backend_supports_closure_invoke_abi(tmp_path):
    result = compile_source(
        'Prefix = "Kuro ";\n'
        'Action Greet Name;\nReturn Prefix + Name;\nDone.\n'
        'Call MakeClosure "Greet";\nCall Invoke @_, "native";\nPrint @_.\n'
    )
    assert result.ok
    executable = tmp_path / "closure"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "Kuro native\n"


@requires_linux_x86_64
def test_native_backend_dispatches_to_runtime_selected_closure(tmp_path):
    result = compile_source(
        "First = 0; Second = 0; Selected = 0; Choice = 1;\n"
        "Action Ten Value; Return Value + 10; Done.\n"
        "Action Twenty Value; Return Value + 20; Done.\n"
        'Call MakeClosure "Ten"; Update First to @_;\n'
        'Call MakeClosure "Twenty"; Update Second to @_;\n'
        "If Choice is equal to 1; Update Selected to First;\n"
        "Else; Update Selected to Second; Done.\n"
        "Call Invoke Selected, 5; Print @_."
    )
    assert result.ok
    executable = tmp_path / "dynamic-closure"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "15\n"


@requires_linux_x86_64
def test_native_backend_returns_branch_selected_closure_targets(tmp_path):
    result = compile_source(
        'First = 0; Second = 0;\n'
        'Action Ten Value; Return Value + 10; Done.\n'
        'Action Twenty Value; Return Value + 20; Done.\n'
        'Action MakeChoice Choice;\n'
        'Selected = 0;\n'
        'If Choice is equal to 1;\n'
        'Call MakeClosure "Ten"; Update Selected to @_;\n'
        'Else;\n'
        'Call MakeClosure "Twenty"; Update Selected to @_;\n'
        'Done.\nReturn Selected;\nDone.\n'
        'Call MakeChoice 1; Update First to @_;\n'
        'Call MakeChoice 0; Update Second to @_;\n'
        'Call Invoke First, 5; Print @_.\n'
        'Call Invoke Second, 5; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "branch-returned-closures"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "15\n25\n"


def test_native_backend_rejects_mixed_closure_and_scalar_action_returns():
    result = compile_source(
        'Chosen = 0;\n'
        'Action Ten Value; Return Value + 10; Done.\n'
        'Action MakeChoice Choice;\n'
        'Selected = 0;\n'
        'If Choice is equal to 1;\n'
        'Call MakeClosure "Ten"; Update Selected to @_;\n'
        'Else; Update Selected to Choice; Done.\n'
        'Return Selected;\nDone.\n'
        'Call MakeChoice 1; Update Chosen to @_;\n'
        'Call Invoke Chosen, 5; Print @_.\n'
    )
    assert result.ok
    with pytest.raises(NativeBackendError, match="statically known targets"):
        emit_x86_64_linux(result.ir)


@requires_linux_x86_64
def test_native_backend_captures_one_escaping_numeric_value(tmp_path):
    result = compile_source(
        'Adder = 0;\n'
        'Action MakeAdder Base;\n'
        'Action AddBase Value;\nReturn Base + Value;\nDone.\n'
        'Call MakeClosure "AddBase";\nReturn @_;\nDone.\n'
        'Call MakeAdder 10; Update Adder to @_;\n'
        'Call Invoke Adder, 7; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "captured-closure"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "17\n"


@requires_linux_x86_64
def test_native_backend_captures_and_computes_with_float_value(tmp_path):
    result = compile_source(
        'Adder = 0;\n'
        'Action MakeAdder Base;\n'
        'Action AddBase Value;\nReturn Base + Value;\nDone.\n'
        'Call MakeClosure "AddBase";\nReturn @_;\nDone.\n'
        'Call MakeAdder 1.25; Update Adder to @_;\n'
        'Call Invoke Adder, 2.5; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "captured-float-closure"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "3.75\n"


@requires_linux_x86_64
def test_native_backend_supports_independent_captured_closure_instances(tmp_path):
    result = compile_source(
        'First = 0; Second = 0;\n'
        'Action MakeAdder Base;\n'
        'Action AddBase Value;\nReturn Base + Value;\nDone.\n'
        'Call MakeClosure "AddBase";\nReturn @_;\nDone.\n'
        'Call MakeAdder 10; Update First to @_;\n'
        'Call MakeAdder 20; Update Second to @_;\n'
        'Call Invoke First, 7; Print @_.\n'
        'Call Invoke Second, 7; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "second-captured-closure"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "17\n27\n"


@requires_linux_x86_64
def test_native_backend_allocates_closures_across_heap_pages(tmp_path):
    source = (
        'First = 0; Last = 0;\n'
        'Action MakeAdder Base;\n'
        'Action AddBase Value;\nReturn Base + Value;\nDone.\n'
        'Call MakeClosure "AddBase";\nReturn @_;\nDone.\n'
        'Call MakeAdder 10; Update First to @_;\n'
        + "".join(
            f"Call MakeAdder {value}; Update Last to @_;\n"
            for value in range(1, 129)
        )
        + 'Call Invoke First, 7; Print @_.\n'
        + 'Call Invoke Last, 7; Print @_.\n'
    )
    result = compile_source(source)
    assert result.ok
    executable = tmp_path / "closures-across-heap-pages"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "17\n135\n"


@requires_linux_x86_64
def test_native_backend_captures_text_in_independent_closures(tmp_path):
    result = compile_source(
        'First = 0; Second = 0;\n'
        'Action MakeGreeter Prefix;\n'
        'Action Greet Name;\nReturn Prefix + Name;\nDone.\n'
        'Call MakeClosure "Greet";\nReturn @_;\nDone.\n'
        'Call MakeGreeter "Kuro "; Update First to @_;\n'
        'Call MakeGreeter "Hello "; Update Second to @_;\n'
        'Call Invoke First, "native"; Print @_.\n'
        'Call Invoke Second, "world"; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "text-captured-closures"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "Kuro native\nHello world\n"


@requires_linux_x86_64
def test_native_backend_captures_and_updates_record_via_closure(tmp_path):
    result = compile_source(
        'Store = 0; Modifier = 0;\n'
        'Call MakeRecord "User"; Update Store to @_;\n'
        'Call RecordSet Store, "rank", 40;\n'
        'Action MakeBumper UserRecord;\n'
        'Action Bump Delta; Rank = 0;\n'
        'Call RecordGet UserRecord, "rank"; Update Rank to @_;\n'
        'Add Delta to Rank;\n'
        'Call RecordSet UserRecord, "rank", Rank; Return Rank; Done.\n'
        'Call MakeClosure "Bump"; Return @_; Done.\n'
        'Call MakeBumper Store; Update Modifier to @_;\n'
        'Call Invoke Modifier, 2; Print @_.\n'
        'Call RecordGet Store, "rank"; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "captured-record-field-update"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "42\n42\n"


@requires_linux_x86_64
def test_native_backend_captures_and_updates_map_via_closure(tmp_path):
    result = compile_source(
        'Store = 0; Mutator = 0;\n'
        'Call MakeMap; Update Store to @_;\n'
        'Call MapSet Store, "answer", 40;\n'
        'Action MakeBumper UserMap;\n'
        'Action Bump Delta; Current = 0;\n'
        'Call MapHas UserMap, "answer"; Print @_.\n'
        'Call MapGet UserMap, "answer"; Update Current to @_;\n'
        'Add Delta to Current;\n'
        'Call MapSet UserMap, "answer", Current; Return Current; Done.\n'
        'Call MakeClosure "Bump"; Return @_; Done.\n'
        'Call MakeBumper Store; Update Mutator to @_;\n'
        'Call Invoke Mutator, 2; Print @_.\n'
        'Call MapGet Store, "answer"; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "captured-map-update"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "1\n42\n42\n"


@requires_linux_x86_64
def test_native_backend_captures_collections_for_indexed_closure_access(tmp_path):
    result = compile_source(
        'Values = 10, 20, 30; Other = 1, 2, 3;\n'
        'AliasValues = Values; AliasOther = 0; First = 0; Second = 0;\n'
        'Update AliasOther to Other;\n'
        'Action MakeAccess Bag;\n'
        'Action Modify Index; Current = 0;\n'
        'Get Bag Index; Update Current to @_; Add 1 to Current;\n'
        'Set Bag Index to Current; Return Current; Done.\n'
        'Call MakeClosure "Modify"; Return @_; Done.\n'
        'Call MakeAccess AliasValues; Update First to @_;\n'
        'Call MakeAccess AliasOther; Update Second to @_;\n'
        'Call Invoke First, 1; Print @_.\n'
        'Call Invoke Second, 0; Print @_.\n'
        'Get Values 1; Print @_. Get Other 0; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "captured-collection-index-update"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "21\n2\n21\n2\n"


@requires_linux_x86_64
def test_native_backend_captures_text_collections_for_indexed_reads(tmp_path):
    result = compile_source(
        'Values = "red", "blue"; Reader = 0;\n'
        'Action MakeReader Bag;\n'
        'Action Read Index; Get Bag Index; Print @_. Return Index; Done.\n'
        'Call MakeClosure "Read"; Return @_; Done.\n'
        'Call MakeReader Values; Update Reader to @_;\n'
        'Call Invoke Reader, 1; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "captured-text-collection-read"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "blue\n1\n"


@pytest.mark.parametrize(
    ("values", "operation", "message"),
    [
        ("1, 2", "Length Bag;", "LENGTH does not yet support captured collection lengths"),
        ("1, 2", "Append 3 to Bag;", "APPEND does not yet support captured collection length metadata"),
        ("1, 2", 'Set Bag 0 to "wrong";', "SET value kind must match the known element kind"),
        ('"a", "b"', 'Set Bag 0 to "longer";', "does not yet update text item lengths"),
    ],
)
def test_native_backend_rejects_captured_collection_operations_without_length_metadata(
    values, operation, message
):
    result = compile_source(
        f'Values = {values}; Reader = 0;\n'
        'Action MakeAccess Bag;\n'
        f'Action Read Dummy; {operation} Return Dummy; Done.\n'
        'Call MakeClosure "Read"; Return @_; Done.\n'
        'Call MakeAccess Values; Update Reader to @_;\n'
    )
    assert result.ok
    with pytest.raises(NativeBackendError, match=message):
        emit_x86_64_linux(result.ir)


def test_native_backend_rejects_closure_value_capture():
    result = compile_source(
        'Stored = 0; Holder = 0;\n'
        'Action Work Value; Return Value; Done.\n'
        'Action MakeHolder Captured;\n'
        'Action GetClosure Dummy; Return Captured; Done.\n'
        'Call MakeClosure "GetClosure"; Return @_; Done.\n'
        'Call MakeClosure "Work"; Update Stored to @_;\n'
        'Call MakeHolder Stored; Update Holder to @_;\n'
    )
    assert result.ok
    with pytest.raises(NativeBackendError, match="numeric, text, record, map, or collection captures only"):
        emit_x86_64_linux(result.ir)


def test_native_backend_rejects_mixed_numeric_capture_kinds():
    result = compile_source(
        'First = 0; Second = 0;\n'
        'Action MakeAdder Base;\n'
        'Action AddBase Value;\nReturn Base + Value;\nDone.\n'
        'Call MakeClosure "AddBase";\nReturn @_;\nDone.\n'
        'Call MakeAdder 1.25; Update First to @_;\n'
        'Call MakeAdder 10; Update Second to @_;\n'
        'Call Invoke First, 2.5; Print @_.\n'
    )
    assert result.ok
    with pytest.raises(NativeBackendError, match="numeric, text, record, map, or collection captures only"):
        emit_x86_64_linux(result.ir)


def test_native_backend_supports_record_field_abi(tmp_path):
    result = compile_source(
        'Store = 0;\nCall MakeRecord "User";\nUpdate Store to @_;\n'
        'Call RecordSet Store, "name", "Kuro";\n'
        'Call RecordSet Store, "rank", 7;\n'
        'Call RecordGet Store, "name";\nPrint @_.\n'
        'Call RecordGet Store, "rank";\nPrint @_.\n'
    )
    assert result.ok
    executable = tmp_path / "record"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "Kuro\n7\n"


@requires_linux_x86_64
@pytest.mark.parametrize("choice, field, initial_value", [(1, "name", 1), (0, "rank", 2)])
def test_native_backend_dispatches_branch_selected_record_fields(tmp_path, choice, field, initial_value):
    result = compile_source(
        f'Store = 0; Choice = {choice}; Field = "";\n'
        'Call MakeRecord "User"; Update Store to @_;\n'
        'Call RecordSet Store, "name", 1;\n'
        'Call RecordSet Store, "rank", 2;\n'
        'If Choice is equal to 1; Update Field to "name";\n'
        'Else; Update Field to "rank"; Done.\n'
        'Call RecordGet Store, Field; Print @_.\n'
        'Call RecordSet Store, Field, 42;\n'
        f'Call RecordGet Store, "{field}"; Print @_.\n'
    )
    assert result.ok
    executable = tmp_path / "dynamic-record-fields"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == f"{initial_value}\n42\n"


def test_native_backend_rejects_unbounded_runtime_record_field_name():
    result = compile_source(
        'Store = 0; Field = "name" + "suffix";\n'
        'Call MakeRecord "User"; Update Store to @_;\n'
        'Call RecordGet Store, Field; Print @_.\n'
    )
    assert result.ok
    with pytest.raises(NativeBackendError, match="statically bounded field-name set"):
        emit_x86_64_linux(result.ir)


def test_native_backend_supports_map_abi_for_known_keys(tmp_path):
    result = compile_source(
        'Store = 0;\nCall MakeMap;\nUpdate Store to @_;\n'
        'Call MapHas Store, "missing";\nPrint @_.\n'
        'Call MapSet Store, "answer", 42;\n'
        'Call MapHas Store, "answer";\nPrint @_.\n'
        'Call MapGet Store, "answer";\nPrint @_.\n'
    )
    assert result.ok
    executable = tmp_path / "map"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "0\n1\n42\n"


def test_native_backend_supports_deterministic_task_abi(tmp_path):
    result = compile_source(
        'Action Work Value;\nReturn Value + 1;\nDone.\n'
        'Call MakeClosure "Work";\nCall Spawn @_, 4;\nCall Await @_;\nPrint @_.\n'
    )
    assert result.ok
    executable = tmp_path / "task"
    build_native(result.ir, executable)
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "5\n"


def test_native_cli_accepts_explicit_target_flag(tmp_path, capsys):
    from cli.kuro import main
    source = tmp_path / "main.kuro"
    source.write_text('Print "target".', encoding="utf-8")
    assert main(["kuro", "native", str(source), "--target", "not-a-target"]) == 1
    assert "unsupported native target" in capsys.readouterr().err


def test_native_compiler_cli_accepts_target_flag(tmp_path, capsys):
    from cli.kuro import main

    assert main(["kuro", "native-compiler", "ignored.kuro", "--target", "not-a-target"]) == 1
    assert "unsupported native target" in capsys.readouterr().err


def test_native_runtime_image_reads_arbitrary_source_from_stdin(tmp_path):
    from compiler.self_host import build_native_runtime

    executable = tmp_path / "kuro-native-runtime-stdin"
    build_native_runtime(None, executable)
    run = subprocess.run([str(executable)], input='Print "stdin source".\n', capture_output=True, text=True, check=True)
    assert run.stdout.endswith("stdin source\n")


def test_native_backend_accepts_compiler_sized_stdin(tmp_path):
    result = compile_source("Source is Text; Take user Source; Length Source; Print @_ .")
    assert result.ok
    executable = tmp_path / "large-input"
    build_native(result.ir, executable)

    source = "K" * 71000
    run = subprocess.run(
        [str(executable)], input=source, capture_output=True, text=True, check=True
    )
    assert run.stdout == "71000\n"


def test_native_backend_artifact_suffix_copies_text_and_rejects_bad_offsets(tmp_path):
    valid = compile_source('Call __KuroArtifactSuffix "prefix-tail", 7;\nPrint @_.')
    assert valid.ok, valid.diags.render_all()
    valid_executable = tmp_path / "suffix-valid"
    build_native(valid.ir, valid_executable)
    run = subprocess.run(
        [str(valid_executable)], capture_output=True, text=True, check=False
    )
    assert run.returncode == 0, run.stderr
    assert run.stdout == "tail\n"

    for offset in (-1, 12):
        invalid = compile_source(
            f'Call __KuroArtifactSuffix "prefix-tail", {offset};\nPrint @_.'
        )
        assert invalid.ok, invalid.diags.render_all()
        executable = tmp_path / f"suffix-invalid-{offset}"
        build_native(invalid.ir, executable)
        rejected = subprocess.run(
            [str(executable)], capture_output=True, text=True, check=False
        )
        assert rejected.returncode == 1
        assert rejected.stdout == ""


def test_native_backend_rejects_suffix_source_without_known_text_kind():
    from compiler.ir import IRFunction, IRProgram, Instr

    program = IRProgram(
        main=[
            Instr("CONST", (7,), "t0"),
            Instr("CONST", (0,), "t1"),
            Instr("ARTIFACT_SUFFIX", ("t0", "t1"), "t2"),
        ]
    )
    with pytest.raises(NativeBackendError, match="statically known Text source"):
        emit_x86_64_linux(program)

    function = IRFunction(
        "UseSuffix",
        [],
        [
            Instr("CONST", (7,), "t0"),
            Instr("CONST", (0,), "t1"),
            Instr("ARTIFACT_SUFFIX", ("t0", "t1"), "t2"),
        ],
    )
    action_program = IRProgram(functions={"UseSuffix": function})
    with pytest.raises(NativeBackendError, match="statically known Text source"):
        emit_x86_64_linux(action_program)


def test_macos_arm64_suffix_requires_proven_text_sources():
    from compiler.ir import IRFunction, IRProgram, Instr
    from compiler.native import emit_macos_arm64

    returns_integer = IRFunction(
        "ReturnsInteger", [],
        [Instr("CONST", (7,), "t0"), Instr("RETURN", ("t0",))],
    )
    untyped_result = IRProgram(
        main=[
            Instr("CALL", ("ReturnsInteger",), "TextResult"),
            Instr("CONST", (0,), "t1"),
            Instr("ARTIFACT_SUFFIX", ("TextResult", "t1"), "t2"),
        ],
        functions={"ReturnsInteger": returns_integer},
    )
    with pytest.raises(NativeBackendError, match="statically known Text source"):
        emit_macos_arm64(untyped_result)

    def action_program(action):
        return IRProgram(
            main=[
                Instr("CONST", ("prefix-tail",), "t0"),
                Instr("CONST", (7,), "t1"),
                Instr("CALL", (action.name, "t0", "t1"), "t2"),
            ],
            functions={action.name: action},
        )

    untyped_action = IRFunction(
        "UseSuffix", ["TextSource", "Offset"],
        [
            Instr("ARTIFACT_SUFFIX", ("TextSource", "Offset"), "t0"),
            Instr("RETURN", ("t0",)),
        ],
    )
    with pytest.raises(NativeBackendError, match="statically known Text source"):
        emit_macos_arm64(action_program(untyped_action))

    typed_action = IRFunction(
        "UseSuffix", ["Source", "Offset"],
        [
            Instr("ARTIFACT_SUFFIX", ("Source", "Offset"), "t0"),
            Instr("RETURN", ("t0",)),
        ],
        parameter_types={"Source": "Text", "Offset": "Integers"},
    )
    assembly = emit_macos_arm64(action_program(typed_action))
    assert "bl _strlen" in assembly
    assert "bl _kuro_artifact_suffix" in assembly
    assert "add x0, x0, x1" in assembly
    assert "L_kuro_artifact_suffix_error:" in assembly
    assert "_kuro_text_heap" not in assembly
    assert "bl _memcpy" not in assembly


def test_macos_arm64_dynamic_print_uses_user_pointer_bounds():
    from compiler.ir import IRFunction, IRProgram, Instr
    from compiler.native import emit_macos_arm64

    printer = IRFunction(
        "PrintValue",
        ["Value"],
        [
            Instr("JUMP", ("print_value",)),
            Instr("LABEL", (), "print_value"),
            Instr("PRINT", ("Value",)),
        ],
        parameter_types={"Value": "Text"},
    )
    program = IRProgram(
        main=[
            Instr("CONST", ("hello",), "t0"),
            Instr("CALL", ("PrintValue", "t0"), "t1"),
        ],
        functions={"PrintValue": printer},
    )

    assembly = emit_macos_arm64(program)
    assert "mov x1, #0x100000000" in assembly
    assert "mov x1, #0x1000000000000" in assembly
    assert "cmp x0, #4096" not in assembly


@requires_linux_x86_64
def test_native_backend_accepts_text_suffix_source_in_typed_action(tmp_path):
    source = (
        "Action Tail Source: Text, Offset: Integers;\n"
        "Call __KuroArtifactSuffix Source, Offset;\n"
        "Return @_;\nDone.\n"
        'Call Tail "prefix-tail", 7;\nPrint @_.'
    )
    result = compile_source(source)
    assert result.ok, result.diags.render_all()
    executable = tmp_path / "suffix-action"
    build_native(result.ir, executable, target="x86_64-linux")
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stderr
    assert run.stdout == "tail\n"


def test_native_compiler_image_compiles_arbitrary_source_from_stdin(tmp_path):
    from compiler.self_host import (
        build_native_artifact_launcher,
        build_native_compiler,
        native_compiler_source,
    )

    executable = tmp_path / "kuro-native-compiler-stdin"
    build_native_compiler(None, executable)
    assert Path(f"{executable}.source.kuro").read_text(encoding="utf-8") == native_compiler_source()
    run = subprocess.run([str(executable)], input="Print 12.5.\n", capture_output=True, text=True, check=True)
    assert run.stdout.splitlines() == ["kuro.bytecode/1", "BC_CONST", "12.5", "BC_PRINT"]

    rejected = subprocess.run(
        [str(executable)], input="Print 12.5", capture_output=True, text=True, check=False
    )
    assert rejected.returncode == 1
    assert rejected.stdout == "kuro.compile-error/1\n"
    for source, encoded in (
        ('Print "".', r"\e"),
        ('Print "a\\nb".', r"a\nb"),
        ('Print "a\\rb".', r"a\rb"),
    ):
        accepted = subprocess.run(
            [str(executable)], input=source, capture_output=True, text=True, timeout=5,
        )
        assert accepted.returncode == 0
        assert accepted.stdout.splitlines() == [
            "kuro.bytecode/1", "BC_CONST_TEXT", encoded, "BC_PRINT"
        ]

    self_build = subprocess.run(
        [str(executable)],
        input=native_compiler_source(),
        capture_output=True,
        text=True,
        timeout=10,
    )
    self_lines = self_build.stdout.splitlines()
    assert self_build.returncode == 0
    assert self_lines[0] == "kuro.bytecode/1"
    assert len(self_lines) > 6000
    assert "BC_FUNC_BEGIN" in self_lines
    assert "BC_CALL_BEGIN" in self_lines

    # Execute the compiler artifact produced by the native compiler, use that
    # artifact to compile a fresh program, then execute the fresh bytecode.
    # This is the complete Python-free production chain after image creation.
    launcher = tmp_path / "kuro-bytecode"
    build_native_artifact_launcher(launcher)
    second_stage = subprocess.run(
        [str(launcher)],
        input=self_build.stdout + "kuro.input/1\nPrint 6 * 7.\n",
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    assert second_stage.stdout.splitlines() == [
        "kuro.bytecode/1", "BC_CONST", "6", "BC_CONST", "7",
        "BC_BINOP", "*", "BC_PRINT",
    ]
    executed = subprocess.run(
        [str(launcher)], input=second_stage.stdout,
        capture_output=True, text=True, timeout=5, check=True,
    )
    assert executed.stdout == "42\n"


@pytest.mark.skipif(platform.system() != "Darwin", reason="requires the macOS x86-64 linker/runtime")
def test_x86_64_macos_native_compiler_self_rebuild_chain(tmp_path):
    from compiler.self_host import (
        build_native_artifact_launcher,
        build_native_compiler,
        native_compiler_source,
    )

    compiler = tmp_path / "kuro-x86-compiler"
    launcher = tmp_path / "kuro-x86-bytecode"
    build_native_compiler(None, compiler, target="x86_64-macos")
    build_native_artifact_launcher(launcher, target="x86_64-macos")

    direct = subprocess.run(
        [str(compiler)], input="Print 6 * 7.\n",
        capture_output=True, text=True, timeout=10, check=True,
    )
    assert direct.stdout.splitlines() == [
        "kuro.bytecode/1", "BC_CONST", "6", "BC_CONST", "7",
        "BC_BINOP", "*", "BC_PRINT",
    ]
    assert subprocess.run(
        [str(launcher)], input=direct.stdout,
        capture_output=True, text=True, timeout=10, check=True,
    ).stdout == "42\n"

    self_build = subprocess.run(
        [str(compiler)], input=native_compiler_source(),
        capture_output=True, text=True, timeout=15, check=True,
    )
    assert len(self_build.stdout.splitlines()) > 6000
    second_stage = subprocess.run(
        [str(launcher)],
        input=self_build.stdout + "kuro.input/1\nPrint 6 * 7.\n",
        capture_output=True, text=True, timeout=15, check=True,
    )
    assert second_stage.stdout == direct.stdout
    assert subprocess.run(
        [str(launcher)], input=second_stage.stdout,
        capture_output=True, text=True, timeout=10, check=True,
    ).stdout == "42\n"
