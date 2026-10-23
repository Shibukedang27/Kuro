"""Private backend-aware admission; eager VM storage is intentionally unchanged."""
from __future__ import annotations

from io import StringIO
from pathlib import Path
import platform
import subprocess

import pytest

from compiler.bytecode import BytecodeVM, encode_ir
from compiler.interpreter import Interpreter, KuroRuntimeException
from compiler.native import NATIVE_COLLECTION_CAPACITY, build_native, emit_macos_arm64, emit_x86_64_linux
from compiler.pipeline import compile_source, run_source
from test_typecheck_cross import kuro_semantic, python_semantic
from test_vm_cross import run_kuro_vm_environment

ROOT = Path(__file__).resolve().parents[2]
TARGET = {
    ("Linux", "x86_64"): "x86_64-linux",
    ("Linux", "amd64"): "x86_64-linux",
    ("Darwin", "arm64"): "aarch64-macos",
    ("Darwin", "aarch64"): "aarch64-macos",
    ("Darwin", "x86_64"): "x86_64-macos",
    ("Darwin", "amd64"): "x86_64-macos",
}.get((platform.system(), platform.machine().lower()))


def _compile(source):
    result = compile_source(source)
    assert result.ok, result.diags.render_all()
    return result


@pytest.mark.parametrize("used", [0, 1, 65535, 65536, 65537, 10**20])
def test_hosted_and_python_bytecode_admit_without_native_ceiling(used):
    source = f"Call __KuroAdmitRow {used}; Print @_."
    result = run_source(source)
    assert result.ok, result.runtime_error or result.compile.diags.render_all()
    assert result.stdout == f"{used}\n"
    out = StringIO()
    vm = BytecodeVM(encode_ir(result.compile.ir), output=out)
    vm.run()
    assert vm.env["_"] == used
    assert out.getvalue() == result.stdout
    assert any(item.op == "CALL" and item.args[0] == "__KuroAdmitRow" for item in result.compile.ir.main)
    assert not any(item.op == "ARTIFACT_SUFFIX" for item in result.compile.ir.main)


@pytest.mark.parametrize("args", [[], [0, 1], [-1], [1.5], ["2"], [True], [None], [[1, 2]]])
@pytest.mark.parametrize("backend", ["interpreter", "bytecode"])
def test_runtime_private_call_rejects_invalid_operands_even_without_frontend(args, backend):
    compiled = _compile("")
    if backend == "interpreter":
        runtime = Interpreter(compiled.ir, output=StringIO())
        call = runtime.call
    else:
        runtime = BytecodeVM(encode_ir(compiled.ir), output=StringIO())
        call = runtime._call
    with pytest.raises(KuroRuntimeException) as error:
        call("__KuroAdmitRow", args)
    assert error.value.code == "E3001"


@pytest.mark.parametrize("source,valid", [
    ("Call __KuroAdmitRow 0;", True),
    ("Used is Integers; Used = 65537; Call __KuroAdmitRow Used;", True),
    ("Action Gate Used: Integers; Call __KuroAdmitRow Used; Return @_; Done. Call Gate 3;", True),
    ("Call __KuroAdmitRow;", False),
    ("Call __KuroAdmitRow 0, 1;", False),
    ('Call __KuroAdmitRow "bad", 1.25;', False),
    ('Call __KuroAdmitRow "1";', False),
    ("Call __KuroAdmitRow 1.5;", False),
    ("Call __KuroAdmitRow @_;", False),
    ("Action Gate Used; Call __KuroAdmitRow Used; Done.", False),
])
def test_reference_and_authored_semantics_agree(source, valid):
    expected = python_semantic(source)
    actual = kuro_semantic(source)
    assert actual == expected
    assert bool(expected["diagnostics"]) is not valid


def test_both_semantic_passes_reject_reserved_private_action_name():
    source = "Action __KuroAdmitRow Used; Done."
    expected = python_semantic(source)
    actual = kuro_semantic(source)
    assert expected["diagnostics"] == actual["diagnostics"] == [("E4002", 1)]
    assert not compile_source(source).ok
    # Invalid-program symbol tables are not an execution contract: reference
    # usage resolution re-registers declarations after its earlier diagnostic.


