"""Action Return must escape VM loop drivers without executing later tokens."""
from __future__ import annotations

import platform
import subprocess

import pytest

from compiler.pipeline import run_source
from compiler.self_host import build_native_artifact_launcher, compile_with_kuro_driver
from test_artifact_launcher import run_artifact
from test_vm_cross import run_kuro_vm_environment


# Keep inputs small and expected output explicit. Sentinels after Return and
# after each loop detect both accidental fallthrough and another iteration.
CASES = [
    pytest.param(
        "Action Pick; N = 0; While N is less than 2; Add 1 to N; "
        "Return 7; Print 901. Done. Print 902. Return 8; Done. "
        "Call Pick; Print @_. Call Pick; Print @_. Print 99.",
        "7\n7\n99\n", id="while-return-repeated-call",
    ),
    pytest.param(
        "Action Pick; Repeat 3; Return 7; Print 901. Done. "
        "Print 902. Return 8; Done. Call Pick; Print @_. "
        "Call Pick; Print @_. Print 99.",
        "7\n7\n99\n", id="repeat-return-repeated-call",
    ),
    pytest.param(
        "Action Pick; N = 0; While N is less than 3; Add 1 to N; "
        "If N is equal to 2; Return N; Else; Print N. Done. "
        "Done. Print 902. Return 8; Done. Call Pick; Print @_. Print 99.",
        "1\n2\n99\n", id="while-conditional-later-iteration",
    ),
    pytest.param(
        "Action Pick; N = 0; Repeat 3; Add 1 to N; "
        "If N is equal to 2; Return N; Else; Print N. Done. "
        "Done. Print 902. Return 8; Done. Call Pick; Print @_. Print 99.",
        "1\n2\n99\n", id="repeat-conditional-later-iteration",
    ),
    pytest.param(
        "Action Pick; N = 0; While N is less than 2; Add 1 to N; "
        "M = 0; While M is less than 2; Add 1 to M; Return 7; "
        "Print 901. Done. Print 902. Done. Return 8; Done. "
        "Call Pick; Print @_. N = 0; While N is less than 2; "
        "Print N. Add 1 to N; Done. Print 99.",
        "7\n0\n1\n99\n", id="nested-while-and-depth-reuse",
    ),
    pytest.param(
        "Action Pick; N = 0; While N is less than 2; Add 1 to N; "
        "Repeat 3; Return 7; Print 901. Done. Print 902. Done. "
        "Return 8; Done. Call Pick; Print @_. Print 99.",
        "7\n99\n", id="repeat-inside-while",
    ),
    pytest.param(
        "Action Pick; Repeat 3; N = 0; While N is less than 2; "
        "Add 1 to N; Return 7; Print 901. Done. Print 902. Done. "
        "Return 8; Done. Call Pick; Print @_. Print 99.",
        "7\n99\n", id="while-inside-repeat",
    ),
    pytest.param(
        "Action Pick; Repeat 3; Repeat 2; Return 7; Print 901. "
        "Done. Print 902. Done. Return 8; Done. Call Pick; Print @_. Print 99.",
        "7\n99\n", id="nested-repeat-immediate-unwind",
    ),
    pytest.param(
        'Action Pick Value: Text; While 1 is equal to 1; Return Value; '
        'Print 901. Done. Return "wrong"; Done. '
        'Call Pick "kept"; Print @_. Print 99.',
        "kept\n99\n", id="text-return",
    ),
    pytest.param(
        "Action Pick Value: Decimals; Repeat 3; Return Value; Print 901. "
        "Done. Return 0.0; Done. Call Pick 3.25; Print @_. Print 99.",
        "3.25\n99\n", id="decimal-return-display",
    ),
    pytest.param(
        "Action Pick; N = 0; While N is less than 0; Return 7; Done. "
        "Repeat 0; Return 8; Done. Return 9; Done. Call Pick; Print @_. Print 99.",
        "9\n99\n", id="skipped-loops-explicit-fallthrough",
    ),
    pytest.param(
        "Action Inner Value; While 1 is equal to 1; Return Value; Done. "
        "Done. Action Outer; N = 0; While N is less than 3; "
        "Call Inner N; Print @_. Add 1 to N; Done. Return 7; Done. "
        "Call Outer; Print @_. Print 99.",
        "0\n1\n2\n7\n99\n", id="callee-return-does-not-exit-caller-loop",
    ),
    pytest.param(
        "Action Count Value; While Value is greater than 0; "
        "Call Count Value - 1; Return 1 + @_; Print 901. Done. Return 0; "
        "Done. Call Count 3; Print @_. Print 99.",
        "3\n99\n", id="recursive-while-return",
    ),
    pytest.param(
        "N = 0; Repeat 3; Repeat 2; Add 1 to N; Done. Print N. Done. Print 99.",
        "2\n4\n6\n99\n", id="nested-repeat-normal-completion",
    ),
]

