"""Fixed 65,600-row storage is exclusive to the native artifact launcher."""
from __future__ import annotations

import copy
import inspect
import platform
import shutil
import subprocess
from dataclasses import fields

import pytest

from compiler import native
from compiler.native import NativeBackendError, NATIVE_COLLECTION_CAPACITY
from compiler.pipeline import compile_source
from compiler.self_host import build_native_artifact_launcher, native_artifact_launcher_source

LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}
LEDGER_COLUMNS = (
    "VMCollectionOwners", "VMCollectionItems", "VMCollectionItemDisplay",
)


BOUNDARY_DRIVER = r'''
Call VMResetCollection "CapacityProbe";
VMAppendCollectionDisplay = "display-zero";
Call VMAppendCollectionItem "CapacityProbe", "raw-zero";
VMAppendCollectionDisplay = "display-one";
Call VMAppendCollectionItem "CapacityProbe", "raw-one";
VMAppendCollectionDisplay = "display-two";
Call VMAppendCollectionItem "CapacityProbe", "raw-two";
CapacityProbePos = 3;
While CapacityProbePos is less than 65600;
    If CapacityProbePos is equal to 65599;
        VMAppendCollectionDisplay = "display-final";
        Call VMAppendCollectionItem "CapacityProbe", "raw-final";
    Else;
        VMAppendCollectionDisplay = "display-other";
        Call VMAppendCollectionItem "CapacityProbe", "raw-other";
    Done.
    Add 1 to CapacityProbePos;
Done.
Print VMCollectionEntryCount.
Get VMCollectionOwners 0; Print @_.
Get VMCollectionItems 0; Print @_.
Get VMCollectionItemDisplay 0; Print @_.
Get VMCollectionOwners 1; Print @_.
Get VMCollectionItems 1; Print @_.
Get VMCollectionItemDisplay 1; Print @_.
Get VMCollectionOwners 2; Print @_.
Get VMCollectionItems 2; Print @_.
Get VMCollectionItemDisplay 2; Print @_.
Get VMCollectionOwners 65599; Print @_.
Get VMCollectionItems 65599; Print @_.
Get VMCollectionItemDisplay 65599; Print @_.
Print "before-overflow".
VMAppendCollectionDisplay = "display-overflow";
Call VMAppendCollectionItem "CapacityProbe", "raw-overflow";
Print "after-overflow".
'''


def _compile(source: str):
    result = compile_source(source)
    assert result.ok, result.diags.render_all()
    return result.ir


def _native_collection_names(ir, *, arm64: bool = False) -> list[str]:
    names: set[str] = set()
    bodies = [ir.main, *(function.body for function in ir.functions.values())]
    for body_index, body in enumerate(bodies):
        for item in body:
            if item.op == "APPEND" and item.args:
                names.add(item.args[0])
            elif item.op == "STORE_LIST" and len(item.args) > 1 and len(item.args[1]) > 1:
                # The ARM64 dynamic emitter collects initializers in main only;
                # x86-64 collects them in main and Action bodies.
                if not arm64 or body_index == 0:
                    names.add(item.args[0])
    return sorted(names)


@pytest.fixture(scope="module")
def launcher_ir():
    return _compile(native_artifact_launcher_source())


@pytest.fixture(scope="module")
def launcher_profile(launcher_ir):
    return native._artifact_launcher_storage_profile(launcher_ir)


def test_fixed_profile_is_private_and_bound_to_one_admission_callsite(launcher_ir, launcher_profile):
    append = launcher_ir.functions["VMAppendCollectionItem"]
    calls = [
        item for item in append.body
        if item.op == "CALL" and item.args and item.args[0] == "__KuroAdmitRow"
    ]
    selected = [item for item in calls if id(item) in launcher_profile.admission_call_ids]
    assert len(calls) == len(selected) == 1
    assert launcher_profile.ledger_collections == frozenset(LEDGER_COLUMNS)
    assert native._row_admission_capacity(selected[0], launcher_profile) == 65_600
    assert native._row_admission_capacity(object(), launcher_profile) == NATIVE_COLLECTION_CAPACITY
    assert NATIVE_COLLECTION_CAPACITY == 65_536
    assert "capacity" not in {field.name for field in fields(launcher_profile)}

    for public_builder in (native.build_native, build_native_artifact_launcher):
        assert "vm_ledger_capacity" not in inspect.signature(public_builder).parameters
    assert "ir" not in inspect.signature(build_native_artifact_launcher).parameters
    assert not hasattr(native, "build_native_artifact_launcher")
    for public_emitter in (native.emit_x86_64_linux, native.emit_x86_64_macos, native.emit_macos_arm64):
        assert "vm_ledger_capacity" not in inspect.signature(public_emitter).parameters
        assert "launcher_profile" not in inspect.signature(public_emitter).parameters
    with pytest.raises(TypeError):
        native.build_native(launcher_ir, "/tmp/not-built", vm_ledger_capacity=65_600)
    with pytest.raises(TypeError):
        build_native_artifact_launcher("/tmp/not-built", vm_ledger_capacity=65_600)


