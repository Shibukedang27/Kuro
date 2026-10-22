"""Frontend admission checks for ``Length`` in both compiler drivers.

The source compiler's Length rule runs after parsing and before lowering, so
these tests intentionally inspect authored-stage environments on rejection as
well as the public hosted/native compiler protocols.
"""
from __future__ import annotations

import platform
import subprocess

import pytest

from compiler.native import build_native
from compiler.pipeline import run_source
from compiler.self_host import (
    SelfHostError,
    build_native_artifact_launcher,
    build_native_compiler,
    compile_with_kuro_driver,
    native_compiler_source,
)


LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {
    "x86_64", "amd64",
}
requires_linux_x86 = pytest.mark.skipif(
    not LINUX_X86, reason="fresh native compiler images execute Linux x86-64 only"
)


def _composed_env(source: str) -> dict[str, object]:
    """Run lexer/parser/lengthcheck/lower/bytecode/driver without native entry."""
    result = run_source(native_compiler_source(source), filename="<length frontend>")
    assert result.ok, (
        result.compile.diags.render_all()
        if not result.compile.ok else result.runtime_error
    )
    assert result.interpreter is not None
    return result.interpreter.env


def _assert_length_rejected(source: str, line: int, col: int = 1) -> None:
    with pytest.raises(SelfHostError):
        compile_with_kuro_driver(source)

    env = _composed_env(source)
    assert env.get("CompilerFailed") == 1
    assert env.get("LengthCheckFailed") == 1
    assert env.get("DiagCodes") == ["E3009"]
    assert env.get("DiagLines") == [line]
    assert env.get("DiagCols") == [col]
    messages = env.get("DiagMessages") or []
    assert len(messages) == 1 and isinstance(messages[0], str) and messages[0]
    assert "Text" in messages[0]
    # A rule failure must stop the pipeline, not leave a plausible partial artifact.
    assert not env.get("IROut")
    assert not env.get("BytecodeOut")
    assert not env.get("CompilerOutput")