@pytest.mark.parametrize("used", [0, 65535, 65536, 65537])
def test_authored_vm_private_call_retains_hosted_ceiling_policy(used):
    env = run_kuro_vm_environment(f"Call __KuroAdmitRow {used}; Print @_.")
    assert env["VMFailed"] == 0
    assert env["VMOutput"] == [used]


def test_authored_vm_private_call_returns_inside_action_without_losing_result():
    env = run_kuro_vm_environment(
        "Action Gate Used: Integers; Call __KuroAdmitRow Used; Return @_; Done.\n"
        "Call Gate 65537; Print @_."
    )
    assert env["VMFailed"] == 0
    assert env["VMOutput"] == [65537]


@pytest.fixture(scope="module")
def admission_image(tmp_path_factory):
    if TARGET is None:
        pytest.skip("requires a supported native executable host")
    source = '''
Mode is Text;
Take user Mode;
Used = 0;
If Mode is equal to "1";
    Used = 1;
Done.
If Mode is equal to "65535";
    Used = 65535;
Done.
If Mode is equal to "65536";
    Used = 65536;
Done.
If Mode is equal to "65537";
    Used = 65536;
    Add 1 to Used;
Done.
If Mode is equal to "-1";
    Used = -1;
Done.
Action Gate Count: Integers;
    Call __KuroAdmitRow Count;
    Return @_;
Done.
Print "before-main".
Call __KuroAdmitRow Used;
Print @_.
Print "before-action".
Call Gate Used;
Print @_.
Print "after".
'''
    image = tmp_path_factory.mktemp("backend-row-admission") / "gate"
    compiled = _compile(source)
    # Exercise this complete boundary driver against ARM64 even on Linux.
    # Do not grow the backend's literal subset just to construct 65537.
    emit_macos_arm64(compiled.ir)
    build_native(compiled.ir, image, target=TARGET)
    return image


@pytest.mark.parametrize("used", [0, 1, 65535, 65536, 65537, -1])
def test_native_main_admission_is_fail_stop_at_real_capacity(admission_image, used):
    assert NATIVE_COLLECTION_CAPACITY == 65536
    result = subprocess.run([str(admission_image)], input=str(used), text=True,
                            capture_output=True, timeout=15, check=False)
    if 0 <= used < NATIVE_COLLECTION_CAPACITY:
        expected = (0, f"before-main\n{used}\nbefore-action\n{used}\nafter\n", "")
    else:
        expected = (1, "before-main\n", "")
    assert (result.returncode, result.stdout, result.stderr) == expected


@pytest.mark.parametrize("used", [65535, 65536, -1])
def test_native_action_admission_guards_before_return(tmp_path, used):
    if TARGET is None:
        pytest.skip("requires a supported native executable host")
    source = f'''Action Gate Count: Integers;
Call __KuroAdmitRow Count;
Print "inside-after".
Return @_;
Done.
Print "before".
Call Gate {used};
Print "after".
'''
    image = tmp_path / "action-gate"
    build_native(_compile(source).ir, image, target=TARGET)
    result = subprocess.run([str(image)], capture_output=True, timeout=15, check=False)
    expected = (0, b"before\ninside-after\nafter\n", b"") if used == 65535 else (1, b"before\n", b"")
    assert (result.returncode, result.stdout, result.stderr) == expected


def test_both_native_emitters_use_capacity_failure_not_bounds_surrogate():
    compiled = _compile("Call __KuroAdmitRow 65536; Print @_.")
    x86 = emit_x86_64_linux(compiled.ir)
    arm = emit_macos_arm64(compiled.ir)
    assert ".Lkuro_overflow" in x86
    assert "L_kuro_collection_overflow" in arm
    assert "call __KuroAdmitRow" not in x86
    assert "bl _kuro_fn___KuroAdmitRow" not in arm


