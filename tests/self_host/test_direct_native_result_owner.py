"""Executable x86-64 regressions for direct-native result ownership.

These exercise the hosted compiler's real native image, not emitted-assembly
text. They are intentionally Linux/x86-64-only; existing ARM64 admission and
assembly witnesses remain separate, and this file makes no ARM64 parity claim.
"""

import platform
import subprocess

import pytest

from compiler.native import NativeBackendError, build_native, emit_x86_64_linux
from compiler.pipeline import compile_source


requires_x86_64_linux = pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires executable x86-64 Linux native images",
)


def _run_native(source: str, tmp_path, name: str) -> subprocess.CompletedProcess[str]:
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    executable = tmp_path / name
    build_native(compiled.ir, executable, target="x86_64-linux")
    return subprocess.run(
        [str(executable)],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
        cwd=tmp_path,
    )


@pytest.mark.parametrize(
    "source",
    [
        'Action Seed; Return "hello"; Done. Action Echo; Print @_. Return 1; Done. '
        'Call Seed; Call Echo; Print @_.',
        "Action Seed; Return 3.25; Done. Action Echo; Print @_. Return 1; Done. "
        "Call Seed; Call Echo; Print @_.",
        "_ = 1, 2; Action Read; Return @_; Done. Call Read; Print @_.",
        "_ is Integers; Take user _; Action Read; Return @_; Done. "
        "Call Read; Print @_.",
    ],
    ids=["inherited-text-owner", "inherited-float-owner", "collection-owner", "input-owner"],
)
def test_x86_emitter_rejects_ambiguous_underscore_result_owners(source):
    # Admission must fail on every host: this exercises portable Linux x86
    # emission directly, not executable-image availability or a platform skip.
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    with pytest.raises(NativeBackendError, match="result owner"):
        emit_x86_64_linux(compiled.ir)


@requires_x86_64_linux
def test_direct_no_param_entry_inherits_callers_current_result(tmp_path):
    source = (
        "Action Seed; Return 17; Done. "
        "Action Read; Return @_; Done. "
        "Call Seed; Call Read; Print @_."
    )
    native = _run_native(source, tmp_path, "direct-entry")
    assert native.returncode == 0, native.stderr
    assert native.stdout == "17\n"


@requires_x86_64_linux
def test_nested_no_param_reader_sees_callers_underscore_parameter(tmp_path):
    source = (
        "Action Read; If @_ is equal to 17; Return 1; Done. Return 0; Done. "
        "Action Outer _; Call Read; Return @_; Done. "
        "Call Outer 17; Print @_."
    )
    native = _run_native(source, tmp_path, "nested-parameter-owner")
    assert native.returncode == 0, native.stderr
    assert native.stdout == "1\n"


@requires_x86_64_linux
def test_nested_successful_producer_reassigns_callers_result_owner(tmp_path):
    # The inner Answer publishes 42 into Outer's local result slot. Read must
    # inherit that current slot (not the old parameter 17 or ambient root slot).
    source = (
        "Action Seed; Return 17; Done. Action Answer; Return 42; Done. "
        "Action Read; If @_ is equal to 17; Return 1; Else; Return 0; Done. Done. "
        "Action Outer _; Call Answer; Call Read; Return @_; Done. "
        "Call Seed; Call Outer 17; Print @_."
    )
    native = _run_native(source, tmp_path, "nested-producer-owner")
    assert native.returncode == 0, native.stderr
    assert native.stdout == "0\n"


@requires_x86_64_linux
def test_recursive_activations_keep_their_underscore_parameter_owner(tmp_path):
    # Each recursive activation receives a distinct underscore parameter. A
    # nested no-parameter Read must see that activation's value: 7, 3, 2, 1.
    source = (
        "Seen is Integers; Seen = 0; "
        "Action Read; Return @_; Done. "
        "Action Recur N, _; Call Read; Seen = Seen * 10 + @_; "
        "If N is greater than 0; Call Recur N - 1, N; Return @_; Done. "
        "Return @_; Done. "
        "Call Recur 3, 7; Print Seen."
    )
    native = _run_native(source, tmp_path, "recursive-owner")
    assert native.returncode == 0, native.stderr
    assert native.stdout == "7321\n"


