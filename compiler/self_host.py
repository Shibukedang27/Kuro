"""Composition of the compiler pipeline written in Kuro itself."""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

from .pipeline import run_source


class SelfHostError(ValueError):
    pass


def verify_native_compiler(source: str, image: str | Path | None = None) -> dict[str, object]:
    """Verify an existing Kuro compiler image without bootstrapping Python.

    Image construction is deliberately separate (`build_native_compiler`).
    This gate consumes only the supplied/prebuilt executable and compares its
    published bytecode stream against the Kuro-authored driver oracle.
    """
    image_path = Path(image) if image is not None else ROOT / "dist" / "kuro-compiler"
    if not image_path.is_file():
        raise SelfHostError(f"native compiler image not found: {image_path}; build it once with `kuro native-compiler`")
    completed = subprocess.run(
        [str(image_path)], input=source, text=True, capture_output=True, check=False
    )
    if completed.returncode != 0:
        raise SelfHostError(completed.stderr.strip() or "native compiler exited unsuccessfully")
    native_lines = completed.stdout.splitlines()
    if not native_lines or native_lines[0] != "kuro.bytecode/1":
        raise SelfHostError("native compiler produced no valid Kuro bytecode artifact")
    hosted = compile_with_kuro_driver(source)
    expected = [str(value) for value in hosted.get("CompilerOutput", [])]
    actual = native_lines[1:]
    if int(hosted.get("CompilerFailed", 1)) != 0 or actual != expected:
        raise SelfHostError("native compiler output differs from the Kuro-authored driver")
    return {"failed": 0, "instruction_count": len(actual)}


def verify_native_compiler_self_build(image: str | Path | None = None) -> dict[str, object]:
    """Compile the complete composed native compiler with its native image."""
    image_path = Path(image) if image is not None else ROOT / "dist" / "kuro-compiler"
    if not image_path.is_file():
        raise SelfHostError(f"native compiler image not found: {image_path}")
    completed = subprocess.run(
        [str(image_path)],
        input=native_compiler_source(),
        text=True,
        capture_output=True,
        check=False,
    )
    lines = completed.stdout.splitlines()
    if completed.returncode != 0 or not lines or lines[0] != "kuro.bytecode/1":
        raise SelfHostError(completed.stderr.strip() or "native full-source self-compile failed")
    if "BC_FUNC_BEGIN" not in lines or "BC_CALL_BEGIN" not in lines:
        raise SelfHostError("native full-source self-compile produced an incomplete artifact")
    return {"failed": 0, "instruction_count": len(lines) - 1, "self_build": True}


ROOT = Path(__file__).resolve().parents[1]
_SOURCE = re.compile(r'^Source = ".*";$', re.MULTILINE)
_TOKENS = re.compile(r"^# --- BEGIN_STANDALONE_TOKENS.*?^# --- END_STANDALONE_TOKENS.*?$\n?", re.MULTILINE | re.DOTALL)
_AST = re.compile(r"^# --- BEGIN_STANDALONE_AST.*?^# --- END_STANDALONE_AST.*?$\n?", re.MULTILINE | re.DOTALL)
_IR = re.compile(r"^# --- BEGIN_STANDALONE_IR.*?^# --- END_STANDALONE_IR.*?$\n?", re.MULTILINE | re.DOTALL)
_BYTECODE = re.compile(r"^# --- BEGIN_STANDALONE_BYTECODE.*?^# --- END_STANDALONE_BYTECODE.*?$\n?", re.MULTILINE | re.DOTALL)
_VM_INPUT_DEFAULT = re.compile(r"^# --- BEGIN_VM_INPUT_DEFAULT.*?^# --- END_VM_INPUT_DEFAULT.*?$\n?", re.MULTILINE | re.DOTALL)


