"""Native-only logical row-admission boundary prototype, not production or COW.

The appended Kuro helpers maintain a monotonic logical debit separate from the
production VM's physical row columns. Candidate admission scans real source
owners and charges one debit per matching row, but deliberately publishes no
values, generation, or detach. The native candidate full-budget path uses a
test-only out-of-bounds Set as a bounds-exit surrogate; that surrogate is not
a capacity label or a hosted-runtime rule.
"""
from __future__ import annotations

from pathlib import Path
import platform
import subprocess

import pytest

from compiler.native import NATIVE_COLLECTION_CAPACITY, build_native
from compiler.pipeline import compile_source, run_source

ROOT = Path(__file__).resolve().parents[2]
LIMIT = 65_536
NATIVE_TARGET = {
    ("Linux", "x86_64"): "x86_64-linux",
    ("Linux", "amd64"): "x86_64-linux",
    ("Darwin", "arm64"): "aarch64-macos",
    ("Darwin", "aarch64"): "aarch64-macos",
    ("Darwin", "x86_64"): "x86_64-macos",
    ("Darwin", "amd64"): "x86_64-macos",
}.get((platform.system(), platform.machine().lower()))


# Appended only by this test. The helper records logical debit per source row;
# it never appends a destination value or changes a production collection.
ADMISSION_HELPER = r'''
VMTestLogicalLimit = 65536;
VMTestLogicalUsed = 0;
VMTestAdmissionFailed = 0;
VMTestNativeTrap = 0;
Action VMTestDebit Amount;
    VMTestDebit_Pos = 0;
    While VMTestDebit_Pos is less than Amount and VMTestAdmissionFailed is equal to 0;
        If VMTestLogicalUsed is less than VMTestLogicalLimit;
            Add 1 to VMTestLogicalUsed;
            Add 1 to VMTestDebit_Pos;
        Else;
            If VMTestNativeTrap is equal to 1;
                # Native-only experiment: fail here, not after copying returns.
                Set VMCollectionOwners 65536 to 0;
            Done.
            # Hosted observation mode only; not a production failure protocol.
            VMTestAdmissionFailed = 1;
        Done.
    Done.
Done.
Action VMTestVirtualAppendDebit;
    # Admission only: deliberately does not append or publish a production row.
    Call VMTestDebit 1;
Done.
Action VMTestAdmitCopy SourceName, DestinationName;
    # Identity is returned before lookup, including an inactive same-name slot.
    If SourceName is equal to DestinationName;
        Return VMTestLogicalUsed;
    Else;
        Call VMFindCollection SourceName, 0;
        VMTestAdmitCopy_SourceIndex = @_;
        If VMTestAdmitCopy_SourceIndex is less than 0;
            VMFailed = 1;
        Else;
            Get VMCollectionIds VMTestAdmitCopy_SourceIndex;
            VMTestAdmitCopy_SourceId = @_;
            VMTestAdmitCopy_Pos = 0;
            While VMTestAdmitCopy_Pos is less than VMCollectionEntryCount and VMTestAdmissionFailed is equal to 0;
                Get VMCollectionOwners VMTestAdmitCopy_Pos;
                If @_ is equal to VMTestAdmitCopy_SourceId;
                    Call VMTestDebit 1;
                Done.
                Add 1 to VMTestAdmitCopy_Pos;
            Done.
        Done.
    Done.
    Return VMTestLogicalUsed;
Done.
'''


def _source(driver: str) -> str:
    """Use unchanged production VM source and append this file's test driver."""
    vm = (ROOT / "self_host" / "vm.kuro").read_text(encoding="utf-8")
    return vm + "\n" + ADMISSION_HELPER + "\n" + driver


def _compile(source: str):
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    return compiled


