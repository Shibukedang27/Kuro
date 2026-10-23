"""Production-VM witnesses that a publication storage model must preserve.

No COW implementation is installed by these tests. The native and hosted
launchers execute the same production source with fixed framed bytecode.
"""
from __future__ import annotations

import platform
import subprocess

import pytest

from compiler.native import build_native
from compiler.pipeline import compile_source, run_source
from compiler.self_host import native_artifact_launcher_source


CASES = [
    pytest.param(
        [
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "old", "BC_CONST", "001.50",
            "BC_STORE_MULTI", "A", "BC_LOADVAR", "A",
            "BC_LOADVAR", "A", "BC_STORE_LIST", "B",
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "new", "BC_CONST_TEXT", "tail",
            "BC_STORE_MULTI", "A", "BC_PRINT",
            "BC_LOADVAR", "B", "BC_PRINT",
        ],
        "new\ntail\nold\n001.50\n0\n0\n",
        id="stack-name-rebinds-but-assigned-snapshot-does-not",
    ),
    pytest.param(
        [
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "seed", "BC_CONST", "001.50",
            "BC_STORE_MULTI", "A", "BC_LOADVAR", "A", "BC_STORE_LIST", "B",
            "BC_LOADVAR", "B", "BC_STORE_LIST", "C",
            "BC_LOADVAR", "B", "BC_STORE_LIST", "B",
            "BC_CONST", "0", "BC_CONST_TEXT", "changed", "BC_SET", "B",
            "BC_CONST", "0009.00", "BC_APPEND", "B",
            "BC_CONST_TEXT", "scalar", "BC_STORE_LIST", "A",
            "BC_LOADVAR", "C", "BC_PRINT", "BC_LOADVAR", "B", "BC_PRINT",
        ],
        "seed\n001.50\nchanged\n001.50\n0009.00\n0\n0\n",
        id="destination-set-append-self-copy-and-source-deactivation",
    ),
    pytest.param(
        [
            "BC_FUNC_BEGIN", "Keep", "BC_PARAM", "Saved", "Text",
            "BC_CONST", "0", "BC_CONST_TEXT", "changed", "BC_SET", "A",
            "BC_LOADVAR", "Saved", "BC_RETURN", "BC_FUNC_END",
            "BC_MULTI_BEGIN", "BC_CONST", "001.50", "BC_CONST_TEXT", "tail",
            "BC_STORE_MULTI", "A", "BC_CONST", "0", "BC_GET", "A", "1",
            "BC_CALL_BEGIN", "Keep", "BC_LOADVAR", "_", "BC_CALL_END",
            "BC_PRINT", "BC_LOADVAR", "_", "BC_PRINT", "BC_LOADVAR", "A", "BC_PRINT",
        ],
        "001.50\n001.50\nchanged\ntail\n0\n0\n",
        id="cell-display-survives-frame-return-and-result-slot",
    ),
    pytest.param(
        [
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "old", "BC_CONST_TEXT", "tail",
            "BC_STORE_MULTI", "A", "BC_LOADVAR", "A",
            "BC_CONST_TEXT", "scalar", "BC_STORE_LIST", "A", "BC_PRINT",
        ],
        "1\n1\n",
        id="stack-name-deactivation-fails-not-retained-generation",
    ),
    pytest.param(
        [
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "source", "BC_CONST_TEXT", "tail",
            "BC_STORE_MULTI", "A",
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "partial", "BC_LOADVAR", "A",
            "BC_STORE_MULTI", "B",
        ],
        "1\n1\n1\npartial\n",
        id="invalid-multi-store-leaves-partial-publication",
    ),
    pytest.param(
        [
            "BC_FUNC_BEGIN", "Echo", "BC_PARAM", "P", "Text",
            "BC_LOADVAR", "P", "BC_RETURN", "BC_FUNC_END",
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "old", "BC_CONST_TEXT", "tail",
            "BC_STORE_MULTI", "A", "BC_CALL_BEGIN", "Echo",
            "BC_LOADVAR", "A", "BC_CALL_END", "BC_PRINT",
        ],
        "A\n0\n0\n",
        id="collection-argument-and-return-erase-collection-kind",
    ),
    pytest.param(
        [
            "BC_FUNC_BEGIN", "Shadow", "BC_PARAM", "A", "Integers",
            "BC_LOADVAR", "A", "BC_PRINT", "BC_CONST", "0", "BC_RETURN", "BC_FUNC_END",
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "old", "BC_CONST_TEXT", "tail",
            "BC_STORE_MULTI", "A", "BC_CALL_BEGIN", "Shadow",
            "BC_CONST", "5", "BC_CALL_END",
        ],
        "old\ntail\n0\n0\n",
        id="global-collection-precedes-scalar-frame-parameter",
    ),
    pytest.param(
        [
            "BC_CONST", "41", "BC_STORE_LIST", "VMNextCollectionId",
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "left", "BC_CONST_TEXT", "right",
            "BC_STORE_MULTI", "VMCollectionIds",
            "BC_LOADVAR", "VMNextCollectionId", "BC_PRINT",
            "BC_LOADVAR", "VMCollectionIds", "BC_PRINT",
        ],
        "41\nleft\nright\n0\n0\n",
        id="bytecode-names-do-not-alias-private-helper-state",
    ),
    pytest.param(
        ["BC_CALL_BEGIN", "VMResetCollection", "BC_CALL_END"],
        "1\n1\n",
        id="bytecode-calls-do-not-invoke-outer-helper-actions",
    ),
    pytest.param(
        [
            "BC_MULTI_BEGIN", "BC_CONST", "001.50", "BC_CONST_TEXT", "tail",
            "BC_STORE_MULTI", "A", "BC_CONST", "0", "BC_GET", "A", "1",
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "new", "BC_CONST_TEXT", "end",
            "BC_STORE_MULTI", "A", "BC_PRINT",
            "BC_LOADVAR", "_", "BC_PRINT", "BC_LOADVAR", "A", "BC_PRINT",
        ],
        "001.50\n001.50\nnew\nend\n0\n0\n",
        id="get-scalar-stack-and-result-outlive-source-reset",
    ),
    pytest.param(
        [
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "first", "BC_CONST_TEXT", "last",
            "BC_STORE_MULTI", "A", "BC_CONST", "2", "BC_GET", "A", "1",
            "BC_PRINT",
        ],
        "1\n1\n",
        id="failed-get-stops-before-user-print",
    ),
]


