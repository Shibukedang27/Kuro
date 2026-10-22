"""Native compiler regressions for malformed Print diagnostics after newlines."""
from __future__ import annotations

import platform
import subprocess

import pytest

from compiler.native import build_native
from compiler.pipeline import compile_source
from compiler.self_host import (
    build_native_artifact_launcher,
    build_native_compiler,
    compile_with_kuro_driver,
    native_compiler_source,
    run_with_kuro_runtime,
)
from test_parser_diagnostics import parse_and_get_diagnostics


LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {
    "x86_64", "amd64",
}
requires_linux_x86 = pytest.mark.skipif(
    not LINUX_X86, reason="fresh native compiler images execute Linux x86-64 only"
)


@pytest.fixture(scope="module")
def native_compiler_image(tmp_path_factory):
    """Build a fresh native compiler from the currently authored self-host stages."""
    if not LINUX_X86:
        pytest.skip("fresh native compiler fixture executes Linux x86-64 images")
    image = tmp_path_factory.mktemp("native-compiler-diagnostics") / "kuro-compiler"
    build_native_compiler(None, image, target="x86_64-linux")
    return image


@pytest.fixture(scope="module")
def native_diagnostic_probe(tmp_path_factory):
    """Build a native compiler variant that prints its first error location."""
    if not LINUX_X86:
        pytest.skip("native diagnostic probe executes Linux x86-64 images")
    source = native_compiler_source() + (
        "\nIf CompilerFailed is not equal to 0;\n"
        "    Get DiagLines 0; Print @_.\n"
        "    Get DiagCols 0; Print @_.\n"
        "Done.\n"
    )
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    image = tmp_path_factory.mktemp("native-diagnostic-location") / "kuro-compiler-probe"
    build_native(compiled.ir, image, target="x86_64-linux")
    return image


@pytest.fixture(scope="module")
def bytecode_hosted_compiler(native_compiler_image, tmp_path_factory):
    """Run the fresh compiler's own bytecode through a fresh native artifact launcher."""
    launcher = tmp_path_factory.mktemp("bytecode-hosted-compiler") / "kuro-bytecode"
    build_native_artifact_launcher(launcher, target="x86_64-linux")
    compiler_source = native_compiler_image.with_suffix(".source.kuro").read_text(
        encoding="utf-8"
    )
    self_compile = subprocess.run(
        [str(native_compiler_image)], input=compiler_source, text=True,
        capture_output=True, check=False, timeout=30,
    )
    assert (self_compile.returncode, self_compile.stderr) == (0, "")
    assert self_compile.stdout.startswith("kuro.bytecode/1\n")
    return launcher, self_compile.stdout


MALFORMED_PRINT = [
    ("\nPrint 1;", ["E2002"], [2], [8]),
    ("\nPrint;", ["E2003", "E2002"], [2, 2], [6, 6]),
    ("\nPrint", ["E2003", "E2002"], [2, 2], [6, 6]),
    ("\nPrint 1 +;", ["E2003", "E2002"], [2, 2], [10, 10]),
]


@pytest.mark.parametrize(
    "source,expected_codes,expected_lines,expected_cols",
    MALFORMED_PRINT,
    ids=["missing-period", "missing-operand", "unexpected-eof", "bad-expression"],
)
def test_fresh_native_compiler_rejects_malformed_print_after_newline(
    source, expected_codes, expected_lines, expected_cols, native_compiler_image,
):
    completed = subprocess.run(
        [str(native_compiler_image)], input=source, text=True, capture_output=True,
        check=False, timeout=30,
    )
    assert (completed.returncode, completed.stdout, completed.stderr) == (
        1, "kuro.compile-error/1\n", "",
    )


@requires_linux_x86
def test_fresh_native_compiler_rejects_print_semicolon_without_prior_newline(
    native_compiler_image,
):
    completed = subprocess.run(
        [str(native_compiler_image)], input="Print 1;", text=True,
        capture_output=True, check=False, timeout=30,
    )
    assert (completed.returncode, completed.stdout, completed.stderr) == (
        1, "kuro.compile-error/1\n", "",
    )


@pytest.mark.parametrize(
    "source,expected_codes,expected_lines,expected_cols",
    MALFORMED_PRINT,
    ids=["missing-period", "missing-operand", "unexpected-eof", "bad-expression"],
)
def test_parser_reports_structured_print_diagnostic_codes_and_locations(
    source, expected_codes, expected_lines, expected_cols,
):
    diagnostics = parse_and_get_diagnostics(source)
    assert diagnostics["parse_failed"] == 1
    assert diagnostics["codes"] == expected_codes
    assert diagnostics["lines"] == expected_lines
    assert diagnostics["cols"] == expected_cols
    assert all(diagnostics["messages"])


@pytest.mark.parametrize(
    "source,expected_codes,expected_lines,expected_cols",
    MALFORMED_PRINT,
    ids=["missing-period", "missing-operand", "unexpected-eof", "bad-expression"],
)
def test_fresh_native_compiler_preserves_print_diagnostic_location(
    source, expected_codes, expected_lines, expected_cols, native_diagnostic_probe,
):
    del expected_codes  # The native probe exposes numeric locations; codes are asserted portably above.
    completed = subprocess.run(
        [str(native_diagnostic_probe)], input=source, text=True,
        capture_output=True, check=False, timeout=30,
    )
    assert (completed.returncode, completed.stdout, completed.stderr) == (
        1,
        "kuro.compile-error/1\n"
        f"{expected_lines[0]}\n{expected_cols[0]}\n",
        "",
    )


@requires_linux_x86
def test_bytecode_hosted_self_compiler_rejects_print_semicolon_after_newline(
    bytecode_hosted_compiler,
):
    launcher, compiler_bytecode = bytecode_hosted_compiler
    completed = subprocess.run(
        [str(launcher)],
        input=compiler_bytecode + "kuro.input/1\n\nPrint 1;",
        text=True, capture_output=True, check=False, timeout=120,
    )
    # The artifact launcher preserves its current runtime exit convention (0
    # for a compiler-published error frame); the compiler must not crash or
    # publish bytecode for this malformed source.
    assert (completed.returncode, completed.stdout, completed.stderr) == (
        0, "kuro.compile-error/1\n", "",
    )


def test_repeated_integer_collection_lengths_keep_native_hosted_and_authored_vm_parity(
    native_compiler_image,
):
    source = (
        "Short = 11, 22;\nLong = 1, 2, 3, 4;\n"
        "Length Long; Length Short; Print @_.\n"
        "Length Long; Print @_.\nLength Short; Print @_.\n"
    )
    native = subprocess.run(
        [str(native_compiler_image)], input=source, text=True,
        capture_output=True, check=False, timeout=30,
    )
    assert (native.returncode, native.stderr) == (0, "")
    assert native.stdout.startswith("kuro.bytecode/1\n")
    tokens = native.stdout.splitlines()[1:]
    assert tokens

    hosted = compile_with_kuro_driver(source)
    assert hosted["CompilerFailed"] == 0
    assert hosted["CompilerOutput"] == tokens
    assert hosted["CompilerInstructionCount"] == len(tokens)
    assert tokens.count("BC_LENGTH") == 4
    assert tokens.count("BC_PRINT") == 3

    authored_vm = run_with_kuro_runtime(source)
    assert authored_vm["VMFailed"] == 0
    assert authored_vm["VMOutput"] == [2, 4, 2]