def _boundary_driver() -> str:
    return r'''
Mode is Text;
Take user Mode;
VMTestNativeTrap = 1;
Call VMResetCollection "Source";
VMAppendCollectionDisplay = "001.50";
Call VMAppendCollectionItem "Source", "raw-one";
VMAppendCollectionDisplay = "002.00";
Call VMAppendCollectionItem "Source", "raw-two";
VMTestLogicalUsed = 2;
If Mode is equal to "candidate-row-prefix" or Mode is equal to "candidate-owner-bound";
    Call VMTestDebit 65533;
    Print "before-last-row".
    Print VMTestLogicalUsed.
    Call VMTestVirtualAppendDebit;
    Print "last-row-admitted".
    Print VMTestLogicalUsed.
    Print VMCollectionEntryCount.
    Length VMCollectionItems;
    Print @_.
    Length VMCollectionItemDisplay;
    Print @_.
    If Mode is equal to "candidate-owner-bound";
        # Length on declared Integers is not admitted by the hosted frontend.
        # Instead show owner index 1 exists and index 2 is still out of bounds.
        Get VMCollectionOwners 1;
        Print @_.
        Print "before-third-owner".
        Get VMCollectionOwners 2;
        Print "unreachable-third-owner".
    Done.
    Call VMTestVirtualAppendDebit;
    Print "unreachable-after-rejected-row".
Done.
BoundaryFiller = 65534;
BoundaryEager = 0;
If Mode is equal to "eager-exact";
    BoundaryFiller = 65532;
    BoundaryEager = 1;
Done.
If Mode is equal to "candidate-exact";
    BoundaryFiller = 65532;
Done.
If Mode is equal to "eager-one-spare";
    BoundaryFiller = 65533;
    BoundaryEager = 1;
Done.
If Mode is equal to "candidate-one-spare";
    BoundaryFiller = 65533;
Done.
If Mode is equal to "eager-full";
    BoundaryEager = 1;
Done.
BoundaryPos = 0;
If BoundaryEager is equal to 1;
    Call VMResetCollection "Filler";
    While BoundaryPos is less than BoundaryFiller;
        Call VMAppendCollectionItem "Filler", "pad";
        Call VMTestDebit 1;
        Add 1 to BoundaryPos;
    Done.
Else;
    Call VMTestDebit BoundaryFiller;
Done.
Print "operation=copy".
Print "logical-before".
Print VMTestLogicalUsed.
If BoundaryEager is equal to 1;
    Call VMCopyCollection "Source", "Published";
    Call VMTestAdmitCopy "Source", "Published";
Else;
    Call VMTestAdmitCopy "Source", "Published";
Done.
Print "operation=copy-complete".
Print "logical-after".
Print VMTestLogicalUsed.
Print VMCollectionEntryCount.
Length VMCollectionItems;
Print @_.
Length VMCollectionItemDisplay;
Print @_.
Call VMLengthCollection "Source";
Print @_.
Call VMFindCollection "Published", 0;
BoundaryPublishedIndex = @_;
BoundaryPublishedLength = 0;
If BoundaryPublishedIndex is greater than or equal to 0;
    Call VMLengthCollection "Published";
    BoundaryPublishedLength = @_;
Done.
Print BoundaryPublishedLength.
Print VMFailed.
'''


@pytest.fixture(scope="module")
def boundary_image(tmp_path_factory):
    if NATIVE_TARGET is None:
        pytest.skip("runtime executable probe requires supported Linux/Darwin native host")
    assert NATIVE_COLLECTION_CAPACITY == LIMIT
    compiled = _compile(_source(_boundary_driver()))
    image = tmp_path_factory.mktemp("native-logical-admission") / "boundary"
    # Explicitly select the matching executable; the default omits Intel Darwin.
    build_native(compiled.ir, image, target=NATIVE_TARGET)
    return image


def _run(image, mode: str, *, timeout: int = 90):
    return subprocess.run(
        [str(image)], input=mode.encode(), capture_output=True,
        cwd=image.parent, timeout=timeout, check=False,
    )


@pytest.mark.parametrize(
    "case,logical_before",
    [("exact", LIMIT - 2), ("one-spare", LIMIT - 1), ("full", LIMIT)],
)
def test_native_eager_production_copy_and_candidate_prefix_at_boundary(
    boundary_image, case, logical_before
):
    """One driver selects eager or candidate; source cells remain real production rows."""
    eager = _run(boundary_image, f"eager-{case}")
    candidate = _run(boundary_image, f"candidate-{case}")
    common_prefix = f"operation=copy\nlogical-before\n{logical_before}\n".encode()
    assert eager.stdout.startswith(common_prefix), (case, eager)
    assert candidate.stdout.startswith(common_prefix), (case, candidate)
    assert eager.stderr == candidate.stderr == b""

    if case == "exact":
        assert eager.returncode == candidate.returncode == 0
        eager_lines = eager.stdout.decode().splitlines()
        candidate_lines = candidate.stdout.decode().splitlines()
        assert eager_lines[:5] == ["operation=copy", "logical-before", str(LIMIT - 2),
                                   "operation=copy-complete", "logical-after"]
        assert candidate_lines[:5] == eager_lines[:5]
        assert eager_lines[5:] == [str(LIMIT), str(LIMIT), str(LIMIT), str(LIMIT), "2", "2", "0"]
        # Candidate: logical count reaches the true limit while all actual row columns
        # still contain only the two source cells; no dummy reservation was appended.
        assert candidate_lines[5:] == [str(LIMIT), "2", "2", "2", "2", "0", "0"]
    else:
        # Eager invokes the unchanged production copier against actual filler rows;
        # candidate only debits per source row. Both encounter their test boundary.
        assert eager.returncode == candidate.returncode == 1, (case, eager, candidate)
        assert eager.stdout == candidate.stdout == common_prefix


