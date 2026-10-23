"""Seeded helper compatibility witnesses, not natural full-history executions.

No helper is replaced. Signed crossing is computed with small runtime literals;
the separate reuse control injects -1 rather than simulating a complete cycle.
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
HistoryMode is Text;
Take user HistoryMode;
If HistoryMode is equal to "empty-churn";
    HistoryStep = 0;
    While HistoryStep is less than 8;
        Call VMResetCollection "Empty";
        Add 1 to HistoryStep;
    Done.
    Print VMNextCollectionId.
    Print VMCollectionCount.
    Print VMCollectionEntryCount.
    Call VMLengthCollection "Empty";
    Print @_.
Else;
    If HistoryMode is equal to "seeded-reuse";
        Call VMResetCollection "Original";
        VMAppendCollectionDisplay = "0007";
        Call VMAppendCollectionItem "Original", "old-raw";
        # Synthetic later state, NOT an execution of a full counter cycle.
        VMNextCollectionId = -1;
        Call VMResetCollection "Gap";
        Call VMFindCollection "Gap", 0;
        Print @_.
        Call VMResetCollection "Reused";
        Call VMLengthCollection "Reused";
        Print @_.
        Call VMGetCollectionItem "Reused", 0;
        Print @_.
        Print VMGetCollectionDisplay.
        VMSetCollectionDisplay = "changed-display";
        Call VMSetCollectionItem "Reused", 0, "changed-raw";
        Call VMGetCollectionItem "Original", 0;
        Print @_.
        Print VMGetCollectionDisplay.
        Call VMDeactivateCollection "Original";
        Call VMGetCollectionItem "Reused", -1;
        Print @_.
        Print VMGetCollectionDisplay.
        Print VMNextCollectionId.
        Print VMCollectionCount.
        Print VMCollectionEntryCount.
    Else;
        HistoryHalfBoundary = 1;
        HistoryBit = 0;
        While HistoryBit is less than 62;
            HistoryHalfBoundary = HistoryHalfBoundary * 2;
            Add 1 to HistoryBit;
        Done.
        VMNextCollectionId = HistoryHalfBoundary - 1;
        VMNextCollectionId = VMNextCollectionId + HistoryHalfBoundary;
        Call VMResetCollection "Source";
        If HistoryMode is equal to "reset-existing";
            VMAppendCollectionDisplay = "old-display";
            Call VMAppendCollectionItem "Source", "old-row";
            Call VMResetCollection "Source";
        Done.
        If HistoryMode is equal to "mark-active";
            HistoryBefore = VMNextCollectionId;
            Call VMMarkCollection "Source";
            If HistoryBefore is equal to VMNextCollectionId;
                Print "counter-unchanged".
            Done.
            Call VMDeactivateCollection "Source";
            If HistoryBefore is equal to VMNextCollectionId;
                Print "deactivate-unchanged".
            Done.
            Call VMResetCollection "Source";
        Else;
            If HistoryMode is equal to "mark-retry";
                Call VMMarkCollection "Destination";
                HistoryBefore = VMNextCollectionId;
                Call VMMarkCollection "Destination";
                If HistoryBefore is equal to VMNextCollectionId;
                    Print "counter-unchanged".
                Else;
                    Print "counter-advanced".
                Done.
            Else;
                If HistoryMode is equal to "copy-nonempty";
                    VMAppendCollectionDisplay = "001.50";
                    Call VMAppendCollectionItem "Source", "source-raw";
                Done.
                If HistoryMode is not equal to "reset-existing";
                    Call VMCopyCollection "Source", "Destination";
                Done.
            Done.
        Done.
        If HistoryMode is equal to "mark-active" or HistoryMode is equal to "reset-existing";
            Call VMFindCollection "Source", 0;
        Else;
            Call VMFindCollection "Destination", 0;
        Done.
        Print @_.
        Print VMCollectionCount.
        Print VMCollectionEntryCount.
        Print VMFailed.
        If VMAppendCollectionDisplay is equal to "";
            Print "append-display-cleared".
        Else;
            Print "append-display-not-cleared".
        Done.
        If HistoryMode is equal to "copy-nonempty";
            # Only render a known-valid raw Text, never failed Get's zero.
            Call VMGetCollectionItem "Source", 0;
            Print @_.
            Print VMGetCollectionDisplay.
            Print VMFailed.
        Done.
        If HistoryMode is equal to "reset-existing";
            Call VMLengthCollection "Source";
            Print @_.
            Print VMFailed.
            # Physical history remains even though the name no longer selects it.
            Get VMCollectionItems 0;
            Print @_.
            Get VMCollectionItemDisplay 0;
            Print @_.
        Done.
    Done.
Done.
'''


# Each expected trace is literal and backend-specific, not computed by a model
# sharing the helper's transitions. Scratch display is compared, not rendered.
CASES = [
    pytest.param("empty-churn", "8\n1\n0\n0\n", "8\n1\n0\n0\n", id="empty-resets-spend-no-rows"),
    pytest.param("mark-active", "counter-unchanged\ndeactivate-unchanged\n0\n1\n0\n0\nappend-display-cleared\n",
                 "counter-unchanged\ndeactivate-unchanged\n-1\n1\n0\n0\nappend-display-cleared\n", id="active-mark-deactivate-reset"),
    pytest.param("mark-retry", "counter-unchanged\n1\n2\n0\n0\nappend-display-cleared\n",
                 "counter-advanced\n-1\n2\n0\n0\nappend-display-cleared\n", id="negative-mark-retries-without-new-slot"),
    pytest.param("copy-empty", "1\n2\n0\n0\nappend-display-cleared\n", "-1\n2\n0\n0\nappend-display-cleared\n", id="empty-copy-publishes-without-append"),
    pytest.param("copy-nonempty", "1\n2\n2\n0\nappend-display-cleared\nsource-raw\n001.50\n0\n",
                 "-1\n2\n1\n1\nappend-display-cleared\nsource-raw\n001.50\n1\n", id="nonempty-copy-fails-after-destination-reset"),
    pytest.param("reset-existing", "0\n1\n1\n0\nappend-display-cleared\n0\n0\nold-row\nold-display\n",
                 "-1\n1\n1\n0\nappend-display-cleared\n0\n1\nold-row\nold-display\n", id="existing-reset-hides-but-retains-old-row"),
    pytest.param("seeded-reuse", "-1\n1\nold-raw\n0007\nchanged-raw\nchanged-display\nchanged-raw\nchanged-display\n1\n3\n1\n",
                 "-1\n1\nold-raw\n0007\nchanged-raw\nchanged-display\nchanged-raw\nchanged-display\n1\n3\n1\n", id="synthetic-id-reuse-exposes-historical-row-alias"),
]


@pytest.mark.parametrize("mode,hosted,native", CASES)
def test_hosted_history_compatibility(mode, hosted, native):
    result = run_source(_source(), input_fn=lambda _prompt: mode)
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    assert result.stdout == hosted
    env = result.interpreter.env
    if mode == "seeded-reuse":
        assert env["VMCollectionIds"][:3] == [-1, -1, 0]
        assert env["VMCollectionOwners"][0] == 0
        assert env["VMFailed"] == 0
    elif mode != "empty-churn":
        assert env["VMNextCollectionId"] == 2**63 + 1


@pytest.fixture(scope="module")
def history_image(tmp_path_factory):
    if not LINUX_X86:
        pytest.skip("requires executable Linux x86-64 helper image")
    compiled = compile_source(_source())
    assert compiled.ok, compiled.diags.render_all()
    image = tmp_path_factory.mktemp("generation-history") / "probe"
    build_native(compiled.ir, image, target="x86_64-linux")
    return image


@pytest.mark.parametrize("mode,hosted,native", CASES)
def test_native_history_compatibility(mode, hosted, native, history_image, tmp_path):
    result = subprocess.run([str(history_image)], input=mode, text=True,
                            capture_output=True, cwd=tmp_path, timeout=60, check=False)
    assert (result.returncode, result.stdout, result.stderr) == (0, native, "")
