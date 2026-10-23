"""Production helper witnesses; no replacement representation is installed."""
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
ConsumerMode is Text;
Take user ConsumerMode;
Call VMResetCollection "Source";
VMAppendCollectionDisplay = "001.50";
Call VMAppendCollectionItem "Source", "raw-first";
VMAppendCollectionDisplay = "0007";
Call VMAppendCollectionItem "Source", "raw-last";
Call VMCopyCollection "Source", "Snapshot";
ConsumerName = "Source";
ConsumerIndex = 0;
If ConsumerMode is equal to "last";
    ConsumerIndex = -1;
Done.
If ConsumerMode is equal to "negative-first";
    ConsumerIndex = -2;
Done.
If ConsumerMode is equal to "too-negative";
    ConsumerIndex = -3;
Done.
If ConsumerMode is equal to "past-end";
    ConsumerIndex = 2;
Done.
If ConsumerMode is equal to "empty";
    Call VMResetCollection "Source";
Done.
If ConsumerMode is equal to "inactive";
    Call VMDeactivateCollection "Source";
Done.
If ConsumerMode is equal to "missing";
    ConsumerName = "Missing";
Done.
If ConsumerMode is equal to "snapshot";
    VMSetCollectionDisplay = "changed-display";
    Call VMSetCollectionItem "Source", 0, "changed-raw";
    Call VMResetCollection "Source";
    ConsumerName = "Snapshot";
Done.
Call VMGetCollectionItem ConsumerName, ConsumerIndex;
ConsumerCapturedValue = @_;
ConsumerCapturedDisplay = VMGetCollectionDisplay;
ConsumerCapturedFailure = VMFailed;
# Clobber the helper's result/display scratch after capturing the scalar pair.
Call VMResetCollection ConsumerName;
Call VMGetCollectionItem ConsumerName, 0;
If ConsumerCapturedFailure is equal to 0;
    Print ConsumerCapturedValue.
Else;
    # A failed helper's numeric zero is not a valid native Text pointer.
    Print "failed-get".
Done.
Print ConsumerCapturedDisplay.
Print ConsumerCapturedFailure.
Print VMCollectionEntryCount.
'''


CASES = [
    pytest.param("first", "raw-first\n001.50\n0\n4\n", id="first"),
    pytest.param("last", "raw-last\n0007\n0\n4\n", id="negative-last"),
    pytest.param("negative-first", "raw-first\n001.50\n0\n4\n", id="negative-first"),
    pytest.param("too-negative", "failed-get\n\n1\n4\n", id="too-negative-fallback"),
    pytest.param("past-end", "failed-get\n\n1\n4\n", id="past-end-fallback"),
    pytest.param("empty", "failed-get\n\n1\n4\n", id="empty-with-historical-rows"),
    pytest.param("inactive", "failed-get\n\n1\n4\n", id="inactive-with-historical-rows"),
    pytest.param("missing", "failed-get\n\n1\n4\n", id="missing-with-historical-rows"),
    pytest.param("snapshot", "raw-first\n001.50\n0\n4\n", id="copy-survives-source-set-reset"),
]


@pytest.mark.parametrize("mode,expected", CASES)
def test_helper_scalar_pair_and_fallback_hosted(mode, expected):
    result = run_source(_source(), input_fn=lambda _prompt: mode)
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    assert result.stdout == expected
    # Later failed reads do not retroactively mutate a captured scalar/display.
    assert result.interpreter.env["VMFailed"] == 1
    assert result.interpreter.env["VMGetCollectionDisplay"] == ""
    if expected.startswith("failed-get\n"):
        # Hosted inspection only; native probes do not reinterpret this sentinel
        # through the helper's inferred Text return ABI.
        assert result.interpreter.env["ConsumerCapturedValue"] == 0


@pytest.fixture(scope="module")
def consumer_image(tmp_path_factory):
    if not LINUX_X86:
        pytest.skip("requires executable Linux x86-64 helper image")
    compiled = compile_source(_source())
    assert compiled.ok, compiled.diags.render_all()
    image = tmp_path_factory.mktemp("consumer-values") / "probe"
    build_native(compiled.ir, image, target="x86_64-linux")
    return image


@pytest.mark.parametrize("mode,expected", CASES)
def test_helper_scalar_pair_and_fallback_native(mode, expected, consumer_image, tmp_path):
    result = subprocess.run([str(consumer_image)], input=mode, text=True,
                            capture_output=True, cwd=tmp_path, timeout=60, check=False)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")
