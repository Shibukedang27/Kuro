"""Behavioral witnesses for VM collection generation and append-only row accounting.

These tests exercise the authored helpers through the hosted interpreter. They
pin observable transitions; they do not model capacity failure or prove native
storage atomicity, concurrency, or unbounded-ID safety.
"""
from __future__ import annotations

from pathlib import Path

from compiler.pipeline import run_source


ROOT = Path(__file__).resolve().parents[2]


def _run_helpers(body: str):
    vm = (ROOT / "self_host" / "vm.kuro").read_text(encoding="utf-8")
    result = run_source(vm + "\n" + body)
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    return result.interpreter.env


def _collection_id(env, name: str) -> int:
    names = env["VMCollectionNames"]
    for index in range(env["VMCollectionCount"]):
        if names[index] == name:
            return env["VMCollectionIds"][index]
    raise AssertionError(f"no collection slot for {name!r}")


def test_reset_deactivate_and_reactivation_advance_generations_not_rows():
    env = _run_helpers('''
Call VMResetCollection "Ledger";
VMAppendCollectionDisplay = "first-display";
Call VMAppendCollectionItem "Ledger", "first-raw";
Call VMResetCollection "Ledger";
VMAppendCollectionDisplay = "second-display";
Call VMAppendCollectionItem "Ledger", "second-raw";
Call VMDeactivateCollection "Ledger";
Call VMMarkCollection "Ledger";
VMAppendCollectionDisplay = "third-display";
Call VMAppendCollectionItem "Ledger", "third-raw";
Call VMMarkCollection "Ledger";
''')

    assert env["VMFailed"] == 0
    assert env["VMNextCollectionId"] == 3
    assert _collection_id(env, "Ledger") == 2
    assert env["VMCollectionEntryCount"] == 3
    assert env["VMCollectionOwners"][:3] == [0, 1, 2]
    assert env["VMCollectionItems"][:3] == ["first-raw", "second-raw", "third-raw"]
    assert env["VMCollectionItemDisplay"][:3] == [
        "first-display", "second-display", "third-display",
    ]


def test_sets_do_not_debit_rows_and_invalid_set_failure_is_sticky():
    env = _run_helpers('''
Call VMResetCollection "SetTarget";
VMAppendCollectionDisplay = "001.50";
Call VMAppendCollectionItem "SetTarget", "1.5";
VMSetCollectionDisplay = "009.00";
Call VMSetCollectionItem "SetTarget", 0, "9";
VMSetCollectionDisplay = "invalid-write";
Call VMSetCollectionItem "SetTarget", 7, "missing-index";
VMFailedAfterInvalidSet = VMFailed;
Get VMCollectionItems 0;
ValueAfterInvalidSet = @_;
Get VMCollectionItemDisplay 0;
DisplayAfterInvalidSet = @_;
VMSetCollectionDisplay = "010.00";
Call VMSetCollectionItem "SetTarget", 0, "10";
VMFailedAfterValidSet = VMFailed;
''')

    assert env["VMCollectionEntryCount"] == 1
    assert env["VMCollectionOwners"][:1] == [0]
    assert env["VMCollectionItems"][:1] == ["10"]
    assert env["VMCollectionItemDisplay"][:1] == ["010.00"]
    assert env["VMFailedAfterInvalidSet"] == 1
    assert (env["ValueAfterInvalidSet"], env["DisplayAfterInvalidSet"]) == ("9", "009.00")
    assert env["VMFailedAfterValidSet"] == 1  # helper failures are sticky
    assert env["VMFailed"] == 1


