"""Bounded public-bytecode witnesses for VM collection generation churn.

The launcher is the complete production artifact launcher; these tests only
append diagnostics and feed it framed bytecode.  The VM currently rejects an
empty BC_STORE_MULTI (zero operands), so successful churn witnesses use valid
non-empty stores and a separate case records that empty-store boundary.
"""
from __future__ import annotations

import platform
import subprocess

import pytest

from compiler.native import build_native
from compiler.pipeline import compile_source, run_source
from compiler.self_host import native_artifact_launcher_source


# The repeat count lives in bytecode rather than being an unrolled sequence.
RESET_LOOP = [
    "BC_CONST", "7", "BC_REPEAT_BEGIN",
    "BC_MULTI_BEGIN", "BC_CONST_TEXT", "alpha", "BC_CONST_TEXT", "omega",
    "BC_STORE_MULTI", "A", "BC_REPEAT_END",
    "BC_LOADVAR", "A", "BC_PRINT",
]

COPY_LOOP = [
    "BC_CONST", "7", "BC_REPEAT_BEGIN",
    "BC_MULTI_BEGIN", "BC_CONST_TEXT", "alpha", "BC_CONST_TEXT", "omega",
    "BC_STORE_MULTI", "A",
    "BC_LOADVAR", "A", "BC_STORE_LIST", "B",
    "BC_REPEAT_END",
    "BC_LOADVAR", "B", "BC_PRINT",
]

ONE_ITEM_COPY_LOOP = [
    "BC_CONST_TEXT", "seed", "BC_APPEND", "A",
    "BC_CONST", "7", "BC_REPEAT_BEGIN",
    "BC_LOADVAR", "A", "BC_STORE_LIST", "B",
    "BC_REPEAT_END",
    "BC_LOADVAR", "B", "BC_PRINT",
]

# An empty multi-store is deliberately covered as the current invalid boundary:
# VM dispatch requires more than one operand before it resets a destination.
EMPTY_STORE = ["BC_MULTI_BEGIN", "BC_STORE_MULTI", "Empty"]

CASES = [
    pytest.param(RESET_LOOP, "alpha\nomega\n7\n1\n14\n0\n0\n", 0,
                 id="bounded-repeat-resets-one-collection"),
    pytest.param(COPY_LOOP, "alpha\nomega\n14\n2\n28\n0\n0\n", 0,
                 id="bounded-repeat-copies-each-current-generation"),
    pytest.param(ONE_ITEM_COPY_LOOP, "seed\n8\n2\n8\n0\n0\n", 0,
                 id="bounded-repeat-copies-one-item-generations"),
    pytest.param(EMPTY_STORE, "0\n0\n0\n1\n1\n", 1,
                 id="empty-multi-store-is-invalid-and-does-not-allocate"),
]


def _source() -> str:
    return native_artifact_launcher_source() + (
        "\nPrint VMNextCollectionId.\n"
        "Print VMCollectionCount.\n"
        "Print VMCollectionEntryCount.\n"
        "Print VMFailed.\n"
        "Print RuntimeExitCode.\n"
    )


def _payload(tokens: list[str]) -> str:
    return "kuro.bytecode/1\n" + "\n".join(tokens) + "\n"


@pytest.mark.parametrize("tokens,expected,expected_exit", CASES)
def test_hosted_bounded_bytecode_generation_churn(tokens, expected, expected_exit):
    payload = _payload(tokens)
    result = run_source(_source(), input_fn=lambda _prompt: payload)
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    env = result.interpreter.env
    assert env["ArtifactSource"] == payload
    assert env["ArtifactFailed"] == 0
    assert env["VMFailed"] == expected_exit
    assert env["RuntimeExitCode"] == expected_exit
    assert result.stdout == expected


@pytest.fixture(scope="module")
def native_churn_images(tmp_path_factory):
    if platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"}:
        pytest.skip("requires executable Linux x86-64 images")
    root = tmp_path_factory.mktemp("generation-dispatch-churn")
    compiled = compile_source(_source())
    assert compiled.ok, compiled.diags.render_all()
    image = root / "generation-dispatch-churn"
    build_native(compiled.ir, image, target="x86_64-linux")
    return image


@pytest.mark.parametrize("tokens,expected,expected_exit", CASES)
def test_native_bounded_bytecode_generation_churn(tokens, expected, expected_exit,
                                                  native_churn_images, tmp_path):
    result = subprocess.run(
        [str(native_churn_images)],
        input=_payload(tokens).encode("utf-8"),
        capture_output=True,
        cwd=tmp_path,
        timeout=60,
        check=False,
    )
    assert (result.returncode, result.stdout, result.stderr) == (
        expected_exit, expected.encode("utf-8"), b""
    )