def test_native_virtual_append_exits_inside_first_rejected_debit(boundary_image):
    result = _run(boundary_image, "candidate-row-prefix")
    assert (result.returncode, result.stdout, result.stderr) == (
        1, b"before-last-row\n65535\nlast-row-admitted\n65536\n2\n2\n2\n", b"",
    )


def test_native_virtual_debits_do_not_extend_integer_owner_column(boundary_image):
    result = _run(boundary_image, "candidate-owner-bound")
    assert (result.returncode, result.stdout, result.stderr) == (
        1, b"before-last-row\n65535\nlast-row-admitted\n65536\n2\n2\n2\n0\nbefore-third-owner\n", b"",
    )


def test_candidate_edge_semantics_are_monotonic_and_not_publication():
    """Hosted execution observes helper state without the native-only Set surrogate."""
    driver = r'''
Call VMResetCollection "Source";
VMAppendCollectionDisplay = "001.50";
Call VMAppendCollectionItem "Source", "one";
VMAppendCollectionDisplay = "002.00";
Call VMAppendCollectionItem "Source", "two";
Call VMResetCollection "Empty";
Call VMResetCollection "Destination";
VMTestLogicalUsed = 65532;
Call VMTestAdmitCopy "Source", "Destination";
Call VMTestAdmitCopy "Source", "Destination";
Print VMTestLogicalUsed.
Call VMResetCollection "Destination";
Call VMDeactivateCollection "Destination";
Print VMTestLogicalUsed.
Call VMTestAdmitCopy "Source", "Source";
Call VMCopyCollection "Source", "Source";
Print VMTestLogicalUsed.
Call VMTestAdmitCopy "Destination", "Destination";
Call VMCopyCollection "Destination", "Destination";
Print VMTestLogicalUsed.
Call VMTestAdmitCopy "Empty", "Destination";
Call VMCopyCollection "Empty", "Destination";
Print VMTestLogicalUsed.
Call VMTestAdmitCopy "Missing", "Destination";
Print VMTestLogicalUsed.
Print VMFailed.
Call VMResetCollection "SetTarget";
VMAppendCollectionDisplay = "009.25";
Call VMAppendCollectionItem "SetTarget", "before";
VMSetCollectionDisplay = "009.25";
Call VMSetCollectionItem "SetTarget", 0, "after";
Print VMTestLogicalUsed.
Call VMGetCollectionItem "SetTarget", 0;
Print @_.
Print VMGetCollectionDisplay.
Call VMTestVirtualAppendDebit;
Print VMTestLogicalUsed.
Print VMTestAdmissionFailed.
Print VMCollectionEntryCount.
Length VMCollectionItems;
Print @_.
Length VMCollectionItemDisplay;
Print @_.
'''
    result = run_source(_source(driver))
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    # Repeated source-copy admission debits four rows; reset/deactivation, identity,
    # empty-copy, and Set neither refund nor debit. Invalid source fails without debit.
    assert result.stdout == "65536\n65536\n65536\n65536\n65536\n65536\n1\n65536\nafter\n009.25\n65536\n1\n3\n3\n3\n"
    assert result.interpreter.env["VMFailed"] == 1  # only the intentional missing source


def test_hosted_controls_prove_native_bounds_surrogate_is_not_hosted_semantics():
    """Production hosted append remains unbounded; the native Set surrogate is not."""
    hosted_append = r'''
Call VMResetCollection "HostedRows";
HostedPos = 0;
While HostedPos is less than 65537;
    Call VMAppendCollectionItem "HostedRows", "row";
    Add 1 to HostedPos;
Done.
Call VMLengthCollection "HostedRows";
Print @_.
'''
    result = run_source(_source(hosted_append))
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    assert result.stdout == "65537\n"
    assert result.interpreter.env["VMCollectionEntryCount"] == 65537

    # The exact same out-of-range native-only Set cannot be used as a hosted limit:
    # hosted collections are dynamic and the source array here has only its seed rows.
    surrogate = r'''
Set VMCollectionOwners 65536 to 0;
Print "unreachable".
'''
    bounded = run_source(_source(surrogate))
    assert bounded.compile.ok, bounded.compile.diags.render_all()
    assert bounded.runtime_error is not None
    assert bounded.runtime_error.code == "E6001"
    assert bounded.stdout == ""
