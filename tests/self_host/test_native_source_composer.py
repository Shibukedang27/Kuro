from __future__ import annotations

import subprocess

import pytest

from compiler import self_host


COMPOSER = self_host.ROOT / "bootstrap" / "compose-native-source.sh"


@pytest.mark.parametrize(
    ("mode", "target", "expected"),
    [
        ("compiler", "aarch64-macos", self_host.native_compiler_source()),
        ("runtime", "aarch64-macos", self_host.native_runtime_source()),
        ("artifact-launcher", "aarch64-macos", self_host.native_artifact_launcher_source()),
        *[
            ("codegen", target, self_host.native_codegen_source(target))
            for target in ("aarch64-macos", "x86_64-macos", "x86_64-linux")
        ],
    ],
)
def test_shell_native_source_composition_matches_python_oracle(
    mode: str, target: str, expected: str
) -> None:
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