def _escape(source: str) -> str:
    return source.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def compile_with_kuro_driver(source: str):
    """Compile source using the compiler stages authored in ``self_host``."""
    files = [ROOT / "self_host" / name for name in ("lexer.kuro", "parser.kuro", "lower.kuro", "bytecode.kuro", "compiler.kuro")]
    replacement = f'Source = "{_escape(source)}";'
    lexer = _SOURCE.sub(lambda _: replacement, files[0].read_text(encoding="utf-8"), count=1)
    parser = _TOKENS.sub("", files[1].read_text(encoding="utf-8"), count=1)
    lower = _AST.sub("", files[2].read_text(encoding="utf-8"), count=1)
    encoder = _IR.sub("", files[3].read_text(encoding="utf-8"), count=1)
    result = run_source("\n".join((lexer, parser, lower, encoder, files[4].read_text(encoding="utf-8"))))
    if not result.ok:
        detail = result.compile.diags.render_all() if not result.compile.ok else str(result.runtime_error)
        raise SelfHostError(detail)
    env = result.interpreter.env
    if env.get("CompilerFailed", 0) != 0:
        raise SelfHostError("Kuro-authored compiler rejected the source")
    return env


def run_with_kuro_runtime(source: str):
    """Run source through the Kuro-authored compiler stages and VM."""
    files = [ROOT / "self_host" / name for name in ("lexer.kuro", "parser.kuro", "lower.kuro", "bytecode.kuro", "vm.kuro", "runtime.kuro")]
    replacement = f'Source = "{_escape(source)}";'
    lexer = _SOURCE.sub(lambda _: replacement, files[0].read_text(encoding="utf-8"), count=1)
    parser = _TOKENS.sub("", files[1].read_text(encoding="utf-8"), count=1)
    lower = _AST.sub("", files[2].read_text(encoding="utf-8"), count=1)
    encoder = _IR.sub("", files[3].read_text(encoding="utf-8"), count=1)
    vm = _BYTECODE.sub("", files[4].read_text(encoding="utf-8"), count=1)
    result = run_source("\n".join((lexer, parser, lower, encoder, vm, files[5].read_text(encoding="utf-8"))))
    if not result.ok:
        detail = result.compile.diags.render_all() if not result.compile.ok else str(result.runtime_error)
        raise SelfHostError(detail)
    return result.interpreter.env


def build_native_runtime(source: str | None, output: str | Path, target: str | None = None):
    """Build a standalone native image from the Kuro-authored runtime.

    The hosted compiler is used only during image construction.  The returned
    executable contains the composed Kuro lexer, parser, lowerer, bytecode
    encoder, VM, and runtime entrypoint; running it does not invoke Python.
    """
    from .native import build_native
    from .pipeline import compile_source

    files = [ROOT / "self_host" / name for name in ("lexer.kuro", "parser.kuro", "lower.kuro", "bytecode.kuro", "vm.kuro", "runtime.kuro")]
    replacement = 'Source is Text;\nTake user Source;' if source is None else f'Source = "{_escape(source)}";'
    lexer = _SOURCE.sub(lambda _: replacement, files[0].read_text(encoding="utf-8"), count=1)
    # The self-host lexer historically printed its token stream as a
    # bootstrap diagnostic.  That stream is useful while cross-testing the
    # lexer, but it is not application output and must not leak from the
    # production runtime image.
    lexer = re.sub(r"(?m)^\s*Print .*$\n", "", lexer)
    parser = _TOKENS.sub("", files[1].read_text(encoding="utf-8"), count=1)
    lower = _AST.sub("", files[2].read_text(encoding="utf-8"), count=1)
    encoder = _IR.sub("", files[3].read_text(encoding="utf-8"), count=1)
    vm = _BYTECODE.sub("", files[4].read_text(encoding="utf-8"), count=1)
    result = compile_source("\n".join((lexer, parser, lower, encoder, vm, files[5].read_text(encoding="utf-8"))))
    if not result.ok:
        raise SelfHostError(result.diags.render_all())
    return build_native(result.ir, output, target=target)


