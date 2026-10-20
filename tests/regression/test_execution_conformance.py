"""Cross-runtime conformance cases for the hosted and Kuro-authored runtimes.

Keep this corpus deliberately small and deterministic. Each case is executed
through both pipelines and must produce the same observable output. Add a
regression case here whenever a mismatch is discovered.
"""
import pytest

from compiler.pipeline import run_source
from compiler.self_host import run_with_kuro_runtime


CASES = [
    pytest.param('Print "Kuro".', "Kuro\n", ["Kuro"], id="text-output"),
    pytest.param("Print 2 + 3 * 4.", "14\n", [14], id="operator-precedence"),
    pytest.param(
        "N = 1;\nUpdate N to N + 2;\nPrint N.",
        "3\n",
        [3],
        id="variable-update",
    ),
    pytest.param(
        'If 1 is equal to 1;\nPrint "yes".\nElse;\nPrint "no".\nDone.',
        "yes\n",
        ["yes"],
        id="if-branch",
    ),
    pytest.param(
        "N = 0;\nWhile N is less than 3;\nPrint N.\nAdd 1 to N;\nDone.",
        "0\n1\n2\n",
        [0, 1, 2],
        id="while-loop",
    ),
    pytest.param(
        "Action Fact N;\n"
        "If N is less than or equal to 1;\nReturn 1;\nElse;\n"
        "Call Fact N - 1;\nReturn N * @_;\nDone.\nDone.\n"
        "Call Fact 5;\nPrint @_.",
        "120\n",
        [120],
        id="recursive-action",
    ),
    pytest.param(
        'Items is Text;\n'
        'Append "a" to Items;\n'
        'Append "b" to Items;\n'
        'Append "c" to Items;\n'
        'Get Items 1;\nPrint @_.\nLength Items;\nPrint @_.',
        "b\n3\n",
        ["b", 3],
        id="collection-index-and-length",
    ),
    pytest.param(
        'Items = "a", "b", "c";\n'
        'Print Items.\nLength Items;\nPrint @_.\nGet Items 1;\nPrint @_.',
        "a\nb\nc\n3\nb\n",
        ["a", "b", "c", 3, "b"],
        id="multi-value-collection-assignment",
    ),
]


@pytest.mark.parametrize(("source", "expected_stdout", "expected_vm_output"), CASES)
def test_hosted_and_kuro_authored_runtimes_agree(
    source: str, expected_stdout: str, expected_vm_output: list[object]
):
    hosted = run_source(source)
    assert hosted.ok, (
        hosted.compile.diags.render_all()
        if not hosted.compile.ok
        else str(hosted.runtime_error)
    )
    assert hosted.stdout == expected_stdout

    native = run_with_kuro_runtime(source)
    assert native["RuntimeExitCode"] == 0
    assert native["RuntimeFailed"] == 0
    assert native["VMOutput"] == expected_vm_output


def test_negative_repeat_failure_conforms_between_hosted_and_kuro_runtime():
    source = 'Repeat -1;\nPrint "unreachable".\nDone.'

    hosted = run_source(source)
    assert not hosted.ok
    assert hosted.runtime_error is not None
    assert hosted.runtime_error.code == "E6004"

    native = run_with_kuro_runtime(source)
    assert native["RuntimeExitCode"] == 1
    assert native["RuntimeFailed"] == 1
    assert native.get("VMOutput") is None
