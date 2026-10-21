"""Native collection indexing must respect each owner's logical length.

The native backend reserves fixed-capacity storage, but spare slots are not
members of a collection. GET alone accepts Python-style negative indices;
SET requires a nonnegative index within the logical length.
"""
from __future__ import annotations

import io
import json
import platform
import subprocess

import pytest

from compiler.bytecode import BytecodeProgram, BytecodeVM, encode_ir
from compiler.interpreter import KuroRuntimeException
from compiler.native import (
    NATIVE_COLLECTION_CAPACITY,
    NativeBackendError,
    build_native,
    emit_macos_arm64,
    emit_x86_64_linux,
    emit_x86_64_macos,
)
from compiler.pipeline import compile_source, run_source
from test_vm_cross import run_kuro_vm_environment

LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {
    "x86_64", "amd64"
}
INT64_MAX = "9223372036854775807"
INT64_MIN_EXPR = "(0 - 9223372036854775807 - 1)"


def _access_source(operation: str, index: str | int, *, action: bool = False) -> str:
    """A two-element owned integer collection, with no output before access."""
    if operation not in {"get", "set"}:
        raise ValueError(operation)
    if action:
        body = "LocalItems = 11, 22;\n"
        if operation == "get":
            body += "Get LocalItems Index;\nPrint @_.\n"
        else:
            body += (
                "Set LocalItems Index to 99;\n"
                "Get LocalItems 0;\nPrint @_.\nGet LocalItems 1;\nPrint @_.\n"
            )
        return (
            "Action Access Index: Integers;\n"
            + body
            + "Return 0;\nDone.\n"
            + f"Call Access {index};\n"
        )
    prefix = "Items = 11, 22;\n"
    if operation == "get":
        return prefix + f"Get Items {index};\nPrint @_.\n"
    return (
        prefix
        + f"Set Items {index} to 99;\n"
        + "Get Items 0;\nPrint @_.\nGet Items 1;\nPrint @_.\n"
    )


def _compile(source: str):
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    return compiled


def _logical_runtimes(source: str) -> dict[str, dict]:
    """Capture hosted interpreter, Python bytecode VM and authored Kuro VM."""
    hosted_result = run_source(source)
    assert hosted_result.compile.ok, hosted_result.compile.diags.render_all()
    hosted_error = hosted_result.runtime_error
    hosted = {
        "stdout": hosted_result.stdout or "",
        "error": None if hosted_error is None else (hosted_error.code, hosted_error.message),
    }

    compiled = _compile(source)
    output = io.StringIO()
    vm = BytecodeVM(BytecodeProgram.from_data(json.loads(json.dumps(
        encode_ir(compiled.ir).to_data()
    ))), output=output)
    bytecode_error = None
    try:
        vm.run()
    except KuroRuntimeException as exc:
        bytecode_error = (exc.code, exc.message)
    bytecode = {"stdout": output.getvalue(), "error": bytecode_error}

    environment = run_kuro_vm_environment(source)
    values = environment.get("VMOutput", [])
    displays = environment.get("VMOutputDisplay", [])
    authored = {
        "stdout": "".join(
            (display if display else str(value)) + "\n"
            for value, display in zip(values, displays)
        ),
        "failed": bool(environment.get("VMFailed", 0)),
    }
    return {"hosted": hosted, "bytecode": bytecode, "kuro_vm": authored}


def _native(source: str, tmp_path, name: str = "native-collection-bounds"):
    executable = tmp_path / name
    build_native(_compile(source).ir, executable, target="x86_64-linux")
    return subprocess.run(
        [str(executable)], text=True, capture_output=True, check=False, timeout=15
    )


def _assert_logical_failure(observations: dict[str, dict], *, native=None) -> None:
    for runtime in ("hosted", "bytecode"):
        assert observations[runtime]["error"] is not None, (runtime, observations)
        assert observations[runtime]["error"][0] == "E6001"
        assert observations[runtime]["stdout"] == ""
    assert observations["kuro_vm"]["failed"]
    assert observations["kuro_vm"]["stdout"] == ""
    if native is not None:
        assert (native.returncode, native.stdout, native.stderr) == (1, "", "")