@pytest.mark.parametrize("entrypoint", ["x86-linux", "x86-macos", "arm64", "builder"])
def test_created_profile_cannot_be_transferred_to_another_ir_at_any_backend_entry(
    entrypoint, launcher_ir, launcher_profile, tmp_path
):
    other_ir = copy.deepcopy(launcher_ir)
    assert other_ir == launcher_ir
    assert other_ir is not launcher_ir

    with pytest.raises(NativeBackendError, match="cannot be transferred"):
        if entrypoint == "x86-linux":
            native._emit_x86_64_linux(other_ir, launcher_profile=launcher_profile)
        elif entrypoint == "x86-macos":
            native._emit_x86_64_macos(other_ir, launcher_profile=launcher_profile)
        elif entrypoint == "arm64":
            native._emit_macos_arm64(other_ir, launcher_profile=launcher_profile)
        else:
            native._build_native(
                other_ir, tmp_path / "must-not-build", target="x86_64-linux",
                launcher_profile=launcher_profile,
            )
    assert not (tmp_path / "must-not-build").exists()

    # The same structurally identical IR gets only generic storage when no
    # launcher-bound profile is supplied through the public emitter.
    x86 = native.emit_x86_64_linux(other_ir)
    arm = native.emit_macos_arm64(other_ir)
    assert ".zero 524800" not in x86 and "cmp $65600," not in x86
    assert "cmp $65536," in x86
    assert ",524800,3" not in arm
    assert "cmp x0, #16, lsl #12" in arm


@pytest.mark.parametrize("mutation", ["column-alias", "counter-alias", "count-not-last", "action-alias"])
def test_launcher_profile_rejects_protocol_aliases_and_shape_changes(launcher_ir, mutation):
    changed = copy.deepcopy(launcher_ir)
    if mutation == "action-alias":
        function = changed.functions.pop("VMAppendCollectionItem")
        function.name = "VMAppendCollectionItemAlias"
        changed.functions[function.name] = function
    else:
        function = changed.functions["VMAppendCollectionItem"]
        call_index = next(
            index for index, item in enumerate(function.body)
            if item.op == "CALL" and item.args and item.args[0] == "__KuroAdmitRow"
        )
        if mutation == "column-alias":
            append = next(item for item in function.body[call_index + 1:] if item.op == "APPEND")
            append.args = (append.args[0] + "Alias", *append.args[1:])
        elif mutation == "counter-alias":
            load = function.body[call_index - 1]
            load.args = ("OtherEntryCount",)
        elif mutation == "count-not-last":
            increment_index = next(
                index for index, item in enumerate(function.body)
                if item.op == "ADD" and item.args and item.args[0] == "VMCollectionEntryCount"
            )
            increment = function.body.pop(increment_index)
            function.body.insert(call_index + 1, increment)
    with pytest.raises(NativeBackendError):
        native._derive_artifact_launcher_storage_profile(changed)


def test_generic_build_with_ledger_names_and_action_name_collision_stays_at_65536():
    source = '''
VMCollectionOwners is Integers;
VMCollectionItems is Text;
VMCollectionItemDisplay is Text;
VMCollectionEntryCount = 0;
Action VMAppendCollectionItem Value: Text;
    Call __KuroAdmitRow VMCollectionEntryCount;
    Append 0 to VMCollectionOwners;
    Append Value to VMCollectionItems;
    Append Value to VMCollectionItemDisplay;
    Add 1 to VMCollectionEntryCount;
Done.
Call VMAppendCollectionItem "raw";
'''
    ir = _compile(source)
    with pytest.raises(NativeBackendError):
        native._artifact_launcher_storage_profile(ir)
    x86 = native.emit_x86_64_linux(ir)
    arm = native.emit_macos_arm64(ir)

    assert "cmp $65600," not in x86
    assert "cmp $65536," in x86
    assert ".zero 524800" not in x86
    assert "cmp x0, #16, lsl #12" in arm
    assert ",524800,3" not in arm

    for index, name in enumerate(_native_collection_names(ir)):
        assert f".Lkuro_collection_{index}: .zero 524288" in x86, name
        assert f".Lkuro_collection_item_len_{index}: .zero 524288" in x86, name
        assert f".zerofill __DATA,__bss,_kuro_collection_{index},524288,3" in arm, name


