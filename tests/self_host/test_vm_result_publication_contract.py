"""Pin admitted direct-call result boundaries; do not claim closure/native parity."""

import pytest

from compiler.pipeline import run_source
import test_vm_cross as harness


CASES = [
    pytest.param(
        "Action Seed; Return 17; Done. Action Read; Return @_; Done. "
        "Call Seed; Call Read; Print @_.",
        "17\n", [17], id="direct-entry-inherits-root-owner",
    ),
    pytest.param(
        "Action Answer; Return 42; Done. Action Read; Return @_; Done. "
        "Action Outer; Call Answer; Call Read; Return @_; Done. "
        "Call Outer; Print @_.",
        "42\n", [42], id="nested-callee-inherits-caller-owner",
    ),
    pytest.param(
        "Action Read _; Return @_; Done. Call Read 17; Print @_.",
        "17\n", [17], id="underscore-parameter-initializes-owner",
    ),
    pytest.param(
        "Action Write _; _ = 23; Return @_; Done. Call Write 17; Print @_.",
        "23\n", [23], id="explicit-assignment-replaces-owner",
    ),
    pytest.param(
        "Action Write _; Update _ to 23; Return @_; Done. Call Write 17; Print @_.",
        "23\n", [23], id="explicit-update-replaces-owner",
    ),
    pytest.param(
        "Action Write _; Add 6 to _; Return @_; Done. Call Write 17; Print @_.",
        "23\n", [23], id="explicit-add-replaces-owner",
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


def test_decimal_owner_publication_preserves_display(monkeypatch):
    source = (
        "Action Sink Value: Decimals; Return Value; Done. "
        "Action Forward Value: Decimals; Call Sink Value; Return @_; Done. "
        "Call Forward 3.25; Print @_."
    )
    steps = 0

    def bounded_run(text):
        nonlocal steps

        def trace(_instruction, _environment, _depth, _pc):
            nonlocal steps
            steps += 1
            assert steps <= 2_000_000, "authored decimal owner instruction budget exhausted"

        result = run_source(text, trace=trace, max_while_iterations=10_000)
        assert result.ok, (
            result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
        )
        assert result.interpreter.frames == []
        return result

    reference = bounded_run(source)
    assert reference.stdout == "3.25\n"
    monkeypatch.setattr(harness, "run_source", bounded_run)
    environment = harness.run_kuro_vm_environment(source)
    assert environment["VMFailed"] == 0
    assert environment["VMOutput"] == [3.25]
    assert environment["VMOutputDisplay"] == ["3.25"]
    assert environment["VMLastResultDisplay"] == "3.25"
    assert environment["VMFrameDepth"] == 0
    assert environment["VMFrameEntryCount"] == 0


def test_failed_authored_invocation_does_not_publish_completed_inner_result():
    # Use a malformed instruction inside an entered Action to exercise VMFailed
    # itself. Division by zero currently escapes through the host interpreter,
    # so it cannot expose the authored VM's post-failure state for inspection.
    import json

    tokens = [
        "BC_FUNC_BEGIN", "Seed", "BC_CONST", "17", "BC_RETURN", "BC_FUNC_END",
        "BC_FUNC_BEGIN", "Answer", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END",
        "BC_FUNC_BEGIN", "Outer", "BC_CALL_BEGIN", "Answer", "BC_CALL_END",
        "BC_CONST", "99", "BC_STORE_LIST", "Side", "BC_INVALID_OWNER_TEST",
        "BC_FUNC_END", "BC_CALL_BEGIN", "Seed", "BC_CALL_END",
        "BC_CALL_BEGIN", "Outer", "BC_CALL_END", "BC_CONST", "998", "BC_PRINT",
    ]
    vm = harness.BYTECODE_RE.sub("", harness.VM.read_text(), count=1)
    source = "BytecodeOut = " + ", ".join(json.dumps(token) for token in tokens) + ";\n" + vm
    steps = 0

    def trace(*_args):
        nonlocal steps
        steps += 1
        assert steps <= 100_000, "authored failed-owner instruction budget exhausted"

    result = run_source(source, trace=trace, max_while_iterations=10_000)
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    environment = result.interpreter.env
    assert result.interpreter.frames == []
    assert environment["VMFailed"] == 1
    assert environment["VMLastResult"] == 17
    assert environment["VMLastResultDisplay"] == ""
    assert environment["VMFrameDepth"] == 0
    assert environment["VMFrameEntryCount"] == 0
    assert environment["VMOutputCount"] == 0
    assert "VMOutput" not in environment
    # Ordinary variable writes are not transactional result rollback.
    names = environment["VMNames"][:environment["VMNameCount"]]
    assert environment["VMValues"][names.index("Side")] == 99
