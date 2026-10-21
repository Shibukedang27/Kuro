"""Assignment list length must not consume one hosted Action frame per value."""
import pytest

from compiler.interpreter import _MAX_CALL_DEPTH
from compiler.self_host import SelfHostError, compile_with_kuro_driver
from test_parser_cross import kuro_ast, python_ast
from test_parser_diagnostics import parse_and_get_diagnostics


def values(count):
    return ", ".join(map(str, range(count)))


@pytest.mark.parametrize("count", [190, 191, 272])
@pytest.mark.parametrize("declaration", ["Items", "Items: Integers"])
def test_hosted_initializer_boundary_exact_ast_and_bytecode(count, declaration):
    # Verified #94 accepts 190 and hits E6005 at 191 for this exact program.
    source = f"{declaration} = {values(count)};\nPrint 7.\n"
    actual, failed = kuro_ast(source)
    assert failed == 0
    assert actual == python_ast(source)
    compiled = compile_with_kuro_driver(source)
    expected = ["BC_MULTI_BEGIN"]
    for value in range(count):
        expected.extend(("BC_CONST", str(value)))
    expected.extend(("BC_STORE_MULTI", "Items", "BC_CONST", "7", "BC_PRINT"))
    assert compiled["CompilerOutput"] == expected
    assert compiled["CompilerInstructionCount"] == len(expected)


@pytest.mark.parametrize("source", [
    "Items = 10 - (3 - 1), 20 * (12 / 3), -(2 + 1); Print 7.",
    'Items = "one", "two", "three"; Next = 1, 2; Print 7.',
    "Action Outer; If 1 is equal to 1; Items = 1, (2 + 3), 4; Done. "
    "Other = 5, 6; Done. Items = 7, 8; Print 9.",
    "Items = 1; Other = 2, 3; Print 4.",
])
def test_assignment_list_preserves_existing_expression_and_block_grammar(source):
    actual, failed = kuro_ast(source)
    assert failed == 0
    assert actual == python_ast(source)


@pytest.mark.parametrize("suffix,code", [
    (",;", "E2003"),
    (",", "E2003"),
    (",, 1;", "E2003"),
    (", * 1;", "E2003"),
    (", (1 + );", "E2003"),
    ("", "E2002"),
])
def test_long_malformed_initializer_stops_with_structured_diagnostic(suffix, code):
    source = f"Items = {values(272)}{suffix}"
    diagnostics = parse_and_get_diagnostics(source)
    assert diagnostics["parse_failed"] == 1
    assert diagnostics["codes"][0] == code
    assert diagnostics["lines"][0] == 1
    assert diagnostics["cols"][0] > 0
    with pytest.raises(SelfHostError, match="rejected the source"):
        compile_with_kuro_driver(source)


def test_deep_expression_still_hits_unchanged_hosted_call_guard():
    assert _MAX_CALL_DEPTH == 200
    source = "Items = " + "(" * 60 + "1" + ")" * 60 + ", 2;"
    with pytest.raises(SelfHostError, match="maximum recursion depth exceeded"):
        compile_with_kuro_driver(source)