@pytest.mark.skipif(not LINUX_X86, reason="native executable coverage targets Linux x86_64")
@pytest.mark.parametrize(
    "operation,index,expected",
    [
        ("get", -2, "11\n"),   # first element: -L is inclusive
        ("get", -1, "22\n"),   # last element
        ("set", 0, "99\n22\n"),
        ("set", 1, "11\n99\n"),
    ],
)
def test_main_collection_valid_indices_match_all_runtimes(
    tmp_path, operation, index, expected
):
    source = _access_source(operation, index)
    observations = _logical_runtimes(source)
    assert {name: value["stdout"] for name, value in observations.items()} == {
        "hosted": expected,
        "bytecode": expected,
        "kuro_vm": expected,
    }
    assert observations["hosted"]["error"] is None
    assert observations["bytecode"]["error"] is None
    assert not observations["kuro_vm"]["failed"]
    native = _native(source, tmp_path)
    assert (native.returncode, native.stdout, native.stderr) == (0, expected, "")


@pytest.mark.skipif(not LINUX_X86, reason="native executable coverage targets Linux x86_64")
@pytest.mark.parametrize(
    "operation,index",
    [
        ("get", -3), ("get", 2), ("get", NATIVE_COLLECTION_CAPACITY - 1),
        ("get", INT64_MAX), ("get", INT64_MIN_EXPR),
        ("set", -1), ("set", 2), ("set", NATIVE_COLLECTION_CAPACITY - 1),
        ("set", INT64_MAX), ("set", INT64_MIN_EXPR),
    ],
)
def test_main_collection_rejects_outside_logical_bounds(
    tmp_path, operation, index
):
    source = _access_source(operation, index)
    observations = _logical_runtimes(source)
    _assert_logical_failure(observations, native=_native(source, tmp_path))


@pytest.mark.skipif(not LINUX_X86, reason="native executable coverage targets Linux x86_64")
@pytest.mark.parametrize(
    "operation,index,expected",
    [
        ("get", -2, "11\n"), ("get", -1, "22\n"),
        ("set", 0, "99\n22\n"), ("set", 1, "11\n99\n"),
    ],
)
def test_action_owned_local_collection_valid_indices_match_all_runtimes(
    tmp_path, operation, index, expected
):
    source = _access_source(operation, index, action=True)
    observations = _logical_runtimes(source)
    assert {name: value["stdout"] for name, value in observations.items()} == {
        "hosted": expected,
        "bytecode": expected,
        "kuro_vm": expected,
    }
    assert observations["hosted"]["error"] is None
    assert observations["bytecode"]["error"] is None
    assert not observations["kuro_vm"]["failed"]
    native = _native(source, tmp_path, "native-action-collection-bounds")
    assert (native.returncode, native.stdout, native.stderr) == (0, expected, "")


@pytest.mark.skipif(not LINUX_X86, reason="native executable coverage targets Linux x86_64")
@pytest.mark.parametrize("operation,index", [("get", -3), ("get", 2), ("set", -1), ("set", 2)])
def test_action_owned_local_collection_rejects_outside_logical_bounds(
    tmp_path, operation, index
):
    source = _access_source(operation, index, action=True)
    observations = _logical_runtimes(source)
    _assert_logical_failure(
        observations, native=_native(source, tmp_path, "native-action-collection-bounds")
    )


@pytest.mark.skipif(not LINUX_X86, reason="native executable coverage targets Linux x86_64")
def test_main_append_shrink_and_interleaved_owners_keep_independent_lengths(tmp_path):
    source = (
        "Items = 1, 2; Other = 7, 8, 9;\n"
        "Append 3 to Items;\n"
        "Get Items -1; Print @_.\n"
        "Items = 4, 5;\n"
        "Get Items -1; Print @_.\n"
        "Get Other -1; Print @_.\n"
        "Append 10 to Other;\n"
        "Get Items -1; Print @_.\n"
        "Get Other -1; Print @_.\n"
    )
    expected = "3\n5\n9\n5\n10\n"
    observations = _logical_runtimes(source)
    assert all(item["stdout"] == expected for item in observations.values())
    assert observations["hosted"]["error"] is None
    assert observations["bytecode"]["error"] is None
    assert not observations["kuro_vm"]["failed"]
    native = _native(source, tmp_path, "native-collection-owner-lengths")
    assert (native.returncode, native.stdout, native.stderr) == (0, expected, "")