def build_native_artifact_launcher(output: str | Path, target: str | None = None):
    """Build the Python-free Kuro bytecode artifact launcher.

    The executable reads a ``kuro.bytecode/1`` stream from standard input,
    validates its framing in Kuro, and executes it with the Kuro-authored VM.
    Python participates only in the bootstrap build of this native image.
    """
    from .native import build_native
    from .pipeline import compile_source

    loader = (ROOT / "self_host" / "artifact_loader.kuro").read_text(encoding="utf-8")
    vm = _BYTECODE.sub(
        "", (ROOT / "self_host" / "vm.kuro").read_text(encoding="utf-8"), count=1
    )
    vm = _VM_INPUT_DEFAULT.sub("", vm, count=1)
    runtime = (ROOT / "self_host" / "runtime.kuro").read_text(encoding="utf-8")
    result = compile_source("\n".join((loader, vm, runtime)))
    if not result.ok:
        raise SelfHostError(result.diags.render_all())
    return build_native(result.ir, output, target=target)


def build_native_codegen(
    output: str | Path, target: str | None = None,
    output_target: str = "aarch64-macos",
):
    """Build a native Kuro code generator for the selected output ABI.

    ``target`` selects the CPU/OS running the generator image; output_target
    selects the assembly it emits. These are independent when cross-building.
    """
    from .native import build_native
    from .pipeline import compile_source

    loader = (ROOT / "self_host" / "artifact_loader.kuro").read_text(encoding="utf-8")
    codegen = (ROOT / "self_host" / "native_codegen.kuro").read_text(encoding="utf-8")
    if output_target not in {"aarch64-macos", "x86_64-macos", "x86_64-linux"}:
        raise SelfHostError(f"unsupported code-generation output target: {output_target}")
    codegen = codegen.replace(
        'NativeTarget = "aarch64-macos";', f'NativeTarget = "{output_target}";', 1
    )
    result = compile_source("\n".join((loader, codegen)))
    if not result.ok:
        raise SelfHostError(result.diags.render_all())
    return build_native(result.ir, output, target=target)


def native_compiler_source(source: str | None = None) -> str:
    """Return the complete, deterministic Kuro source for the native compiler.

    Keeping composition separate from image construction gives the native
    compiler a formal self-rebuild input and prevents build-only source
    rewriting from being hidden inside the hosted backend.
    """
    files = [ROOT / "self_host" / name for name in ("lexer.kuro", "parser.kuro", "lower.kuro", "bytecode.kuro", "compiler.kuro")]
    replacement = 'Source is Text;\nTake user Source;' if source is None else f'Source = "{_escape(source)}";'
    lexer = _SOURCE.sub(lambda _: replacement, files[0].read_text(encoding="utf-8"), count=1)
    lexer = re.sub(r"(?m)^\s*Print .*$\n", "", lexer)
    parser = _TOKENS.sub("", files[1].read_text(encoding="utf-8"), count=1)
    lower = _AST.sub("", files[2].read_text(encoding="utf-8"), count=1)
    encoder = _IR.sub("", files[3].read_text(encoding="utf-8"), count=1)
    compiler = files[4].read_text(encoding="utf-8")
    if source is None:
        entrypoint = (ROOT / "self_host" / "native_compiler_entry.kuro").read_text(encoding="utf-8")
        compiler = "\n".join((compiler, entrypoint))
    return "\n".join((lexer, parser, lower, encoder, compiler))


def build_native_compiler(source: str | None, output: str | Path, target: str | None = None):
    """Build a standalone native image of the Kuro-authored compiler."""
    from .native import build_native
    from .pipeline import compile_source

    composed_source = native_compiler_source(source)
    result = compile_source(composed_source)
    if not result.ok:
        raise SelfHostError(result.diags.render_all())
    image = build_native(result.ir, output, target=target)
    if source is None:
        Path(f"{output}.source.kuro").write_text(composed_source, encoding="utf-8")
    return image
