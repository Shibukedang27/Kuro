from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "bootstrap" / "audit-native-bootstrap-gap.sh"


def _seed_tools(tmp_path: Path) -> tuple[Path, Path]:
    compiler = tmp_path / "seed-compiler"
    compiler.write_text(
        "#!/bin/sh\n"
        "if grep -q 'CompilerFailed' ; then\n"
        "  if [ \"${FAKE_COMPILER_MODE:-complete}\" = truncated ]; then\n"
        "    printf 'kuro.bytecode/1\\n'\n"
        "    exit 0\n"
        "  fi\n"
        "  printf 'kuro.bytecode/1\\n'\n"
        "  i=0\n"
        "  while [ \"$i\" -lt 70 ]; do printf 'BC_FUNC_BEGIN\\nBC_FUNC_END\\n'; i=$((i + 1)); done\n"
        "  i=0\n"
        "  while [ \"$i\" -lt 290 ]; do printf 'BC_CALL_BEGIN\\n'; i=$((i + 1)); done\n"
        "  i=0\n"
        "  while [ \"$i\" -lt 8700 ]; do printf 'BC_NOOP\\n'; i=$((i + 1)); done\n"
        "else\n"
        "  printf 'kuro.bytecode/1\\nBC_CONST\\n5\\nBC_PRINT\\n'\n"
        "fi\n",
        encoding="utf-8",
    )
    codegen = tmp_path / "seed-codegen"
    codegen.write_text(
        "#!/bin/sh\n"
        "if grep -q '^BC_FUNC_BEGIN$' ; then\n"
        "  case \"${FAKE_CODEGEN_MODE:-blocked}\" in\n"
        "    recovered) printf '.globl _start\\n'; exit 0 ;;\n"
        "    crash) exit 139 ;;\n"
        "    diagnostic) printf 'unsupported\\n' >&2; exit 1 ;;\n"
        "    partial) printf '.section .text\\n'; exit 1 ;;\n"
        "    blocked) exit 1 ;;\n"
        "    *) exit 88 ;;\n"
        "  esac\n"
        "fi\n"
        "printf '.globl _start\\n'\n",
        encoding="utf-8",
    )
    compiler.chmod(0o755)
    codegen.chmod(0o755)
    return compiler, codegen


def _run_audit(
    tmp_path: Path,
    *,
    compiler_mode: str = "complete",
    codegen_mode: str = "blocked",
) -> subprocess.CompletedProcess[str]:
    compiler, codegen = _seed_tools(tmp_path)
    env = os.environ.copy()
    env["KURO_NATIVE_SEED_COMPILER"] = str(compiler)
    env["KURO_NATIVE_SEED_CODEGEN"] = str(codegen)
    env["FAKE_COMPILER_MODE"] = compiler_mode
    env["FAKE_CODEGEN_MODE"] = codegen_mode
    return subprocess.run(
        ["sh", str(AUDIT)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_native_bootstrap_audit_reports_observed_full_compiler_codegen_gap(tmp_path: Path) -> None:
    result = _run_audit(tmp_path)
    assert result.returncode == 0, result.stderr
    assert "Python/toolchain visibility: blocked during audit" in result.stdout
    assert "Arithmetic stage-0 codegen control: passed" in result.stdout
    assert "BC_FUNC_BEGIN markers=70; BC_CALL_BEGIN markers=290" in result.stdout
    assert "normal rejection (status 1, stdout/stderr empty; no partial assembly)" in result.stdout
    assert "no dist files changed" in result.stdout


def test_native_bootstrap_audit_rejects_truncated_compiler_artifact(tmp_path: Path) -> None:
    result = _run_audit(tmp_path, compiler_mode="truncated")
    assert result.returncode != 0
    assert "compiler artifact is below the documented full-source guardrails" in result.stderr


def test_native_bootstrap_audit_fails_closed_when_codegen_recovers(tmp_path: Path) -> None:
    result = _run_audit(tmp_path, codegen_mode="recovered")
    assert result.returncode != 0
    assert "full compiler codegen now exits successfully" in result.stderr


def test_native_bootstrap_audit_rejects_codegen_crash_or_unexpected_status(tmp_path: Path) -> None:
    result = _run_audit(tmp_path, codegen_mode="crash")
    assert result.returncode != 0
    assert "expected normal codegen rejection status 1, got 139" in result.stderr


def test_native_bootstrap_audit_rejects_partial_codegen_output(tmp_path: Path) -> None:
    result = _run_audit(tmp_path, codegen_mode="partial")
    assert result.returncode != 0
    assert "expected empty output on normal rejection" in result.stderr


def test_native_bootstrap_audit_rejects_stderr_diagnostics(tmp_path: Path) -> None:
    result = _run_audit(tmp_path, codegen_mode="diagnostic")
    assert result.returncode != 0
    assert "expected empty output on normal rejection" in result.stderr
    assert "stdout=0 bytes stderr=" in result.stderr
    assert "refusing partial or diagnostic output" in result.stderr