def test_profiled_launcher_allocations_and_guards_match_one_fixed_ledger_layout(launcher_ir, launcher_profile, tmp_path):
    x86 = native._emit_x86_64_linux(launcher_ir, launcher_profile=launcher_profile)
    arm = native._emit_macos_arm64(launcher_ir, launcher_profile=launcher_profile)
    x86_names = _native_collection_names(launcher_ir)
    arm_names = _native_collection_names(launcher_ir, arm64=True)

    for index, name in enumerate(x86_names):
        expected_bytes = 65_600 * 8 if name in launcher_profile.ledger_collections else 65_536 * 8
        assert f".Lkuro_collection_{index}: .zero {expected_bytes}" in x86, name
        assert f".Lkuro_collection_item_len_{index}: .zero {expected_bytes}" in x86, name
    assert x86.count(".zero 524800") == 6
    assert x86.count("cmp $65600, %rcx") == 3  # the three column append guards
    assert x86.count("cmp $65600, %rax") == 1  # their one pre-write admission guard
    assert "cmp $65536, %rax" in x86  # unrelated collection/admission guards remain ordinary

    for index, name in enumerate(arm_names):
        expected_bytes = 65_600 * 8 if name in launcher_profile.ledger_collections else 65_536 * 8
        assert f".zerofill __DATA,__bss,_kuro_collection_{index},{expected_bytes},3" in arm, name
    assert arm.count(",524800,3") == 3
    assert "movz x4, #64\n    movk x4, #1, lsl #16\n    cmp x0, x4" in arm
    assert "cmp x0, #16, lsl #12" in arm

    clang = shutil.which("clang")
    if clang is None:
        pytest.skip("cross-assembly assertion requires Clang")
    assembly = tmp_path / "launcher-arm64.s"
    obj = tmp_path / "launcher-arm64.o"
    assembly.write_text(arm, encoding="utf-8")
    assembled = subprocess.run(
        [clang, "-target", "arm64-apple-macos11", "-c", str(assembly), "-o", str(obj)],
        capture_output=True, text=True, timeout=90,
    )
    assert assembled.returncode == 0, assembled.stderr
    assert obj.is_file()


@pytest.fixture(scope="module")
def launcher_boundary_image(tmp_path_factory, launcher_ir, launcher_profile):
    # Add a test driver after the real launcher source so the image exercises its
    # actual three-column VM append helper and the dedicated launcher profile.
    ir = _compile(native_artifact_launcher_source() + BOUNDARY_DRIVER)
    assert ir.functions == launcher_ir.functions
    # The canonical functions retain their profile-bound admission callsite;
    # only the test's top-level driver is added after RuntimeMain.
    ir.functions = launcher_ir.functions
    with pytest.raises(NativeBackendError):
        native._artifact_launcher_storage_profile(ir)
    # This private helper fixture models a launcher image plus test-only main
    # instructions. Bind a separate shape-checked profile to that exact IR;
    # production selection remains exclusively in the canonical source wrapper.
    boundary_profile = native._derive_artifact_launcher_storage_profile(ir)
    image = tmp_path_factory.mktemp("launcher-vm-ledger-boundary") / "kuro-bytecode"
    native._build_native(
        ir, image, target="x86_64-linux", launcher_profile=boundary_profile
    )
    return image


@pytest.mark.skipif(not LINUX_X86, reason="runtime boundary witness requires Linux x86-64")
def test_65600th_row_reads_all_columns_and_65601st_append_fails_before_marker(launcher_boundary_image):
    result = subprocess.run(
        [str(launcher_boundary_image)],
        input="kuro.bytecode/1\nBC_CONST_TEXT\nlauncher-ready\nBC_PRINT\n",
        capture_output=True, text=True, timeout=90, check=False,
    )
    expected = (
        "launcher-ready\n65600\n"
        "0\nraw-zero\ndisplay-zero\n"
        "0\nraw-one\ndisplay-one\n"
        "0\nraw-two\ndisplay-two\n"
        "0\nraw-final\ndisplay-final\n"
        "before-overflow\n"
    )
    assert (result.returncode, result.stdout, result.stderr) == (1, expected, "")
    assert "after-overflow" not in result.stdout


@pytest.mark.skipif(not LINUX_X86, reason="generic fixed-capacity control requires Linux x86-64")
def test_generic_collection_accepts_65536th_row_and_rejects_65537th(tmp_path):
    source = '''
Rows is Integers;
Position = 0;
While Position is less than 65536;
    Append Position to Rows;
    Add 1 to Position;
Done.
Print Position.
Print "before-generic-overflow".
Append Position to Rows;
Print "after-generic-overflow".
'''
    ir = _compile(source)
    image = tmp_path / "generic-collection-boundary"
    native.build_native(ir, image, target="x86_64-linux")
    result = subprocess.run([str(image)], capture_output=True, text=True, timeout=30, check=False)
    assert (result.returncode, result.stdout, result.stderr) == (
        1, "65536\nbefore-generic-overflow\n", "",
    )
