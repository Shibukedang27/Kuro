"""Regression coverage for expression-tail operator scratch across recursion.

The Kuro parser stores ordinary Action locals globally. Parsing a parenthesized
right operand re-enters ParseTermTail/ParseFactorTail, so the pending outer
operator must be carried in the tail call's frame rather than mutable scratch.
"""
import platform
import subprocess

import pytest

from compiler.pipeline import run_source
from compiler.self_host import build_native_compiler
from test_lower_cross import lower_source
from test_native_indexed_state_contract import compiler_tokens
from test_parser_cross import kuro_ast, python_ast
from test_vm_cross import run_kuro_vm_environment


# Each postfix stream is the exact expected operand/operator order. Keeping
# that explicit makes the IR and bytecode assertions independent of parsing.
CASES = [
    ("nested-minus", "10 - (3 - 1)", ("10", "3", "1", "-", "-"), "8\n"),
    ("nested-plus-minus", "10 + (3 - 1)", ("10", "3", "1", "-", "+"), "12\n"),
    ("multiply-over-divide", "20 * (12 / 3)", ("20", "12", "3", "/", "*"), "80\n"),
    ("divide-over-multiply", "20 / (3 * 2)", ("20", "3", "2", "*", "/"), "3.3333333333333335\n"),
    ("triple-nested-factors", "2 * (3 * (4 / 2))", ("2", "3", "4", "2", "/", "*", "*"), "12\n"),
    ("triple-nested-terms", "20 - (3 + (2 - 1))", ("20", "3", "2", "1", "-", "+", "-"), "16\n"),
    ("unary-minus", "- (10 - (3 - 1))", ("0", "10", "3", "1", "-", "-", "-"), "-8\n"),
    ("left-associative-subtraction", "20 - 6 - 2", ("20", "6", "-", "2", "-"), "12\n"),
    ("left-associative-mixed-factor", "24 / 4 * 2", ("24", "4", "/", "2", "*"), "12\n"),
]


def expected_ir(postfix):
    ir = []
    for item in postfix:
        if item in ("+", "-", "*", "/"):
            ir.extend(("BINOP", item))
        else:
            ir.extend(("CONST", item))
    ir.append("PRINT")
    return ir


def expected_bytecode(postfix):
    bytecode = []
    for item in postfix:
        if item in ("+", "-", "*", "/"):
            bytecode.extend(("BC_BINOP", item))
        else:
            bytecode.extend(("BC_CONST", item))
    bytecode.append("BC_PRINT")
    return bytecode


@pytest.mark.parametrize("name, expression, postfix, expected_stdout", CASES, ids=[case[0] for case in CASES])
def test_recursive_expression_operator_state(name, expression, postfix, expected_stdout):
    source = f"Print {expression}."

    expected_ast = python_ast(source)
    actual_ast, parse_failed = kuro_ast(source)
    assert parse_failed == 0, f"self-hosted parser rejected {name}: {source!r}"
    assert actual_ast == expected_ast

    ir, lower_failed = lower_source(source)
    assert lower_failed in (None, 0)
    assert ir == expected_ir(postfix)

    assert compiler_tokens(source) == expected_bytecode(postfix)

    hosted = run_source(source)
    assert hosted.ok, hosted.compile.diags.render_all() if not hosted.compile.ok else hosted.runtime_error
    authored_vm = run_kuro_vm_environment(source)
    assert authored_vm["VMFailed"] in (None, 0)
    assert hosted.stdout == expected_stdout
    # Hosted stdout renders decimal results as text; the authored VM retains a
    # numeric value. Compare numerically so division's decimal representation
    # is covered without conflating text formatting with VM value semantics.
    assert authored_vm["VMOutput"] == [float(hosted.stdout.strip())]


LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}


@pytest.mark.skipif(not LINUX_X86, reason="fresh native compiler smoke test executes Linux x86-64 images")
def test_fresh_native_compiler_frames_recursive_expression_bytecode(tmp_path):
    source = "Print 20 / (3 * 2)."
    image = tmp_path / "kuro-compiler"
    build_native_compiler(None, image)

    completed = subprocess.run(
        [str(image)], input=source, text=True, capture_output=True, check=False, timeout=30
    )
    expected_lines = ["kuro.bytecode/1", *expected_bytecode(("20", "3", "2", "*", "/"))]
    assert (completed.returncode, completed.stdout, completed.stderr) == (
        0, "\n".join(expected_lines) + "\n", ""
    )