INTEGER_LENGTH_FAILURES = [
    pytest.param("N = 5;\nLength N;\nPrint @_.\n", 2, id="inferred-integer-scalar"),
    pytest.param("N = 1.5;\nLength N;\nPrint @_.\n", 2, id="inferred-decimal-scalar"),
    pytest.param("Flag is Symbols;\nFlag = 1;\nLength Flag;\nPrint @_.\n", 3, id="typed-symbol-scalar"),
    pytest.param("N is Integers;\nN = 5;\nLength N;\nPrint @_.\n", 3, id="typed-integer-scalar"),
    pytest.param("N is Decimals;\nN = 1.5;\nLength N;\nPrint @_.\n", 3, id="typed-decimal-scalar"),
    pytest.param("N is Widget;\nN = 5;\nLength N;\nPrint @_.\n", 3, id="typed-custom-scalar"),
    pytest.param("Items = 11, 22;\nLength Items;\nPrint @_.\n", 2, id="inferred-integer-collection"),
    pytest.param("Items = 1.5, 2.5;\nLength Items;\nPrint @_.\n", 2, id="inferred-decimal-collection"),
    pytest.param("Items is Integers;\nItems = 11, 22;\nLength Items;\nPrint @_.\n", 3, id="typed-integer-collection"),
    pytest.param("Items = 11, 22;\nLength Items;\nPrint @_.\n", 2, id="global-inference"),
    pytest.param("N = 5;\nLength N;\nN is Integers;\nPrint @_.\n", 2, id="forward-global-type"),
    pytest.param("Items = 11, 22;\nSet Items 0 to 99;\nLength Items;\nPrint @_.\n", 3, id="after-cell-mutation"),
    pytest.param("Items = 11, 22;\nOther = 1, 2;\nLength Items;\nLength Other;\nPrint @_.\n", 3, id="repeated-lengths"),
    pytest.param("Compare R 4 is equal to 4;\nLength R;\nPrint 0.\n", 2, id="compare-result-symbol-top-level"),
    pytest.param("If 1 is equal to 1;\nCompare R 4 is equal to 4;\nLength R;\nDone.\nPrint 0.\n", 3, id="compare-result-symbol-in-branch"),
    pytest.param("Items = 11, 22;\nIf 1 is equal to 1;\nLength Items;\nDone.\nPrint 0.\n", 3, id="inside-branch"),
    pytest.param("Items = 11, 22;\nAction Check;\nLength Items;\nDone.\nCall Check;\nPrint 0.\n", 3, id="inside-action-global"),
    pytest.param("Value is Text;\nValue = \"ok\";\nAction Check Value: Integers;\nLength Value;\nDone.\nCall Check 1;\nPrint 0.\n", 4, id="typed-parameter-shadows-text-global"),
    pytest.param("Repeat 2;\nLength Index;\nDone.\nPrint 0.\n", 2, id="repeat-index"),
    pytest.param("N: Widget = 5;\nLength N;\nPrint 0.\n", 2, id="custom-typed-assignment"),
    pytest.param("Length N;\nN is Integers;\nPrint 0.\n", 1, id="forward-declaration"),
    pytest.param("N = 5;\nN = \"hi\";\nLength N;\nPrint 0.\n", 3, id="first-type-not-last-value"),
    pytest.param("Length Flag;\nCompare Flag 1 is equal to 1;\nPrint 0.\n", 1, id="forward-compare-result"),
    pytest.param("Length is Integers;\nLength Length;\nPrint 0.\n", 2, id="length-named-target"),
    pytest.param("Action = 1;\nN = 5;\nLength N;\nPrint 0.\n", 3, id="action-name-does-not-open-block"),
    pytest.param("If = 1;\nN = 5;\nLength N;\nPrint 0.\n", 3, id="if-name-does-not-open-block"),
    pytest.param("Done = 1;\nN = 5;\nLength N;\nPrint 0.\n", 3, id="done-name-does-not-close-block"),
    pytest.param("Action Check (Value: Decimals);\nLength Value;\nDone.\nPrint 0.\n", 2, id="parenthesized-decimal-param"),
    pytest.param("Action Check Value: Symbols;\nIf 1 is equal to 1;\nLength Value;\nDone.\nDone.\nPrint 0.\n", 3, id="param-inside-nested-if"),
    pytest.param("Index is Text;\nRepeat 1;\nLength Index;\nDone.\nPrint 0.\n", 3, id="repeat-index-shadows-global"),
    pytest.param("Action Check Value: Integers;\nIf 1 is equal to 1;\nPrint 0.\nDone.\nLength Value;\nDone.\nPrint 0.\n", 5, id="typed-param-restored-after-nested-block"),
]


@pytest.mark.parametrize("source,line", INTEGER_LENGTH_FAILURES)
def test_known_nontext_length_fails_before_lowering(source: str, line: int) -> None:
    _assert_length_rejected(source, line)


def test_nested_only_inferred_name_is_not_claimed_as_a_known_nontext_length():
    # The checker is deliberately narrow: nested assignment inference is not
    # promoted into global knowledge, and no resolver/full semantic pass is enabled.
    source = "If 1 is equal to 1;\n    Local = 7;\n    Length Local;\nDone.\nPrint 0.\n"
    env = compile_with_kuro_driver(source)
    assert env["CompilerFailed"] == 0
    assert "BC_LENGTH" in env["CompilerOutput"]


@pytest.mark.parametrize("source", [
    "Alias = Items;\nLength Alias;\nPrint 0.\n",
    "N = 4;\nComputed = N + 1;\nLength Computed;\nPrint 0.\n",
    "If 1 is equal to 1;\nLocal = 3;\nDone.\nLength Local;\nPrint 0.\n",
    "Value is Integers;\nValue = 5;\nAction Check Value;\nLength Value;\nDone.\nCall Check 1;\nPrint 0.\n",
])
def test_unknown_aliases_expressions_and_out_of_scope_names_remain_unclassified(source):
    # This stage is not a replacement for ordinary name resolution/typechecking.
    env = compile_with_kuro_driver(source)
    assert env["CompilerFailed"] == 0
    assert "BC_LENGTH" in env["CompilerOutput"]