def test_linux_action_collection_parameters_require_logical_length_metadata():
    for operation in ("get", "set"):
        if operation == "get":
            body = "Get Items Index; Return 0;\n"
        else:
            body = "Set Items Index to 9; Return 0;\n"
        source = (
            "Items = 1, 2;\n"
            "Action Touch Items: Integers, Index: Integers;\n"
            + body
            + "Done.\n"
        )
        compiled = _compile(source)
        with pytest.raises(NativeBackendError, match="logical length metadata"):
            emit_x86_64_linux(compiled.ir)


def test_arm64_main_and_action_guards_use_lengths_before_scaled_addressing():
    source = (
        "Items = 1, 2;\nAppend 3 to Items;\n"
        "Set Items 1 to 8; Get Items -1; Print @_.\n"
        "Action LocalAccess Index: Integers;\n"
        "LocalItems = 4; Append 5 to LocalItems; Set LocalItems Index to 9;\n"
        "Get LocalItems -1; Print @_. Return 0; Done.\n"
        "Call LocalAccess 0;\n"
    )
    assembly = emit_macos_arm64(_compile(source).ir)
    # Two SET and two GET instructions (one each in main and in the Action) are
    # checked against owner-specific logical lengths before offsets are scaled.
    assert assembly.count("b.hs L_kuro_collection_bounds") >= 4
    assert assembly.count("csel x1, x4, x1, lt") >= 2  # GET normalization only
    assert assembly.count("lsl x1, x1, #3") >= 4


def test_x86_macos_wrapper_keeps_linux_logical_length_guards():
    source = "Items = 1, 2; Set Items 0 to 3; Get Items -1; Print @_."
    assembly = emit_x86_64_macos(_compile(source).ir)
    assert "cmp %r8, %rcx" in assembly
    assert "cmovs %r9, %rcx" in assembly
    assert ".Lkuro_bounds" in assembly


@pytest.mark.parametrize("emitter", [emit_x86_64_linux, emit_macos_arm64], ids=["linux-x86", "macos-arm64"])
@pytest.mark.parametrize("form", ["parameter", "local-alias", "parameter-alias", "shadowed-buffer"])
@pytest.mark.parametrize("operation", ["Get Bag 0;", "Set Bag 0 to 9;", "Append 9 to Bag;"])
def test_pointer_only_action_collections_fail_closed(emitter, form, operation):
    # APPEND deliberately forces ARM's dynamic path. An alias APPEND is also
    # discovered as a static buffer by the old backend; that label is NOT proof
    # that the aliased pointer has the corresponding logical-length metadata.
    if form == "parameter":
        action = f"Action Touch Bag; {operation} Return 0; Done. Call Touch Items;"
    elif form == "local-alias":
        action = ("Action Touch; Alias = Items; " + operation.replace("Bag", "Alias")
                  + " Return 0; Done. Call Touch;")
    elif form == "parameter-alias":
        action = ("Action Touch Bag; Alias = Bag; " + operation.replace("Bag", "Alias")
                  + " Return 0; Done. Call Touch Items;")
    else:
        action = ("Action Touch Items; " + operation.replace("Bag", "Items")
                  + " Return 0; Done. Call Touch Others;")
    source = "Items = 11, 22; Others = 7, 8, 9; Append 33 to Items; " + action
    with pytest.raises(NativeBackendError, match="logical length metadata|captured collection|known element kind"):
        emitter(_compile(source).ir)


@pytest.mark.parametrize("emitter", [emit_x86_64_linux, emit_macos_arm64], ids=["linux-x86", "macos-arm64"])
@pytest.mark.parametrize("alias", [False, True], ids=["parameter", "parameter-alias"])
def test_pointer_only_action_length_cannot_become_strlen(emitter, alias):
    body = "Alias = Bag; Length Alias;" if alias else "Length Bag;"
    source = ("Items = 11, 22; Append 33 to Items; Action Touch Bag; "
              + body + " Return 0; Done. Call Touch Items;")
    with pytest.raises(NativeBackendError, match="logical length metadata|captured collection lengths"):
        emitter(_compile(source).ir)


