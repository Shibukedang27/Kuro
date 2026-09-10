#!/usr/bin/env python3
"""The `kuro` CLI (spec section 17).

Implemented honestly and only for what actually works end to end this
session: `run` and `check`. Every other subcommand the spec lists
(build/test/fmt/lint/doc/repl/package/doctor) is *named* here so `kuro help`
is a truthful list of the target surface, but each one exits 2 with
"not yet implemented" rather than pretending to do something — see spec
section 55 ("no fake features").
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from compiler.pipeline import compile_source, run_source  # noqa: E402

NOT_YET_IMPLEMENTED = {
    "build": "native/IR-emitting build (Stage 9, needs a backend)",
    "test": "Kuro-native test framework (spec section 32)",
    "fmt": "formatter (spec section 31)",
    "lint": "linter (spec section 17)",
    "doc": "documentation generator",
    "repl": "REPL (spec section 47)",
    "package": "package manager (spec section 15)",
    "doctor": "environment diagnostics",
}


def cmd_run(path: str) -> int:
    source = Path(path).read_text(encoding="utf-8")
    result = run_source(source, filename=path)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if not result.compile.ok:
        print(result.compile.diags.render_all(), file=sys.stderr)
        return 1
    if result.runtime_error is not None:
        print(f"error[{result.runtime_error.code}]: {result.runtime_error.message}", file=sys.stderr)
        return 1
    return 0


def cmd_check(path: str) -> int:
    source = Path(path).read_text(encoding="utf-8")
    result = compile_source(source, filename=path)
    if not result.ok:
        print(result.diags.render_all(), file=sys.stderr)
        return 1
    print(f"{path}: no problems found")
    return 0


def cmd_emit_ir(path: str) -> int:
    source = Path(path).read_text(encoding="utf-8")
    result = compile_source(source, filename=path)
    if not result.ok:
        print(result.diags.render_all(), file=sys.stderr)
        return 1
    print(result.ir)
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: kuro <run|check|emit-ir|version> <file.kuro>", file=sys.stderr)
        return 2
    cmd = argv[1]
    if cmd == "version":
        from compiler import __version__

        print(f"kuro {__version__}")
        return 0
    if cmd in NOT_YET_IMPLEMENTED:
        print(f"kuro {cmd}: not yet implemented ({NOT_YET_IMPLEMENTED[cmd]})", file=sys.stderr)
        return 2
    if cmd not in ("run", "check", "emit-ir"):
        print(f"kuro: unknown command {cmd!r}", file=sys.stderr)
        return 2
    if len(argv) < 3:
        print(f"usage: kuro {cmd} <file.kuro>", file=sys.stderr)
        return 2
    path = argv[2]
    if cmd == "run":
        return cmd_run(path)
    if cmd == "check":
        return cmd_check(path)
    return cmd_emit_ir(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