def test_production_vm_admission_precedes_all_three_row_columns():
    vm = (ROOT / "self_host" / "vm.kuro").read_text()
    body = vm.split("Action VMAppendCollectionItem Name, Value;", 1)[1].split("Action VMGetCollectionItem", 1)[0]
    call = body.index("Call __KuroAdmitRow VMCollectionEntryCount;")
    assert body.index("VMFailed = 1;") < call
    for write in ("Set VMCollectionOwners", "Set VMCollectionItems", "Set VMCollectionItemDisplay", "Append VMAppendCollection_Id"):
        assert call < body.index(write)
    assert body.index("Add 1 to VMCollectionEntryCount;") > call


def test_production_vm_hosted_admission_does_not_add_native_limit():
    vm = (ROOT / "self_host" / "vm.kuro").read_text()
    source = vm + '''
Call VMResetCollection "Hosted";
Pos = 0;
While Pos is less than 65537;
    Call VMAppendCollectionItem "Hosted", "row";
    Add 1 to Pos;
Done.
Print VMCollectionEntryCount.
Length VMCollectionItems;
Print @_.
Length VMCollectionItemDisplay;
Print @_.
'''
    result = run_source(source)
    assert result.ok, result.runtime_error or result.compile.diags.render_all()
    assert result.stdout == "65537\n65537\n65537\n"
    assert len(result.interpreter.env["VMCollectionOwners"]) == 65537


@pytest.fixture(scope="module")
def admission_launcher(tmp_path_factory):
    if TARGET is None:
        pytest.skip("requires a supported native executable host")
    from compiler.self_host import build_native_artifact_launcher
    launcher = tmp_path_factory.mktemp("admission-launcher") / "kuro-bytecode"
    build_native_artifact_launcher(launcher, target=TARGET)
    return launcher


@pytest.mark.parametrize("used", [0, 65535, 65536, 65537, -1])
def test_fresh_native_authored_vm_executes_private_call(admission_launcher, used):
    from compiler.self_host import compile_with_kuro_driver
    result = compile_with_kuro_driver(f'Print "before". Call __KuroAdmitRow {used}; Print @_. Print "after".')
    assert result["CompilerFailed"] == 0
    artifact = "kuro.bytecode/1\n" + "\n".join(result["CompilerOutput"]) + "\n"
    execution = subprocess.run([str(admission_launcher)], input=artifact, text=True,
                               capture_output=True, timeout=20, check=False)
    expected = (0, f"before\n{used}\nafter\n", "") if 0 <= used < 65536 else (1, "", "")
    # Authored VM output is buffered until successful execution, unlike direct
    # native source output. No postmortem destination-state claim is made.
    assert (execution.returncode, execution.stdout, execution.stderr) == expected


@pytest.mark.parametrize("target", ["x86_64-linux", "aarch64-macos"])
def test_authored_generator_fails_closed_for_private_runtime_call(target):
    from test_native_codegen import run_codegen
    env = run_codegen('"BC_CALL_BEGIN", "__KuroAdmitRow", "BC_CONST", "0", "BC_CALL_END", "BC_STORE_LIST", "_"', target=target)
    assert env["NativeFailed"] == 1


def test_native_virtual_admission_does_not_allocate_dummy_rows(tmp_path):
    if TARGET is None:
        pytest.skip("requires a supported native executable host")
    source = (ROOT / "self_host" / "vm.kuro").read_text() + '''
Call VMResetCollection "Source";
Call VMAppendCollectionItem "Source", "one";
Call VMAppendCollectionItem "Source", "two";
LogicalUsed = 2;
While LogicalUsed is less than 65536;
    Call __KuroAdmitRow LogicalUsed;
    Add 1 to LogicalUsed;
Done.
Print LogicalUsed.
Print VMCollectionEntryCount.
Length VMCollectionItems;
Print @_.
Length VMCollectionItemDisplay;
Print @_.
Get VMCollectionOwners 1;
Print @_.
Print "before-rejected".
Call __KuroAdmitRow LogicalUsed;
Print "unreachable".
'''
    image = tmp_path / "virtual-admission"
    build_native(_compile(source).ir, image, target=TARGET)
    execution = subprocess.run([str(image)], capture_output=True, timeout=20, check=False)
    assert (execution.returncode, execution.stdout, execution.stderr) == (
        1, b"65536\n2\n2\n2\n0\nbefore-rejected\n", b"",
    )


