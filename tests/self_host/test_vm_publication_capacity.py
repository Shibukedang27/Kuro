"""Publication capacity witnesses, not a COW implementation or reduced-limit VM.

Native probes call unchanged production helpers at the real 65,536-row limit.
They observe fail-stop output, not postmortem atomicity or recoverable VM failure.
Portable probes use small ledgers to pin the same logical transitions; the hosted
interpreter does not inherit the native emitter's fixed buffer capacity.
"""
from __future__ import annotations

from pathlib import Path
import platform
import subprocess

import pytest

from compiler.native import NATIVE_COLLECTION_CAPACITY, build_native
from compiler.pipeline import compile_source, run_source


ROOT = Path(__file__).resolve().parents[2]
LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}


def _source(filler: int) -> str:
    # Retain the complete production VM, including its harmless standalone demo.
    # The demo does not allocate interpreted collection rows. No production helper,
    # capacity, emitter or assembly is patched by this harness.
    vm = (ROOT / "self_host/vm.kuro").read_text(encoding="utf-8")
    return vm + f'''
CapacityMode is Text;
Take user CapacityMode;
Call VMResetCollection "Source";
VMAppendCollectionDisplay = "001.50";
Call VMAppendCollectionItem "Source", "raw-one";
Call VMAppendCollectionItem "Source", "raw-two";
Call VMResetCollection "Filler";
CapacityIndex = 0;
While CapacityIndex is less than {filler};
    Call VMAppendCollectionItem "Filler", "pad";
    Add 1 to CapacityIndex;
Done.
If CapacityMode is equal to "copy-one-spare";
    Call VMAppendCollectionItem "Filler", "pad";
Done.
If CapacityMode is not equal to "copy-two-spare" and CapacityMode is not equal to "copy-one-spare";
    Call VMAppendCollectionItem "Filler", "pad";
    Call VMAppendCollectionItem "Filler", "pad";
Done.
Print "before".
Print VMCollectionEntryCount.
If CapacityMode is equal to "self-copy-full";
    Call VMCopyCollection "Source", "Source";
Else;
    If CapacityMode is equal to "set-full";
        VMSetCollectionDisplay = "009.00";
        Call VMSetCollectionItem "Source", 0, "changed";
    Else;
        If CapacityMode is equal to "reset-append-full";
            Call VMResetCollection "Source";
            Call VMLengthCollection "Source";
            Print @_.
            Call VMAppendCollectionItem "Source", "overflow";
        Else;
            If CapacityMode is equal to "deactivate-append-full";
                Call VMDeactivateCollection "Source";
                Call VMFindCollection "Source", 0;
                Print @_.
                Call VMAppendCollectionItem "Filler", "overflow";
            Else;
                If CapacityMode is equal to "empty-copy-full";
                    Call VMResetCollection "Empty";
                    Call VMCopyCollection "Empty", "Source";
                Else;
                    Call VMCopyCollection "Source", "Published";
                Done.
            Done.
        Done.
    Done.
Done.
Print "after".
Print VMCollectionEntryCount.
Length VMCollectionItems;
Print @_.
Length VMCollectionItemDisplay;
Print @_.
Print VMFailed.
If CapacityMode is equal to "copy-two-spare" or CapacityMode is equal to "copy-one-spare" or CapacityMode is equal to "copy-full";
    Call VMLengthCollection "Published";
    Print @_.
    Call VMGetCollectionItem "Published", 0;
    Print @_.
    Print VMGetCollectionDisplay.
Else;
    If CapacityMode is equal to "deactivate-append-full";
        Call VMLengthCollection "Filler";
        Print @_.
    Else;
        Call VMLengthCollection "Source";
        Print @_.
        If CapacityMode is equal to "self-copy-full" or CapacityMode is equal to "set-full";
            Call VMGetCollectionItem "Source", 0;
            Print @_.
            Print VMGetCollectionDisplay.
        Done.
    Done.
Done.
'''


MODES = (
    "copy-two-spare", "copy-one-spare", "copy-full", "self-copy-full",
    "set-full", "reset-append-full", "deactivate-append-full", "empty-copy-full",
)


def _expected(mode: str, filler: int, *, native: bool) -> tuple[int, str]:
    before = filler + (2 if mode == "copy-two-spare" else 3 if mode == "copy-one-spare" else 4)
    prefix = f"before\n{before}\n"
    if mode == "reset-append-full":
        prefix += "0\n"
    elif mode == "deactivate-append-full":
        prefix += "-1\n"
    if native and mode in {"copy-one-spare", "copy-full", "reset-append-full", "deactivate-append-full"}:
        return 1, prefix
    after = before + (2 if mode.startswith("copy-") else 1 if "append" in mode else 0)
    suffix = f"after\n{after}\n{after}\n{after}\n0\n"
    if mode.startswith("copy-") or mode == "self-copy-full":
        suffix += "2\nraw-one\n001.50\n"
    elif mode == "set-full":
        suffix += "2\nchanged\n009.00\n"
    elif mode == "reset-append-full":
        suffix += "1\n"
    elif mode == "deactivate-append-full":
        suffix += f"{filler + 3}\n"
    else:
        suffix += "0\n"
    return 0, prefix + suffix


@pytest.mark.parametrize("mode", MODES)
def test_small_hosted_publication_transitions(mode):
    # A deliberate target distinction: crossing this small number is NOT an
    # emulated capacity failure. Hosted lists have no native 65,536-row limit.
    _, expected = _expected(mode, 3, native=False)
    result = run_source(_source(3), input_fn=lambda _prompt: mode)
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    assert result.stdout == expected
    assert result.interpreter.env["VMFailed"] == 0
    env = result.interpreter.env
    assert all(len(env[column]) == env["VMCollectionEntryCount"] for column in (
        "VMCollectionOwners", "VMCollectionItems", "VMCollectionItemDisplay",
    ))


@pytest.fixture(scope="module")
def capacity_image(tmp_path_factory):
    if not LINUX_X86:
        pytest.skip("real-capacity executable probes require Linux x86-64")
    assert NATIVE_COLLECTION_CAPACITY == 65_536
    compiled = compile_source(_source(NATIVE_COLLECTION_CAPACITY - 4))
    assert compiled.ok, compiled.diags.render_all()
    image = tmp_path_factory.mktemp("publication-capacity") / "probe"
    build_native(compiled.ir, image, target="x86_64-linux")
    return image


@pytest.mark.parametrize("mode", MODES)
def test_real_native_publication_capacity(mode, capacity_image, tmp_path):
    status, expected = _expected(mode, NATIVE_COLLECTION_CAPACITY - 4, native=True)
    result = subprocess.run(
        [str(capacity_image)], input=mode.encode(), capture_output=True,
        cwd=tmp_path, timeout=60, check=False,
    )
    assert (result.returncode, result.stdout, result.stderr) == (status, expected.encode(), b"")