def _source(partial: bool) -> str:
    source = native_artifact_launcher_source()
    source += "\nPrint VMFailed.\nPrint RuntimeExitCode.\n"
    if partial:
        # Capture failure flags first: the diagnostic reads themselves are not
        # a claim that failed VM execution is transactional or resumable.
        source += 'Call VMLengthCollection "B";\nPrint @_.\nCall VMGetCollectionItem "B", 0;\nPrint @_.\n'
    return source


def _payload(tokens: list[str]) -> str:
    return "kuro.bytecode/1\n" + "\n".join(tokens) + "\n"


@pytest.mark.parametrize("tokens,expected", CASES)
def test_production_vm_publication_roots_hosted(tokens, expected):
    source = _source(expected.endswith("partial\n"))
    result = run_source(source, input_fn=lambda _prompt: _payload(tokens))
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    assert result.interpreter.env["ArtifactFailed"] == 0
    assert result.stdout == expected


@pytest.fixture(scope="module")
def native_root_images(tmp_path_factory):
    if platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"}:
        pytest.skip("requires executable Linux x86-64 images")
    root = tmp_path_factory.mktemp("publication-root-images")
    images = {}
    for partial in (False, True):
        compiled = compile_source(_source(partial))
        assert compiled.ok, compiled.diags.render_all()
        image = root / ("partial" if partial else "ordinary")
        build_native(compiled.ir, image, target="x86_64-linux")
        images[partial] = image
    return images


@pytest.mark.parametrize("tokens,expected", CASES)
def test_production_vm_publication_roots_native(tokens, expected, native_root_images, tmp_path):
    image = native_root_images[expected.endswith("partial\n")]
    result = subprocess.run(
        [str(image)], input=_payload(tokens).encode(), capture_output=True,
        cwd=tmp_path, timeout=60, check=False,
    )
    # The native epilogue propagates RuntimeExitCode even with diagnostic prints.
    expected_exit = 1 if expected.startswith("1\n1\n") else 0
    assert (result.returncode, result.stdout, result.stderr) == (expected_exit, expected.encode(), b"")
