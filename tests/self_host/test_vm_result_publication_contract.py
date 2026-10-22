"""Pin admitted direct-call result boundaries; do not claim closure/native parity."""

import pytest

from compiler.pipeline import run_source
import test_vm_cross as harness


CASES = [
    pytest.param(
        "Action Seed; Return 17; Done. Action Read; Return @_; Done. "
        "Call Seed; Call Read; Print @_.",
        "17\n", [0], id="direct-entry-live-global-versus-zero",
    ),
    pytest.param(
        "Action Answer; Return 42; Done. Action Read; Return @_; Done. "
        "Action Outer; Call Answer; Call Read; Return @_; Done. "
        "Call Outer; Print @_.",
        "42\n", [0], id="nested-callee-entry-not-caller-inheritance",
    ),
    pytest.param(
        "Action Answer; Return 42; Done. "
        "Action Outer; Call Answer; Done. Call Outer; Print @_.",
        "None\n", [0], id="implicit-return-none-versus-zero",
    ),
    pytest.param(
        "Action Answer; Return 42; Done. "
        "Action Outer; Call Answer; Print @_. Return 9; Done. "
        "Call Outer; Print @_.",
        "42\n9\n", [42, 9], id="explicit-nested-publication-agrees",
    ),
]


@pytest.mark.parametrize("source, reference_output, authored_output", CASES)
def test_direct_call_initialization_and_publication_boundary(
    monkeypatch, source, reference_output, authored_output,
):
    def bounded_run(text):
        steps = 0

        def trace(_instruction, _environment, _depth, _pc):
            nonlocal steps
            steps += 1
            assert steps <= 2_000_000, "authored publication instruction budget exhausted"

        result = run_source(text, trace=trace, max_while_iterations=10_000)
        assert result.ok, (
            result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
        )
        assert result.interpreter.frames == []
        return result

    reference = bounded_run(source)
    assert reference.stdout == reference_output
    # Reuse the established source -> authored lexer/parser/lower/encoder/VM
    # composition, with a shared execution budget across its internal Actions.
    monkeypatch.setattr(harness, "run_source", bounded_run)
    environment = harness.run_kuro_vm_environment(source)
    assert environment["VMFailed"] == 0
    assert environment["VMOutput"] == authored_output
    assert environment["VMFrameDepth"] == 0
    assert environment["VMFrameEntryCount"] == 0
