from __future__ import annotations

import subprocess

import pytest

from compiler import self_host


COMPOSER = self_host.ROOT / "bootstrap" / "compose-native-source.sh"


@pytest.mark.parametrize(
    ("mode", "target"),
    [
        ("compiler", "aarch64-macos"),
        ("runtime", "aarch64-macos"),
        ("artifact-launcher", "aarch64-macos"),
        *[
            ("codegen", target)
            for target in ("aarch64-macos", "x86_64-macos", "x86_64-linux")
        ],
    ],
    ids=[
        "compiler-aarch64-macos",
        "runtime-aarch64-macos",
        "artifact-launcher-aarch64-macos",
        "codegen-aarch64-macos",
        "codegen-x86_64-macos",
        "codegen-x86_64-linux",
    ],
)
def test_shell_native_source_composition_matches_python_oracle(
    mode: str, target: str
) -> None:
    if mode == "compiler":
        expected = self_host.native_compiler_source()
    elif mode == "runtime":
        expected = self_host.native_runtime_source()
    elif mode == "artifact-launcher":
        expected = self_host.native_artifact_launcher_source()
    else:
        expected = self_host.native_codegen_source(target)
    result = subprocess.run(
        ["sh", str(COMPOSER), mode, target],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout == expected


def test_shell_native_source_composer_rejects_unknown_codegen_target() -> None:
    result = subprocess.run(
        ["sh", str(COMPOSER), "codegen", "unknown-target"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "unsupported codegen output target" in result.stderr

@pytest.mark.parametrize('output_target', ['aarch64-macos', 'x86_64-macos', 'x86_64-linux'])
@pytest.mark.parametrize('execution_target', ['unverified', 'aarch64-macos', 'x86_64-macos', 'x86_64-linux'])
def test_codegen_execution_target_composition_matches_shell(output_target, execution_target):
    expected = self_host.native_codegen_source(output_target, execution_target=execution_target)
    result = subprocess.run(['sh', str(COMPOSER), 'codegen', output_target, execution_target],
                            check=True, capture_output=True, text=True)
    assert result.stdout == expected
    assert f'NativeIndexedExecutionTarget = "{execution_target}";' in expected


def test_codegen_execution_target_composition_defaults_fail_closed():
    assert 'NativeIndexedExecutionTarget = "unverified";' in self_host.native_codegen_source('x86_64-linux')
    with pytest.raises(self_host.SelfHostError, match='execution target'):
        self_host.native_codegen_source('x86_64-linux', execution_target='unsafe-target')
    result = subprocess.run(['sh', str(COMPOSER), 'codegen', 'x86_64-linux', 'unsafe-target'],
                            capture_output=True, text=True)
    assert result.returncode != 0 and 'execution target' in result.stderr


@pytest.mark.parametrize('requested,system,machine,expected', [
    (None, 'Linux', 'x86_64', 'x86_64-linux'),
    (None, 'Darwin', 'arm64', 'aarch64-macos'),
    ('x86_64-macos', 'Linux', 'x86_64', 'x86_64-macos'),
    ('x86_64-linux', 'Darwin', 'arm64', 'x86_64-linux'),
])
def test_codegen_builder_transports_image_target_not_output_abi(monkeypatch, tmp_path, requested, system, machine, expected):
    import platform
    from types import SimpleNamespace
    from compiler import native, pipeline
    captured = {}
    monkeypatch.setattr(platform, 'system', lambda: system)
    monkeypatch.setattr(platform, 'machine', lambda: machine)
    def compile_stub(source):
        captured['source'] = source
        return SimpleNamespace(ok=True, ir=object())
    def build_stub(ir, output, **kwargs):
        captured.update(kwargs)
        return output
    monkeypatch.setattr(pipeline, 'compile_source', compile_stub)
    monkeypatch.setattr(native, 'build_native', build_stub)
    self_host.build_native_codegen(tmp_path / 'generator', target=requested, output_target='x86_64-linux')
    assert captured['target'] == expected
    assert f'NativeIndexedExecutionTarget = "{expected}";' in captured['source']
    assert 'NativeTarget = "x86_64-linux";' in captured['source']
