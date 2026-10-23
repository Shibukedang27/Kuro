"""Unchanged production row/borrow witnesses, not a moving-storage proof.

Dynamic Text pairs outlive an in-place cell overwrite or retained-row reset.
No rows or Text allocations are reclaimed by this test or production helpers.
"""
from pathlib import Path
import platform
import subprocess

import pytest

from compiler.native import build_native
from compiler.pipeline import compile_source, run_source

ROOT = Path(__file__).resolve().parents[2]
LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}


def _source():
    return (ROOT / "self_host/vm.kuro").read_text(encoding="utf-8") + '''
ReplacementMode is Text;
Take user ReplacementMode;
ReplacementOld = "raw-" + ReplacementMode;
ReplacementDisplay = "display-" + ReplacementMode;
Call VMResetCollection "Source";
VMAppendCollectionDisplay = ReplacementDisplay;
Call VMAppendCollectionItem "Source", ReplacementOld;
VMAppendCollectionDisplay = "tail-display";
Call VMAppendCollectionItem "Source", "tail-raw";
Call VMCopyCollection "Source", "Snapshot";
# Copy traverses its newly appended rows too, but their owner does not match.
If VMCopyCollection_Pos is equal to 4;
    Print "copy-scan-four".
Done.
Call VMGetCollectionItem "Source", 0;
ReplacementCaptured = @_;
ReplacementCapturedDisplay = VMGetCollectionDisplay;
ReplacementNew = ReplacementMode + "-changed";
ReplacementNewDisplay = ReplacementMode + "-new-display";
If ReplacementMode is equal to "set";
    VMSetCollectionDisplay = ReplacementNewDisplay;
    Call VMSetCollectionItem "Source", 0, ReplacementNew;
Else;
    If ReplacementMode is equal to "failed-set";
        VMSetCollectionDisplay = ReplacementNewDisplay;
        Call VMSetCollectionItem "Source", 2, ReplacementNew;
    Else;
        If ReplacementMode is equal to "self-copy";
            Call VMCopyCollection "Source", "Source";
        Else;
            If ReplacementMode is equal to "deactivate-reset";
                Call VMDeactivateCollection "Source";
            Done.
            Call VMResetCollection "Source";
            VMAppendCollectionDisplay = ReplacementNewDisplay;
            Call VMAppendCollectionItem "Source", ReplacementNew;
        Done.
    Done.
Done.
# Allocate later dynamic Text without retaining earlier noise results. This is
# bounded arena churn, not forced collection, arena exhaustion, or relocation.
ReplacementStep = 0;
While ReplacementStep is less than 64;
    ReplacementNoise = ReplacementMode + "-noise";
    Add 1 to ReplacementStep;
Done.
Print ReplacementCaptured.
Print ReplacementCapturedDisplay.
Call VMGetCollectionItem "Source", 0;
Print @_.
Print VMGetCollectionDisplay.
Call VMGetCollectionItem "Snapshot", 0;
Print @_.
Print VMGetCollectionDisplay.
Get VMCollectionItems 0;
Print @_.
Get VMCollectionItemDisplay 0;
Print @_.
Call VMLengthCollection "Source";
Print @_.
If VMLengthCollection_Pos is equal to VMCollectionEntryCount;
    Print "length-scanned-all-rows".
Done.
Print VMCollectionEntryCount.
Print VMNextCollectionId.
Print VMCollectionCount.
Print VMFailed.
If VMSetCollectionDisplay is equal to "";
    Print "set-display-cleared".
Done.
'''


# Literal state/trace expectations are independent of a proposed replacement.
CASES = [
    pytest.param("set", "copy-scan-four\nraw-set\ndisplay-set\nset-changed\nset-new-display\nraw-set\ndisplay-set\nset-changed\nset-new-display\n2\nlength-scanned-all-rows\n4\n2\n2\n0\nset-display-cleared\n", id="overwrite-row-keeps-captured-pair-and-eager-snapshot"),
    pytest.param("reset", "copy-scan-four\nraw-reset\ndisplay-reset\nreset-changed\nreset-new-display\nraw-reset\ndisplay-reset\nraw-reset\ndisplay-reset\n1\nlength-scanned-all-rows\n5\n3\n2\n0\nset-display-cleared\n", id="reset-retains-old-physical-row-and-captured-pair"),
    pytest.param("deactivate-reset", "copy-scan-four\nraw-deactivate-reset\ndisplay-deactivate-reset\ndeactivate-reset-changed\ndeactivate-reset-new-display\nraw-deactivate-reset\ndisplay-deactivate-reset\nraw-deactivate-reset\ndisplay-deactivate-reset\n1\nlength-scanned-all-rows\n5\n3\n2\n0\nset-display-cleared\n", id="deactivation-does-not-reclaim-row-or-text"),
    pytest.param("failed-set", "copy-scan-four\nraw-failed-set\ndisplay-failed-set\nraw-failed-set\ndisplay-failed-set\nraw-failed-set\ndisplay-failed-set\nraw-failed-set\ndisplay-failed-set\n2\nlength-scanned-all-rows\n4\n2\n2\n1\nset-display-cleared\n", id="failed-set-does-not-publish-either-cell-and-failure-is-sticky"),
    pytest.param("self-copy", "copy-scan-four\nraw-self-copy\ndisplay-self-copy\nraw-self-copy\ndisplay-self-copy\nraw-self-copy\ndisplay-self-copy\nraw-self-copy\ndisplay-self-copy\n2\nlength-scanned-all-rows\n4\n2\n2\n0\nset-display-cleared\n", id="self-copy-debits-neither-rows-nor-generations"),
]


@pytest.mark.parametrize("mode,expected", CASES)
def test_row_replacement_lifetime_hosted(mode, expected):
    result = run_source(_source(), input_fn=lambda _prompt: mode)
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    assert result.stdout == expected
    env = result.interpreter.env
    assert env["VMCollectionOwners"][:4] == [0, 0, 1, 1]
    assert env["VMCollectionIds"][:2] == ([2, 1] if mode in {"reset", "deactivate-reset"} else [0, 1])
    first_raw = mode + "-changed" if mode == "set" else "raw-" + mode
    first_display = mode + "-new-display" if mode == "set" else "display-" + mode
    assert env["VMCollectionItems"][:4] == [first_raw, "tail-raw", "raw-" + mode, "tail-raw"]
    assert env["VMCollectionItemDisplay"][:4] == [first_display, "tail-display", "display-" + mode, "tail-display"]
    if mode in {"reset", "deactivate-reset"}:
        assert env["VMCollectionOwners"][4] == 2
        assert env["VMCollectionItems"][4] == mode + "-changed"
        assert env["VMCollectionItemDisplay"][4] == mode + "-new-display"
    assert env["ReplacementCaptured"] == "raw-" + mode
    assert env["ReplacementCapturedDisplay"] == "display-" + mode


@pytest.fixture(scope="module")
def replacement_image(tmp_path_factory):
    if not LINUX_X86:
        pytest.skip("requires executable Linux x86-64 helper image")
    compiled = compile_source(_source())
    assert compiled.ok, compiled.diags.render_all()
    image = tmp_path_factory.mktemp("row-replacement") / "probe"
    build_native(compiled.ir, image, target="x86_64-linux")
    return image


@pytest.mark.parametrize("mode,expected", CASES)
def test_row_replacement_lifetime_native(mode, expected, replacement_image, tmp_path):
    result = subprocess.run([str(replacement_image)], input=mode, text=True,
                            capture_output=True, cwd=tmp_path, timeout=60, check=False)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")
