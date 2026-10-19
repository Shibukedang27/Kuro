"""Guard expensive generator fixture lifetime without building native images."""
from pathlib import Path
import json

import pytest


pytest_plugins = ["pytester"]
ROOT = Path(__file__).resolve().parents[2]


def test_macos_x86_generator_builds_once_per_module_and_is_fresh_per_session(pytester):
    # Import the real fixture in a separate pytest process, so no host-platform
    # spoofing or monkeypatch can leak into the native integration suite.
    events = pytester.path / "builds.jsonl"
    pytester.makeconftest(
        f'''
import json
import sys
from pathlib import Path

sys.path.insert(0, {str(ROOT)!r})
import compiler.self_host

sys.path.insert(0, {str(ROOT / "tests" / "self_host")!r})
from test_native_codegen import x86_macos_codegen


def fake_build(output, target=None, output_target="aarch64-macos"):
    with Path({str(events)!r}).open("a") as stream:
        stream.write(json.dumps([str(output), target, output_target]) + "\\n")
    output.write_text("fresh test-only generator")


compiler.self_host.build_native_codegen = fake_build
'''
    )
    pytester.makepyfile(
        '''
import inspect
import pytest
import test_native_codegen as native_codegen


integration = native_codegen.test_native_kuro_codegen_image_emits_executable_x86_macos
assert "x86_macos_codegen" in inspect.signature(integration).parameters
cases = next(mark.args[1] for mark in integration.pytestmark if mark.name == "parametrize")
assert len(cases) == 6


@pytest.mark.parametrize("tokens,expected", cases)
def test_consumer(tokens, expected, tmp_path, x86_macos_codegen):
    assert x86_macos_codegen.read_text() == "fresh test-only generator"
    # Each consumer retains its own workspace; sharing is only the executable.
    assert x86_macos_codegen.parent != tmp_path
    (tmp_path / "case").write_text(repr((tokens, expected)))
'''
    )
    for session in range(2):
        result = pytester.runpytest_subprocess("-q")
        result.assert_outcomes(passed=6)
        builds = [json.loads(line) for line in events.read_text().splitlines()]
        assert len(builds) == session + 1
        assert builds[-1][1:] == ["x86_64-macos", "x86_64-macos"]
    # Never use a stale image from a previous pytest invocation/checkout.
    assert builds[0][0] != builds[1][0]
