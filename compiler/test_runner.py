"""Deterministic source-level test runner for Kuro projects."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .pipeline import run_source


@dataclass(frozen=True)
class TestCaseResult:
    path: Path
    passed: bool
    output: str = ""
    error: str = ""


def discover_tests(root: str | Path) -> list[Path]:
    base = Path(root)
    if base.is_file():
        return [base] if base.suffix == ".kuro" else []
    return sorted(base.rglob("*.kuro"))


def run_tests(root: str | Path) -> list[TestCaseResult]:
    results = []
    for path in discover_tests(root):
        try:
            result = run_source(path.read_text(encoding="utf-8"), filename=str(path))
        except OSError as error:
            results.append(TestCaseResult(path, False, error=str(error)))
            continue
        if result.compile.ok and result.runtime_error is None:
            results.append(TestCaseResult(path, True, output=result.stdout or ""))
        else:
            error = result.compile.diags.render_all() if not result.compile.ok else str(result.runtime_error)
            results.append(TestCaseResult(path, False, output=result.stdout or "", error=error))
    return results