@requires_x86_64_linux
def test_six_argument_call_preserves_hidden_result_owner_channel(tmp_path):
    source = (
        "Action Six A, B, C, D, E, F; Return A + B + C + D + E + F; Done. "
        "Call Six 1, 2, 3, 4, 5, 6; Print @_."
    )
    native = _run_native(source, tmp_path, "six-argument-owner-channel")
    assert native.returncode == 0, native.stderr
    assert native.stdout == "21\n"


@requires_x86_64_linux
def test_successful_publication_and_outer_return_boundary(tmp_path):
    source = (
        "Action Answer; Return 42; Done. "
        "Action Outer; Call Answer; Print @_. Return 9; Done. "
        "Call Outer; Print @_."
    )
    native = _run_native(source, tmp_path, "return-boundary")
    assert native.returncode == 0, native.stderr
    assert native.stdout == "42\n9\n"


@requires_x86_64_linux
def test_raw_call_without_source_publication_keeps_root_result_owner(tmp_path):
    # Source Call syntax normally lowers to CALL followed by STORE_LIST of its
    # result temporary. Remove only Outer’s publication to pin the raw-IR API
    # boundary: nested Answer production must not leak into the root owner.
    source = (
        "Action Seed; Return 17; Done. Action Answer; Return 42; Done. "
        "Action Outer; Call Answer; Return 9; Done. "
        "Call Seed; Call Outer; Print @_."
    )
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    outer_call = next(
        index for index, instruction in enumerate(compiled.ir.main)
        if instruction.op == "CALL" and instruction.args[0] == "Outer"
    )
    publication = compiled.ir.main[outer_call + 1]
    assert publication.op == "STORE_LIST" and publication.args[0] == "_"
    del compiled.ir.main[outer_call + 1]

    executable = tmp_path / "raw-call-no-publication"
    build_native(compiled.ir, executable, target="x86_64-linux")
    native = subprocess.run(
        [str(executable)], capture_output=True, text=True, check=False,
        timeout=30, cwd=tmp_path,
    )
    assert native.returncode == 0, native.stderr
    assert native.stdout == "17\n"


@requires_x86_64_linux
def test_explicit_underscore_write_is_published_by_successful_call(tmp_path):
    source = "Action Write _; _ = 23; Return @_; Done. Call Write 17; Print @_."
    native = _run_native(source, tmp_path, "explicit-write")
    assert native.returncode == 0, native.stderr
    assert native.stdout == "23\n"


@requires_x86_64_linux
def test_admitted_failing_call_stops_before_later_publication_or_output(tmp_path):
    # Native arithmetic faults are process-fatal, not recoverable source-call
    # unwinds. This pins only fail-stop behavior: prior successful output stays,
    # and execution never reaches the statements after the fault.
    source = (
        "Action Answer; Return 42; Done. Action Fail; Return 1 / 0; Done. "
        "Call Answer; Print @_. Call Fail; Print 99."
    )
    native = _run_native(source, tmp_path, "failing-call")
    assert native.returncode != 0
    assert native.stdout == "42\n"


@requires_x86_64_linux
def test_nested_failure_after_inner_producer_stops_before_outer_publication(tmp_path):
    source = (
        "Action Answer; Return 42; Done. Action Fail; Return 1 / 0; Done. "
        "Action Outer; Call Answer; Print @_. Call Fail; Return 9; Done. "
        "Call Outer; Print 99."
    )
    native = _run_native(source, tmp_path, "nested-failing-call")
    assert native.returncode != 0
    assert native.stdout == "42\n"
