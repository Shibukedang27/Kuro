#!/usr/bin/env python3
"""The Kuro compiler, artifact builder, runtime launcher, and developer CLI."""
from __future__ import annotations

import sys
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from compiler.pipeline import compile_source, run_source  # noqa: E402
from compiler.bytecode import encode_ir  # noqa: E402
from compiler.ir import ir_to_data, validate  # noqa: E402
from compiler.artifacts import make_artifact_document  # noqa: E402
from compiler.packages import read_manifest, resolve_manifest, verify_lock, write_lock  # noqa: E402
from compiler.formatter import format_source  # noqa: E402
from compiler.linter import lint_source  # noqa: E402

NOT_YET_IMPLEMENTED = {
    "doc": "documentation generator",
    "doctor": "environment diagnostics",
}


def cmd_test(path: str = ".") -> int:
    from compiler.test_runner import run_tests

    results = run_tests(path)
    for result in results:
        if result.passed:
            print(f"PASS {result.path}")
        else:
            print(f"FAIL {result.path}")
            if result.error:
                print(result.error, file=sys.stderr)
    passed = sum(result.passed for result in results)
    print(f"tests: {passed}/{len(results)} passed")
    return 0 if results and passed == len(results) else 1


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


def cmd_build(path: str, output: str | None = None) -> int:
    """Compile a Kuro source file into a validated portable IR artifact.

    This is deliberately an IR build, not a native executable build. Keeping
    that distinction explicit prevents the CLI from claiming a backend that
    does not exist yet while still making compilation a reproducible step in
    a project workflow.
    """
    source = Path(path).read_text(encoding="utf-8")
    result = compile_source(source, filename=path)
    if not result.ok:
        print(result.diags.render_all(), file=sys.stderr)
        return 1
    problems = validate(result.ir)
    if problems:
        print("error[E5001]: invalid IR", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    destination = Path(output) if output else Path(path).with_suffix(".kuro.ir")
    destination.parent.mkdir(parents=True, exist_ok=True)
    artifact = make_artifact_document(encode_ir(result.ir), kind="kuro.ir/1", entry=Path(path).name)
    artifact["program"] = ir_to_data(result.ir)
    destination.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(f"{path}: built IR -> {destination}")
    return 0


def cmd_bundle(path: str, output: str | None = None) -> int:
    """Write a deterministic portable Kuro application bundle."""
    source = Path(path).read_text(encoding="utf-8")
    result = compile_source(source, filename=path)
    if not result.ok:
        print(result.diags.render_all(), file=sys.stderr)
        return 1
    problems = validate(result.ir)
    if problems:
        print("error[E5001]: invalid IR", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    destination = Path(output) if output else Path(path).with_suffix(".kuro.app")
    destination.parent.mkdir(parents=True, exist_ok=True)
    bundle = make_artifact_document(encode_ir(result.ir), kind="kuro.app/1", entry=Path(path).name)
    bundle.update({"artifact": "validated-ir", "ir": str(result.ir), "program": ir_to_data(result.ir)})
    destination.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    print(f"{path}: bundled portable app -> {destination}")
    return 0


def cmd_exec(path: str) -> int:
    from compiler.artifacts import ArtifactError, run_artifact

    try:
        _, output, runtime_error = run_artifact(path)
    except (OSError, ArtifactError) as error:
        print(f"error[E8002]: {error}", file=sys.stderr)
        return 1
    if output:
        sys.stdout.write(output)
    if runtime_error is not None:
        print(f"error[{runtime_error.code}]: {runtime_error.message}", file=sys.stderr)
        return 1
    return 0


def cmd_native_artifact(path: str, output: str | None = None, target: str | None = None) -> int:
    """Turn a validated Kuro artifact into a Python-free executable image."""
    from compiler.artifacts import ArtifactError, read_program
    from compiler.bytecode import decode_to_ir
    from compiler.native import NativeBackendError, build_native

    destination = Path(output) if output else Path(path).with_suffix("")
    try:
        program = read_program(path)
        build_native(decode_to_ir(program), destination, target=target)
    except (OSError, ArtifactError, NativeBackendError, subprocess.SubprocessError) as error:
        print(f"error[E8007]: {error}", file=sys.stderr)
        return 1
    print(f"{path}: standalone executable -> {destination}")
    return 0


def cmd_artifact_verify(path: str) -> int:
    from compiler.artifacts import ArtifactError, read_program

    try:
        program = read_program(path)
    except (OSError, ArtifactError) as error:
        print(f"error[E8008]: {error}", file=sys.stderr)
        return 1
    print(f"{path}: valid Kuro artifact ({len(program.main)} main instructions, {len(program.functions)} functions)")
    return 0


def cmd_artifact_pack(path: str, output: str | None = None) -> int:
    """Convert a validated JSON artifact to the framed binary Kuro format."""
    from compiler.artifacts import ArtifactError, read_artifact_document, read_program, write_binary_artifact

    destination = Path(output) if output else Path(path).with_suffix(".kuro.bin")
    try:
        document = read_artifact_document(path)
        program = read_program(path)
        write_binary_artifact(destination, program, kind=document["format"], entry=document["entry"])
    except (OSError, ArtifactError) as error:
        print(f"error[E8009]: {error}", file=sys.stderr)
        return 1
    print(f"{path}: packed reusable Kuro artifact -> {destination}")
    return 0


def cmd_package(path: str) -> int:
    try:
        manifest = read_manifest(path)
        packages = resolve_manifest(path)
        lock = write_lock(path, packages)
        verify_lock(path)
    except (OSError, ValueError) as error:
        print(f"error[E5003]: {error}", file=sys.stderr)
        return 1
    print(f"package {manifest.name} {manifest.version}: resolved {len(packages)} package(s)")
    print(f"lockfile -> {lock}")
    return 0


def cmd_fmt(path: str, write: bool = False) -> int:
    source_path = Path(path)
    formatted = format_source(source_path.read_text(encoding="utf-8"))
    if write:
        source_path.write_text(formatted, encoding="utf-8")
    else:
        sys.stdout.write(formatted)
    return 0


def cmd_lint(path: str, strict: bool = False) -> int:
    source = Path(path).read_text(encoding="utf-8")
    diags = lint_source(source, filename=path)
    if diags.diagnostics:
        print(diags.render_all(), file=sys.stderr)
    if diags.has_errors() or (strict and diags.diagnostics):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: kuro <run|check|build|bundle|exec|emit-ir|version> <file>", file=sys.stderr)
        return 2
    cmd = argv[1]
    if cmd == "debug":
        from cli.debugger import debug_main
        if len(argv) < 3:
            print("usage: kuro debug <file.kuro> [--break LINE] [--max-steps N] [--watch NAME] [--json]", file=sys.stderr)
            return 2
        breaks: set[int] = set()
        max_steps = None
        json_output = False
        watches: set[str] = set()
        index = 3
        while index < len(argv):
            if argv[index] == "--break" and index + 1 < len(argv):
                breaks.add(int(argv[index + 1])); index += 2
            elif argv[index] == "--max-steps" and index + 1 < len(argv):
                max_steps = int(argv[index + 1]); index += 2
            elif argv[index] == "--json":
                json_output = True; index += 1
            elif argv[index] == "--watch" and index + 1 < len(argv):
                watches.add(argv[index + 1]); index += 2
            else:
                print("usage: kuro debug <file.kuro> [--break LINE] [--max-steps N]", file=sys.stderr)
                return 2
        return debug_main(argv[2], breakpoints=breaks, max_steps=max_steps, json_output=json_output, watches=watches)
    if cmd == "profile":
        from compiler.profiler import profile_source
        if len(argv) not in (3, 4) or (len(argv) == 4 and argv[3] != "--json"):
            print("usage: kuro profile <file.kuro> [--json]", file=sys.stderr)
            return 2
        try:
            report = profile_source(Path(argv[2]).read_text(encoding="utf-8"), argv[2])
        except (OSError, ValueError) as error:
            print(error, file=sys.stderr)
            return 1
        if len(argv) == 4:
            sys.stdout.write(report.to_json())
            return 0
        if report.program_output:
            sys.stdout.write(report.program_output)
        print(f"profile: {report.elapsed_seconds:.6f}s")
        print(f"max call depth: {report.max_call_depth}")
        for operation, count in report.instruction_counts.most_common():
            print(f"{operation}: {count}")
        return 0
    if cmd == "init":
        from compiler.scaffold import create_project
        if len(argv) != 3:
            print("usage: kuro init <project-directory>", file=sys.stderr)
            return 2
        try:
            root = create_project(argv[2])
        except (OSError, ValueError) as error:
            print(f"error[E5004]: {error}", file=sys.stderr)
            return 1
        print(f"created Kuro project -> {root}")
        return 0
    if cmd == "native":
        from compiler.native import NativeBackendError, build_native
        output = None
        target = None
        index = 3
        while index < len(argv):
            if argv[index] in ("-o", "--output") and index + 1 < len(argv):
                output = argv[index + 1]; index += 2
            elif argv[index] == "--target" and index + 1 < len(argv):
                target = argv[index + 1]; index += 2
            else:
                print("usage: kuro native <file.kuro> [--target TARGET] [-o <executable>]", file=sys.stderr)
                return 2
        destination = output or str(Path(argv[2]).with_suffix(""))
        result = compile_source(Path(argv[2]).read_text(encoding="utf-8"), argv[2])
        if not result.ok:
            print(result.diags.render_all(), file=sys.stderr)
            return 1
        try:
            build_native(result.ir, destination, target=target)
        except (OSError, subprocess.SubprocessError, NativeBackendError) as error:
            print(f"error[E8001]: {error}", file=sys.stderr)
            return 1
        print(f"{argv[2]}: native executable -> {destination}")
        return 0
    if cmd in ("native-compiler", "native-runtime"):
        from compiler.native import NativeBackendError, build_native
        from compiler.self_host import SelfHostError, build_native_compiler, build_native_runtime
        output = None
        target = None
        index = 3
        while index < len(argv):
            if argv[index] in ("-o", "--output") and index + 1 < len(argv):
                output = argv[index + 1]; index += 2
            elif argv[index] == "--target" and index + 1 < len(argv):
                target = argv[index + 1]; index += 2
            else:
                print(f"usage: kuro {cmd} <file.kuro> [--target TARGET] [-o <executable>]", file=sys.stderr)
                return 2
        destination = output or str(Path(argv[2]).with_suffix(""))
        try:
            builder = build_native_compiler if cmd == "native-compiler" else build_native_runtime
            builder(None, destination, target=target)
        except (OSError, subprocess.SubprocessError, NativeBackendError, SelfHostError) as error:
            print(f"error[E8004]: {error}", file=sys.stderr)
            return 1
        print(f"{argv[2]}: {cmd} executable -> {destination}")
        return 0
    if cmd == "self-host":
        from compiler.self_host import SelfHostError, compile_with_kuro_driver
        if len(argv) != 3:
            print("usage: kuro self-host <file.kuro>", file=sys.stderr)
            return 2
        try:
            env = compile_with_kuro_driver(Path(argv[2]).read_text(encoding="utf-8"))
        except (OSError, SelfHostError) as error:
            print(f"error[E8003]: {error}", file=sys.stderr)
            return 1
        output = env.get("CompilerOutput", [])
        print(f"{argv[2]}: self-host compiled ({len(output)} bytecode values)")
        return 0
    if cmd == "self-host-verify":
        from compiler.self_host import SelfHostError, verify_native_compiler
        image = None
        if len(argv) == 5 and argv[3] in ("--image", "-i"):
            image = argv[4]
        elif len(argv) != 3:
            print("usage: kuro self-host-verify <file.kuro> [--image <native-compiler>]", file=sys.stderr)
            return 2
        try:
            report = verify_native_compiler(Path(argv[2]).read_text(encoding="utf-8"), image=image)
        except (OSError, SelfHostError) as error:
            print(f"error[E8006]: {error}", file=sys.stderr)
            return 1
        print(f"{argv[2]}: native/Kuro compiler parity verified ({report['instruction_count']} instructions)")
        return 0
    if cmd == "self-host-rebuild-check":
        from compiler.self_host import SelfHostError, verify_native_compiler_self_build
        image = argv[2] if len(argv) == 3 else None
        if len(argv) not in (2, 3):
            print("usage: kuro self-host-rebuild-check [native-compiler]", file=sys.stderr)
            return 2
        try:
            report = verify_native_compiler_self_build(image=image)
        except (OSError, SelfHostError) as error:
            print(f"error[E8006]: {error}", file=sys.stderr)
            return 1
        print(f"native compiler self-build verified ({report['instruction_count']} instructions)")
        return 0
    if cmd == "self-host-run":
        from compiler.self_host import SelfHostError, run_with_kuro_runtime
        if len(argv) != 3:
            print("usage: kuro self-host-run <file.kuro>", file=sys.stderr)
            return 2
        try:
            env = run_with_kuro_runtime(Path(argv[2]).read_text(encoding="utf-8"))
        except (OSError, SelfHostError) as error:
            print(f"error[E8005]: {error}", file=sys.stderr)
            return 1
        for value in env.get("VMOutput", []):
            print(value)
        return int(env.get("RuntimeExitCode", 0))
    if cmd == "repl":
        from cli.repl import repl_main
        return repl_main()
    if cmd == "version":
        from compiler import __version__

        print(f"kuro {__version__}")
        return 0
    if cmd == "test":
        if len(argv) > 3:
            print("usage: kuro test [path]", file=sys.stderr)
            return 2
        return cmd_test(argv[2] if len(argv) == 3 else ".")
    if cmd in NOT_YET_IMPLEMENTED:
        print(f"kuro {cmd}: not yet implemented ({NOT_YET_IMPLEMENTED[cmd]})", file=sys.stderr)
        return 2
    if cmd not in ("run", "check", "build", "bundle", "exec", "native-artifact", "artifact-verify", "artifact-pack", "self-host", "self-host-verify", "self-host-rebuild-check", "self-host-run", "native-compiler", "native-runtime", "package", "fmt", "lint", "emit-ir", "test"):
        print(f"kuro: unknown command {cmd!r}", file=sys.stderr)
        return 2
    if len(argv) < 3:
        print(f"usage: kuro {cmd} <file.kuro> [--output <path>]", file=sys.stderr)
        return 2
    path = argv[2]
    if cmd == "exec":
        if len(argv) != 3:
            print("usage: kuro exec <file.kuro.ir|file.kuro.app>", file=sys.stderr)
            return 2
        return cmd_exec(path)
    if cmd == "native-artifact":
        output = None
        target = None
        index = 3
        while index < len(argv):
            if argv[index] in ("-o", "--output") and index + 1 < len(argv):
                output = argv[index + 1]; index += 2
            elif argv[index] == "--target" and index + 1 < len(argv):
                target = argv[index + 1]; index += 2
            else:
                print("usage: kuro native-artifact <file.kuro.ir|file.kuro.app> [--target TARGET] [-o <executable>]", file=sys.stderr)
                return 2
        return cmd_native_artifact(path, output, target)
    if cmd == "artifact-verify":
        if len(argv) != 3:
            print("usage: kuro artifact-verify <file.kuro.ir|file.kuro.app>", file=sys.stderr)
            return 2
        return cmd_artifact_verify(path)
    if cmd == "artifact-pack":
        output = None
        if len(argv) == 5 and argv[3] in ("-o", "--output"):
            output = argv[4]
        elif len(argv) != 3:
            print("usage: kuro artifact-pack <file.kuro.ir|file.kuro.app> [-o <file.kuro.bin>]", file=sys.stderr)
            return 2
        return cmd_artifact_pack(path, output)
    if cmd == "run":
        return cmd_run(path)
    if cmd == "check":
        return cmd_check(path)
    if cmd == "build":
        output = None
        if len(argv) == 5 and argv[3] in ("-o", "--output"):
            output = argv[4]
        elif len(argv) != 3:
            print("usage: kuro build <file.kuro> [--output <path>]", file=sys.stderr)
            return 2
        return cmd_build(path, output)
    if cmd == "bundle":
        output = None
        if len(argv) == 5 and argv[3] in ("-o", "--output"):
            output = argv[4]
        elif len(argv) != 3:
            print("usage: kuro bundle <file.kuro> [--output <path>]", file=sys.stderr)
            return 2
        return cmd_bundle(path, output)
    if cmd == "package":
        return cmd_package(path)
    if cmd == "fmt":
        write = len(argv) == 4 and argv[3] in ("-w", "--write")
        if len(argv) not in (3, 4) or (len(argv) == 4 and not write):
            print("usage: kuro fmt <file.kuro> [--write]", file=sys.stderr)
            return 2
        return cmd_fmt(path, write=write)
    if cmd == "lint":
        strict = len(argv) == 4 and argv[3] in ("--strict", "-s")
        if len(argv) not in (3, 4) or (len(argv) == 4 and not strict):
            print("usage: kuro lint <file.kuro> [--strict]", file=sys.stderr)
            return 2
        return cmd_lint(path, strict=strict)
    return cmd_emit_ir(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


def entrypoint() -> None:
    """Console-script entry point used by installed Kuro environments."""
    raise SystemExit(main(sys.argv))
