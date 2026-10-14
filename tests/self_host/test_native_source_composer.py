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