@pytest.mark.parametrize("emitter", [emit_x86_64_linux, emit_macos_arm64], ids=["linux-x86", "macos-arm64"])
def test_collection_copy_cannot_borrow_a_static_alias_buffer_length(emitter):
    source = "Items = 11, 22; Alias = Items; Append 33 to Alias; Get Alias 0; Print @_."
    with pytest.raises(NativeBackendError, match="logical length metadata"):
        emitter(_compile(source).ir)


@pytest.mark.parametrize("index,expected", [(-2, "11"), (-1, "22")])
def test_arm64_constant_collection_reads_accept_negative_offsets(index, expected):
    assembly = emit_macos_arm64(_compile(f"Items = 11, 22; Get Items {index}; Print @_.").ir)
    assert f'.asciz "{expected}"' in assembly


@pytest.mark.parametrize("operation", ["Get Items -3;", "Get Items 2;", "Set Items -1 to 9;", "Set Items 2 to 9;"])
def test_arm64_invalid_constant_collection_access_retains_compile_rejection(operation):
    with pytest.raises(NativeBackendError, match="constant.*index"):
        emit_macos_arm64(_compile("Items = 11, 22; " + operation + " Print 0.").ir)


NATIVE_HOST = LINUX_X86 or (
    platform.system() == "Darwin"
    and platform.machine().lower() in {"arm64", "aarch64", "x86_64", "amd64"}
)


@pytest.mark.skipif(not NATIVE_HOST, reason="requires a supported native execution host")
@pytest.mark.parametrize(
    "operation,index,expected,returncode",
    [("get", -3, "11\n", 0), ("get", -1, "33\n", 0),
     ("get", -4, "", 1), ("get", 3, "", 1),
     ("set", -1, "", 1), ("set", 2, "99\n", 0)],
)
def test_native_host_action_global_collection_bounds(tmp_path, operation, index, expected, returncode):
    # APPEND selects actual dynamic ARM64 lowering rather than constant folding.
    body = ("Get Items Index; Print @_." if operation == "get" else
            "Set Items Index to 99; Get Items 2; Print @_.")
    source = ("Items = 11, 22; Append 33 to Items; "
              "Action Access Index: Integers; " + body
              + f" Return 0; Done. Call Access {index};")
    executable = tmp_path / "native-host-action-bounds"
    build_native(_compile(source).ir, executable)
    completed = subprocess.run([str(executable)], capture_output=True, text=True, timeout=15)
    assert (completed.returncode, completed.stdout, completed.stderr) == (returncode, expected, "")


@pytest.mark.parametrize("emitter", [emit_x86_64_linux, emit_macos_arm64], ids=["linux-x86", "macos-arm64"])
@pytest.mark.parametrize("alias_name", ["target", "__bag", "t0", "Alias"])
@pytest.mark.parametrize("operation", ["Get NAME 0;", "Set NAME 0 to 9;"])
def test_global_collection_alias_names_are_not_classified_by_prefix(emitter, alias_name, operation):
    # These are legal source variable names, not proof of IR temporary identity.
    # The review reproducer previously entered Text byte access and segfaulted.
    source = (f"Items = 11, 22; Append 33 to Items; {alias_name} = Items; "
              "Action ReadIt; " + operation.replace("NAME", alias_name)
              + " Return 0; Done. Call ReadIt;")
    with pytest.raises(NativeBackendError, match="logical length metadata|captured collection"):
        emitter(_compile(source).ir)


@pytest.mark.parametrize("emitter", [emit_x86_64_linux, emit_macos_arm64], ids=["linux-x86", "macos-arm64"])
@pytest.mark.parametrize("operation", ["Get Alias 0;", "Set Alias 0 to 9;"])
@pytest.mark.parametrize("reader_first", [False, True], ids=["maker-first", "reader-first"])
def test_collection_alias_created_in_an_action_is_rejected_across_actions(emitter, operation, reader_first):
    maker = "Action Make; Alias = Items; Return 0; Done. "
    reader = f"Action ReadIt; {operation} Return 0; Done. "
    source = ("Items = 11, 22; Append 33 to Items; " + maker + reader
              + "Call Make; Call ReadIt;")
    ir = _compile(source).ir
    if reader_first:
        # The frontend rejects a read before its source declaration. Reorder
        # already resolved Action bodies to check fixed-point scan order only.
        ir.functions = dict(reversed(list(ir.functions.items())))
    with pytest.raises(NativeBackendError, match="logical length metadata"):
        emitter(ir)