# These were contract-only fixtures until the reference lowerer gained
# invocation-safe counter and Index restoration. Keep the reference trace
# bounded below so a future collision regression cannot hang the suite.
REENTRANT_REPEAT_CASES = [
    pytest.param(
        "Action Pick; Repeat 3; Return 7; Done. Done. N = 0; "
        "Repeat 3; Call Pick; Print @_. Add 1 to N; Done. Print N.",
        "7\n7\n7\n3\n", id="callee-repeat-return-preserves-caller-repeat",
    ),
    pytest.param(
        "Action Pick; Repeat 2; Print 7. Done. Return 8; Done. "
        "Repeat 3; Call Pick; Print @_. Print 9. Done. Print 99.",
        "7\n7\n8\n9\n7\n7\n8\n9\n7\n7\n8\n9\n99\n",
        id="callee-repeat-completion-preserves-caller-tail",
    ),
    pytest.param(
        "Action Count Value; If Value is equal to 0; Return 0; Done. "
        "Repeat 2; Call Count Value - 1; Return 1 + @_; Print 901. "
        "Done. Return 8; Done. Repeat 3; Call Count 3; Print @_. Done. Print 99.",
        "3\n3\n3\n99\n", id="recursive-repeat-return-resumes-caller",
    ),
    *[
        pytest.param(
            "Action Pick; " + "Repeat 1; " * depth + "Return 7; "
            + "Done. " * depth + "Return 8; Done. "
            "Call Pick; Print @_. Call Pick; Print @_. Print 99.",
            "7\n7\n99\n", id=f"repeat-depth-{depth}-unwind-and-reuse",
        )
        for depth in (9, 10, 11)
    ],
]
ALL_CASES = CASES + REENTRANT_REPEAT_CASES


def artifact(source):
    compiled = compile_with_kuro_driver(source)
    assert compiled["CompilerFailed"] == 0
    return "kuro.bytecode/1\n" + "\n".join(compiled["CompilerOutput"]) + "\n"


@pytest.mark.parametrize("source,expected", ALL_CASES)
def test_host_loop_return_oracle(source, expected):
    steps = 0

    def bounded_trace(*_):
        nonlocal steps
        steps += 1
        assert steps <= 10000, "reference Repeat execution exceeded its test budget"

    host = run_source(source, trace=bounded_trace)
    assert host.ok, host.compile.diags.render_all() if not host.compile.ok else host.runtime_error
    assert host.stdout == expected


@pytest.mark.parametrize("source,expected", ALL_CASES)
def test_authored_vm_loop_return_contract(source, expected):
    env = run_kuro_vm_environment(source)
    assert env["VMFailed"] == 0
    output = "".join(
        (display if display else str(value)) + "\n"
        for value, display in zip(env["VMOutput"], env["VMOutputDisplay"])
    )
    assert output == expected
    assert env["VMFrameDepth"] == 0
    assert env["VMFrameEntryCount"] == 0
    assert env["VMWhileDepth"] == 0
    assert env["VMRepeatDepth"] == 0
    assert env["VMReturnPending"] == 0
    assert env["VMPos"] == env["VMCodeLen"]


@pytest.mark.parametrize("source,expected", ALL_CASES)
def test_framed_launcher_loop_return_contract(source, expected):
    env, output = run_artifact(artifact(source))
    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert output == expected


@pytest.fixture(scope="module")
def fresh_loop_return_launcher(tmp_path_factory):
    if platform.system() not in {"Darwin", "Linux"}:
        pytest.skip("requires a supported native backend")
    image = tmp_path_factory.mktemp("loop-return-launcher") / "kuro-bytecode"
    build_native_artifact_launcher(image)
    return image


@pytest.mark.parametrize("source,expected", ALL_CASES)
def test_fresh_native_launcher_loop_return_contract(
    source, expected, fresh_loop_return_launcher, tmp_path,
):
    payload = artifact(source)
    (tmp_path / "program.kuro").write_text(source, encoding="utf-8")
    (tmp_path / "program.kurobc").write_text(payload, encoding="utf-8")
    result = subprocess.run(
        [str(fresh_loop_return_launcher)], input=payload, text=True,
        capture_output=True, check=False, timeout=20,
    )
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")