def test_eager_copies_get_fresh_generations_and_retain_raw_display_snapshots():
    env = _run_helpers('''
Call VMResetCollection "Source";
VMAppendCollectionDisplay = "001.50";
Call VMAppendCollectionItem "Source", "1.5";
Call VMPushCollection "Source";
Call VMCopyCollection "Source", "CopyOne";
Call VMCopyCollection "Source", "CopyTwo";
Call VMCopyCollection "Source", "CopyOne";
VMSetCollectionDisplay = "009.00";
Call VMSetCollectionItem "Source", 0, "9";
Call VMResetCollection "Source";
VMAppendCollectionDisplay = "010.00";
Call VMAppendCollectionItem "Source", "10";
Call VMPop;
LateBoundName = @_;
Call VMGetCollectionItem LateBoundName, 0;
LateBoundValue = @_;
LateBoundDisplay = VMGetCollectionDisplay;
Call VMDeactivateCollection "Source";
Call VMGetCollectionItem "CopyOne", 0;
CopyOneValue = @_;
CopyOneDisplay = VMGetCollectionDisplay;
Call VMGetCollectionItem "CopyTwo", 0;
CopyTwoValue = @_;
CopyTwoDisplay = VMGetCollectionDisplay;
''')

    assert env["VMFailed"] == 0
    assert env["VMNextCollectionId"] == 5
    assert _collection_id(env, "Source") == -1
    assert _collection_id(env, "CopyOne") == 3
    assert _collection_id(env, "CopyTwo") == 2
    assert env["VMCollectionEntryCount"] == 5
    # Original generation 0, historical CopyOne generation 1, CopyTwo 2,
    # latest CopyOne 3, and replacement Source generation 4 all remain rows.
    assert env["VMCollectionOwners"][:5] == [0, 1, 2, 3, 4]
    assert env["VMCollectionItems"][:5] == ["9", "1.5", "1.5", "1.5", "10"]
    assert env["VMCollectionItemDisplay"][:5] == [
        "009.00", "001.50", "001.50", "001.50", "010.00",
    ]
    # A stack-held name is resolved at use time; eager copies preserve their
    # prior raw/display values after source mutation, reset, and deactivation.
    assert env["LateBoundName"] == "Source"
    assert (env["LateBoundValue"], env["LateBoundDisplay"]) == ("10", "010.00")
    assert (env["CopyOneValue"], env["CopyOneDisplay"]) == ("1.5", "001.50")
    assert (env["CopyTwoValue"], env["CopyTwoDisplay"]) == ("1.5", "001.50")


def test_empty_copy_self_copy_and_missing_source_transitions():
    env = _run_helpers('''
Call VMResetCollection "Empty";
Call VMCopyCollection "Empty", "EmptyCopy";
EmptyCopyId = VMNextCollectionId - 1;
Call VMResetCollection "Kept";
VMAppendCollectionDisplay = "kept-display";
Call VMAppendCollectionItem "Kept", "kept-raw";
Call VMResetCollection "Dormant";
Call VMDeactivateCollection "Dormant";
BeforeSelfCopyNextId = VMNextCollectionId;
BeforeSelfCopyRows = VMCollectionEntryCount;
Call VMCopyCollection "Dormant", "Dormant";
AfterSelfCopyNextId = VMNextCollectionId;
AfterSelfCopyRows = VMCollectionEntryCount;
FailedAfterSelfCopy = VMFailed;
Call VMCopyCollection "NoSuchSource", "Kept";
FailedAfterMissingSource = VMFailed;
Call VMLengthCollection "Kept";
KeptLengthAfterMissingSource = @_;
Call VMGetCollectionItem "Kept", 0;
KeptValueAfterMissingSource = @_;
KeptDisplayAfterMissingSource = VMGetCollectionDisplay;
''')

    assert env["VMCollectionEntryCount"] == 1  # reset/copy of empty did not append
    assert env["VMNextCollectionId"] == 4
    assert env["EmptyCopyId"] == 1
    assert _collection_id(env, "EmptyCopy") == 1
    assert _collection_id(env, "Kept") == 2
    assert _collection_id(env, "Dormant") == -1
    assert env["BeforeSelfCopyNextId"] == env["AfterSelfCopyNextId"] == 4
    assert env["BeforeSelfCopyRows"] == env["AfterSelfCopyRows"] == 1
    assert env["FailedAfterSelfCopy"] == 0  # equal-name no-op precedes lookup
    assert env["FailedAfterMissingSource"] == 1
    assert env["KeptLengthAfterMissingSource"] == 1
    assert env["KeptValueAfterMissingSource"] == "kept-raw"
    assert env["KeptDisplayAfterMissingSource"] == "kept-display"
