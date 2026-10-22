"""Pin the admitted result behavior of direct native and authored-VM paths.

These are path-specific observations, not a cross-runtime semantic policy.
"""

import platform
import subprocess

import pytest

from compiler.native import NativeBackendError, build_native, emit_macos_arm64
from compiler.pipeline import compile_source, run_source
import compiler.self_host as self_host
from compiler.self_host import build_native_artifact_launcher, compile_with_kuro_driver


requires_native_backend = pytest.mark.skipif(
    platform.system() not in {"Darwin", "Linux"},
    reason="requires a supported native backend",
)


# Sources stay inside the small Action/Call/Return subset admitted by both
# native execution paths except the explicit ARM64 rejection. Output pairs are
# intentionally explicit: the
# authored VM's zero-initialized frame result differs from the Python native
# backend's direct-call/global behavior at entry and fall-through.
DIRECT_ENTRY_SOURCE = (
    "Action Seed; Return 17; Done. Action Read; Return @_; Done. "
    "Call Seed; Call Read; Print @_."
)
CASES = [
    pytest.param(
        DIRECT_ENTRY_SOURCE,
        "17\n",
        "0\n",
        "native action 'Read' reads a dynamic value",
        id="direct-entry-global-versus-authored-zero",
    ),
    pytest.param(
        "Action Read _; Return @_; Done. Call Read 17; Print @_.",
        "17\n",
        "0\n",
        None,
        id="underscore-parameter-entry-only",
    ),
    pytest.param(
        "Action Answer; Return 42; Done. "
        "Action Read _; Call Answer; Return @_; Done. "
        "Call Read 17; Print @_.",
        "42\n",
        "42\n",
        None,
        id="underscore-parameter-replaced-by-producer",
    ),
    pytest.param(
        'Action Answer; Return 42; Done. Action Outer; Call Answer; Done. '
        'Call Outer; If @_ is equal to 0; Print "zero". Else; '
        'Print "not-zero". Done.',
        "zero\n",
        "zero\n",
        None,
        id="implicit-return-zero-in-native-paths",
    ),
    pytest.param(
        "Action Answer; Return 42; Done. "
        "Action Outer; Call Answer; Print @_. Return 9; Done. "
        "Call Outer; Print @_ .",
        "42\n9\n",
        "42\n9\n",
        None,
        id="explicit-inner-publication-then-outer-return",
    ),
]


@pytest.fixture(scope="module")
def native_artifact_launcher(tmp_path_factory):
    """Build the native authored-VM launcher once for this test module."""
    executable = tmp_path_factory.mktemp("native-result-launcher") / "kuro-bytecode"
    build_native_artifact_launcher(executable)
    return executable


def _native_stream_from_authored_compiler(source: str, monkeypatch) -> str:
    """Compile source with Kuro's lexer/parser/lowerer/encoder and frame tokens.

    The line escaping here mirrors the existing native compiler entry protocol;
    these bounded fixtures contain no special framing tokens, but preserve the
    general empty/control/backslash rules so the harness does not depend on
    newline-free token assumptions.
    """
    def bounded_run(text):
        instructions = 0

        def trace(_instruction, _environment, _depth, _pc):
            nonlocal instructions
            instructions += 1
            assert instructions <= 2_000_000, "authored compiler instruction budget exhausted"

        result = run_source(text, trace=trace, max_while_iterations=10_000)
        assert result.ok, (
            result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
        )
        assert result.interpreter.frames == []
        return result

    monkeypatch.setattr(self_host, "run_source", bounded_run)
    environment = compile_with_kuro_driver(source)
    tokens = environment["CompilerOutput"]

    def escape(token):
        token = str(token)
        if token == "":
            return r"\e"
        if token == "kuro.input/1":
            return r"\i"
        return (
            token.replace("\\", "\\\\")
            .replace("\n", r"\n")
            .replace("\r", r"\r")
            .replace("\t", r"\t")
        )

    return "kuro.bytecode/1\n" + "\n".join(escape(token) for token in tokens) + "\n"


@requires_native_backend
@pytest.mark.parametrize(
    "source, expected_python_native, expected_authored_vm, arm64_error",
    CASES,
)
def test_native_paths_publish_results_as_admitted(
    monkeypatch,
    tmp_path,
    native_artifact_launcher,
    source,
    expected_python_native,
    expected_authored_vm,
    arm64_error,
):
    """Compare execution of hosted-compiled native code and authored bytecode."""
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()

    executable = tmp_path / "program"
    macos_arm64 = (
        platform.system() == "Darwin"
        and platform.machine().lower() in {"arm64", "aarch64"}
    )
    if macos_arm64 and arm64_error:
        with pytest.raises(NativeBackendError, match=arm64_error):
            build_native(compiled.ir, executable)
        assert not executable.exists()
    else:
        build_native(compiled.ir, executable)
        native = subprocess.run(
            [str(executable)], capture_output=True, text=True, check=False, timeout=30
        )
        assert native.returncode == 0, native.stderr
        assert native.stdout == expected_python_native

    artifact = _native_stream_from_authored_compiler(source, monkeypatch)
    launched = subprocess.run(
        [str(native_artifact_launcher)],
        input=artifact,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert launched.returncode == 0, launched.stderr
    assert launched.stdout == expected_authored_vm


def test_arm64_direct_entry_global_read_is_rejected_before_image_emission():
    # Exercise the exact CI admission boundary even on a Linux development host.
    compiled = compile_source(DIRECT_ENTRY_SOURCE)
    assert compiled.ok, compiled.diags.render_all()
    with pytest.raises(NativeBackendError, match="native action 'Read' reads a dynamic value"):
        emit_macos_arm64(compiled.ir)