def test_parse_errors_do_not_enter_the_length_validator():
    source = "N = 5;\nLength N;\nPrint @_\n"
    env = _composed_env(source)
    assert env.get("ParseFailed") == 1
    assert env.get("LengthCheckFailed", 0) == 0
    assert env.get("CompilerFailed") == 1
    assert (env.get("DiagCodes") or [])
    assert all(code != "E3009" for code in env["DiagCodes"])


@pytest.mark.parametrize("source", [
    "Length = 5;\nPrint Length.\n",
    "Action = 1;\nPrint Action.\n",
    "Done = 1;\nPrint Done.\n",
    'Label = "Length";\nPrint Label.\n',
])
def test_keyword_like_names_and_string_contents_do_not_trigger_length_rule(source):
    env = compile_with_kuro_driver(source)
    assert env["CompilerFailed"] == 0
    assert env.get("LengthCheckFailed", 0) == 0
    assert env["CompilerOutput"]


TEXT_LENGTH_CASES = [
    pytest.param(
        'Name is Text;\nName = "Kuro";\nLength Name;\nPrint @_.\n',
        ["BC_DECLTYPE", "Name", "Text", "BC_CONST_TEXT", "Kuro", "BC_STORE_LIST", "Name", "BC_LENGTH", "Name", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT"],
        id="text-scalar",
    ),
    pytest.param(
        'Names = "A", "B";\nLength Names;\nPrint @_.\n',
        ["BC_MULTI_BEGIN", "BC_CONST_TEXT", "A", "BC_CONST_TEXT", "B", "BC_STORE_MULTI", "Names", "BC_LENGTH", "Names", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT"],
        id="text-element-collection",
    ),
    pytest.param(
        'Name = "A";\nName = Name + "B";\nLength Name;\nPrint @_.\n',
        None,
        id="text-after-reassignment",
    ),
]


@pytest.mark.parametrize("source,expected_tokens", TEXT_LENGTH_CASES)
def test_text_length_is_preserved_in_complete_bytecode(source: str, expected_tokens):
    env = compile_with_kuro_driver(source)
    tokens = [str(token) for token in env["CompilerOutput"]]
    assert env["CompilerFailed"] == 0
    assert "BC_LENGTH" in tokens
    if expected_tokens is not None:
        assert tokens == expected_tokens


def test_unknown_assignment_type_does_not_get_rejected_as_nontext():
    # An alias assignment does not carry static type evidence in this checker.
    source = "Items = 11, 22;\nAlias = Items;\nLength Alias;\nPrint 0.\n"
    env = compile_with_kuro_driver(source)
    assert env["CompilerFailed"] == 0
    assert "BC_LENGTH" in env["CompilerOutput"]


@pytest.mark.parametrize("source", [
    'Value = 5;\nAction Check Value: Text;\nLength Value;\nDone.\nPrint 0.\n',
    'Value = 5;\nAction Check Value;\nLength Value;\nDone.\nPrint 0.\n',
    'Index = "Kuro";\nRepeat 1;\nPrint Index.\nDone.\nLength Index;\nPrint @_.\n',
    'Value = "Kuro";\nAction Check Value: Integers;\nPrint Value.\nDone.\nLength Value;\nPrint @_.\n',
    'Length is Text;\nLength = "Kuro";\nLength Length;\nPrint @_.\n',
    'Compare = 5;\nLength Unknown;\nPrint 0.\n',
    'If 1 is equal to 1;\nN: Integers = 5;\nLength N;\nDone.\nPrint 0.\n',
    'Words = "Kuro";\nIf 1 is equal to 1;\nPrint 0.\nElse;\nPrint 1.\nDone.\nLength Words;\nPrint @_.\n',
    'is = 5;\nIf is greater than 0;\nN = 5;\nDone.\nLength N;\nPrint 0.\n',
    'is = 5;\nWhile is less than 0;\nN = 5;\nDone.\nLength N;\nPrint 0.\n',
])
def test_lexical_overlay_restore_and_unknown_boundaries(source):
    env = compile_with_kuro_driver(source)
    assert env["CompilerFailed"] == 0
    assert "BC_LENGTH" in env["CompilerOutput"]


@pytest.mark.parametrize("depth", [1, 3])
def test_scope_frame_storage_is_reused_instead_of_accumulating_closed_blocks(depth):
    block = "If 1 is equal to 1;\n" * depth + "Length Name;\n" + "Done.\n" * depth
    source = 'Name = "Kuro";\n' + block * 16 + "Print 0.\n"
    env = compile_with_kuro_driver(source)
    assert env["CompilerFailed"] == 0
    assert env["LCFrameTop"] == 0
    for name in ("LCFrameAction", "LCFrameRepeat"):
        assert len(env[name]) == depth


@pytest.mark.parametrize("source", [
    'Name = "Kuro";\nLength Name;\nPrint @_.\n',
    'N = 5;\nLength N;\nPrint 0.\n',
    'is = 5;\nIf is greater than 0;\nPrint 1.\nDone.\n',
])
def test_reused_declaration_lookahead_restores_parser_cursor(source):
    env = _composed_env(source)
    assert env["ParseFailed"] == 0
    assert env["TokPos"] == env["TokCount"]
    assert env["TokPos"] == env["LCBinding_SavedPos"]


@pytest.fixture(scope="module")
def fresh_native_length_compiler(tmp_path_factory):
    if not LINUX_X86:
        pytest.skip("fresh native compiler fixture executes Linux x86-64 images")
    image = tmp_path_factory.mktemp("native-length-compiler") / "kuro-compiler"
    build_native_compiler(None, image, target="x86_64-linux")
    return image


@pytest.fixture(scope="module")
def native_length_diagnostic_probe(tmp_path_factory):
    if not LINUX_X86:
        pytest.skip("native diagnostic probe executes Linux x86-64 images")
    probe_source = native_compiler_source() + (
        "\nIf CompilerFailed is not equal to 0;\n"
        "    Get DiagCodes 0; Print @_.\n"
        "    Get DiagLines 0; Print @_.\n"
        "    Get DiagCols 0; Print @_.\n"
        "    Get DiagMessages 0; Print @_.\n"
        "    Print LengthCheckFailed.\n"
        "    Length IROut; Print @_.\n"
        "    Length BytecodeOut; Print @_.\n"
        "Done.\n"
    )
    from compiler.pipeline import compile_source

    compiled = compile_source(probe_source)
    assert compiled.ok, compiled.diags.render_all()
    image = tmp_path_factory.mktemp("native-length-probe") / "kuro-length-probe"
    build_native(compiled.ir, image, target="x86_64-linux")
    return image


@requires_linux_x86
@pytest.mark.parametrize("source,line", INTEGER_LENGTH_FAILURES)
def test_fresh_native_compiler_keeps_compile_error_protocol_on_length_rejection(
    fresh_native_length_compiler, source, line,
):
    completed = subprocess.run(
        [str(fresh_native_length_compiler)], input=source, text=True,
        capture_output=True, check=False, timeout=30,
    )
    assert (completed.returncode, completed.stdout, completed.stderr) == (
        1, "kuro.compile-error/1\n", "",
    )


@requires_linux_x86
@pytest.mark.parametrize(
    "source",
    [pytest.param(case.values[0], id=case.id) for case in TEXT_LENGTH_CASES] + [
        pytest.param('Value = 5;\nAction Check Value: Text;\nLength Value;\nDone.\nPrint 0.\n', id='text-parameter-shadows-integer'),
        pytest.param('Value = 5;\nAction Check Value;\nLength Value;\nDone.\nPrint 0.\n', id='untyped-parameter-is-unknown'),
        pytest.param('Index = "Kuro";\nRepeat 1;\nPrint Index.\nDone.\nLength Index;\nPrint @_.\n', id='global-index-restored'),
        pytest.param('Items = 1, "Kuro";\nLength Items;\nPrint 0.\n', id='mixed-literals-unknown'),
        pytest.param('Items = "Kuro", 1;\nLength Items;\nPrint 0.\n', id='mixed-literals-reversed-unknown'),
        pytest.param('Items = 11, 22;\nAlias = Items;\nLength Alias;\nPrint 0.\n', id='alias-still-unknown'),
        pytest.param('is = 5;\nIf is greater than 0;\nN = 5;\nDone.\nLength N;\nPrint 0.\n', id='if-is-comparison-not-declaration'),
        pytest.param('is = 5;\nWhile is less than 0;\nN = 5;\nDone.\nLength N;\nPrint 0.\n', id='while-is-comparison-not-declaration'),
    ],
)
def test_fresh_native_compiler_preserves_complete_text_length_bytecode(
    fresh_native_length_compiler, source: str,
):
    native = subprocess.run(
        [str(fresh_native_length_compiler)], input=source, text=True,
        capture_output=True, check=False, timeout=30,
    )
    hosted = compile_with_kuro_driver(source)
    expected = [str(token) for token in hosted["CompilerOutput"]]
    assert native.returncode == 0 and native.stderr == ""
    assert native.stdout.startswith("kuro.bytecode/1\n")
    assert native.stdout.splitlines()[1:] == expected


@requires_linux_x86
def test_fresh_native_length_probe_reports_keyword_location_and_empty_stage_outputs(
    native_length_diagnostic_probe,
):
    source = "N is Integers;\nN = 5;\n    Length N;\nPrint @_.\n"
    completed = subprocess.run(
        [str(native_length_diagnostic_probe)], input=source, text=True,
        capture_output=True, check=False, timeout=30,
    )
    lines = completed.stdout.splitlines()
    assert completed.returncode == 1
    assert lines[:5] == ["kuro.compile-error/1", "E3009", "3", "5", lines[4]]
    assert lines[4] and "Text" in lines[4]
    assert lines[5:] == ["1", "0", "0"]
    assert completed.stderr == ""


@pytest.fixture(scope="module")
def bytecode_hosted_length_compiler(fresh_native_length_compiler, tmp_path_factory):
    launcher = tmp_path_factory.mktemp("length-bytecode-launcher") / "kuro-bytecode"
    build_native_artifact_launcher(launcher, target="x86_64-linux")
    source = fresh_native_length_compiler.with_suffix(".source.kuro").read_text(encoding="utf-8")
    self_compile = subprocess.run(
        [str(fresh_native_length_compiler)], input=source, text=True,
        capture_output=True, check=False, timeout=60,
    )
    assert self_compile.returncode == 0 and self_compile.stderr == ""
    assert self_compile.stdout.startswith("kuro.bytecode/1\n")
    return launcher, self_compile.stdout


@requires_linux_x86
@pytest.mark.parametrize(
    "source,expected",
    [pytest.param(case.values[0], "kuro.compile-error/1\n", id=case.id)
     for case in INTEGER_LENGTH_FAILURES] + [
        pytest.param('Name is Text;\nName = "Kuro";\nLength Name;\nPrint @_.\n', "4\n", id="accept-text"),
        pytest.param('Value = 5;\nAction Check Value: Text;\nLength Value;\nDone.\nPrint 0.\n', "0\n", id="text-param-shadows-global"),
        pytest.param('Value = 5;\nAction Check Value;\nLength Value;\nDone.\nPrint 0.\n', "0\n", id="untyped-param-shadows-global"),
    ],
)
def test_bytecode_self_compiled_full_compiler_preserves_length_admission(
    bytecode_hosted_length_compiler, source: str, expected: str,
):
    launcher, compiler_bytecode = bytecode_hosted_length_compiler
    completed = subprocess.run(
        [str(launcher)], input=compiler_bytecode + "kuro.input/1\n" + source,
        text=True, capture_output=True, check=False, timeout=120,
    )
    # The launcher executes the compiler, which publishes a frame, not the
    # user's program. Execute a successful frame separately to check its output.
    assert (completed.returncode, completed.stderr) == (0, "")
    if expected.startswith("kuro.compile-error/"):
        assert completed.stdout == expected
    else:
        assert completed.stdout.startswith("kuro.bytecode/1\n")
        executed = subprocess.run(
            [str(launcher)], input=completed.stdout, text=True,
            capture_output=True, check=False, timeout=30,
        )
        assert (executed.returncode, executed.stdout, executed.stderr) == (0, expected, "")
