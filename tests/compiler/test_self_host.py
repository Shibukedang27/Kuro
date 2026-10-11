import platform

import pytest

from compiler.self_host import compile_with_kuro_driver, verify_native_compiler


MACOS_ARM64_HOST = (
    platform.system() == "Darwin"
    and platform.machine().lower() in {"arm64", "aarch64"}
)


def test_kuro_authored_driver_compiles_source():
    env = compile_with_kuro_driver('Print "self hosted".')
    assert env["CompilerFailed"] == 0
    assert env["CompilerOutput"][:2] == ["BC_CONST_TEXT", "self hosted"]


def test_kuro_authored_driver_compiles_itself():
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    source = (root / "self_host" / "compiler.kuro").read_text(encoding="utf-8")
    env = compile_with_kuro_driver(source)
    assert env["CompilerFailed"] == 0
    assert "BC_FUNC_BEGIN" in env["CompilerOutput"]


def test_native_compiler_matches_kuro_authored_driver(tmp_path):
    from compiler.self_host import build_native_compiler

    image = tmp_path / "kuro-compiler"
    build_native_compiler(None, image)
    report = verify_native_compiler('Print "parity".', image=image)
    assert report == {"failed": 0, "instruction_count": 3}


@pytest.mark.skipif(
    not MACOS_ARM64_HOST,
    reason="dist/kuro-compiler is the packaged macOS ARM64 image",
)
def test_native_compiler_verification_accepts_existing_image():
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    image = root / "dist" / "kuro-compiler"
    if not image.is_file():
        return
    report = verify_native_compiler("Print 7.", image=image)
    assert report["failed"] == 0