@pytest.mark.parametrize("emitter", [emit_x86_64_linux, emit_macos_arm64])
@pytest.mark.parametrize("value", ["not-an-integer", 1.25])
def test_native_emitter_rejects_invalid_operand_kinds_without_frontend(emitter, value):
    from compiler.native import NativeBackendError
    compiled = _compile("Call __KuroAdmitRow 0;")
    next(item for item in compiled.ir.main if item.op == "CONST").args = (value,)
    with pytest.raises(NativeBackendError):
        emitter(compiled.ir)


@pytest.mark.parametrize("emitter", [emit_x86_64_linux, emit_macos_arm64])
@pytest.mark.parametrize("arity", [0, 2])
def test_native_emitter_rejects_wrong_arity_without_frontend(emitter, arity):
    from compiler.native import NativeBackendError
    compiled = _compile("Call __KuroAdmitRow 0;")
    call = next(item for item in compiled.ir.main if item.op == "CALL")
    call.args = ("__KuroAdmitRow", *((call.args[1],) * arity))
    with pytest.raises(NativeBackendError):
        emitter(compiled.ir)


def _private_call_vm_source(arguments):
    import json
    from test_vm_cross import BYTECODE_RE
    tokens = ["BC_CALL_BEGIN", "__KuroAdmitRow", *arguments, "BC_CALL_END",
              "BC_STORE_LIST", "_", "BC_CONST_TEXT", "unreachable", "BC_PRINT"]
    wire = "BytecodeOut = " + ", ".join(json.dumps(x) for x in tokens) + ";\n"
    return wire + BYTECODE_RE.sub("", (ROOT / "self_host" / "vm.kuro").read_text(), count=1)


@pytest.mark.parametrize("arguments", [
    [], ["BC_CONST", "0", "BC_CONST", "1"],
    ["BC_CONST_TEXT", "not-numeric"], ["BC_CONST_TEXT", "2"],
    ["BC_CONST", "1.25"], ["BC_CONST", "-1"],
])
def test_authored_vm_rejects_bounded_malformed_private_calls(arguments):
    result = run_source(_private_call_vm_source(arguments))
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is not None or result.interpreter.env["VMFailed"] == 1
    assert "unreachable" not in (result.interpreter.env.get("VMOutput") or [])
    if result.runtime_error is not None:
        assert result.runtime_error.code == "E3001"


@pytest.mark.parametrize("arguments", [
    [], ["BC_CONST", "0", "BC_CONST", "1"],
    ["BC_CONST_TEXT", "not-numeric"], ["BC_CONST_TEXT", "2"],
    ["BC_CONST", "1.25"], ["BC_CONST", "-1"],
])
def test_native_authored_vm_rejects_bounded_malformed_private_calls(admission_launcher, arguments):
    tokens = ["BC_CALL_BEGIN", "__KuroAdmitRow", *arguments, "BC_CALL_END",
              "BC_STORE_LIST", "_", "BC_CONST_TEXT", "unreachable", "BC_PRINT"]
    artifact = "kuro.bytecode/1\n" + "\n".join(tokens) + "\n"
    execution = subprocess.run([str(admission_launcher)], input=artifact, text=True,
                               capture_output=True, timeout=20, check=False)
    assert (execution.returncode, execution.stdout, execution.stderr) == (1, "", "")


@pytest.mark.parametrize("image", ["runtime", "bytecode"])
def test_full_arm64_vm_images_use_typed_admission_bridge_without_widening_inference(image):
    from compiler.self_host import native_artifact_launcher_source, native_runtime_source
    source = (native_runtime_source() if image == "runtime"
              else native_artifact_launcher_source())
    assembly = emit_macos_arm64(_compile(source).ir)
    helper = assembly.split("_kuro_fn_VMAdmitRow:", 1)[1].split("    ret", 1)[0]
    assert "    cmp x0, #0" in helper
    assert "    b.lt L_kuro_collection_overflow" in helper
    assert f"    cmp x0, #{NATIVE_COLLECTION_CAPACITY >> 12}, lsl #12" in helper
    assert "    b.hs L_kuro_collection_overflow" in helper
    assert "    bl _kuro_fn_VMAdmitRow" in assembly
