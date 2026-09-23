"""Differential tests for the Kuro-authored bytecode encoder."""
import re
from pathlib import Path

from compiler.pipeline import run_source

ROOT = Path(__file__).resolve().parents[2]
BYTECODE = ROOT / "self_host" / "bytecode.kuro"
STANDALONE_RE = re.compile(
    r"^# --- BEGIN_STANDALONE_IR.*?^# --- END_STANDALONE_IR.*?$\n?",
    re.MULTILINE | re.DOTALL,
)


def encode(ir):
    body = STANDALONE_RE.sub("", BYTECODE.read_text(encoding="utf-8"))
    values = ", ".join(f'"{v}"' for v in ir)
    generated = f'IROut = {values};\n' + body
    result = run_source(generated)
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    return result.interpreter.env.get("BytecodeOut"), result.interpreter.env.get("BytecodeFailed")


def test_bytecode_encoder_consumes_operands_by_opcode_contract():
    out, failed = encode(["CONST", "7", "STORE_LIST", "N", "PRINT"])
    assert failed in (None, 0)
    assert out == ["BC_CONST", "7", "BC_STORE_LIST", "N", "BC_PRINT"]


def test_bytecode_encoder_handles_functions_and_control_markers():
    out, failed = encode([
        "FUNC_BEGIN", "Add", "PARAM", "A", "Integers",
        "LOADVAR", "A", "RETURN", "FUNC_END",
        "CALL_BEGIN", "Add", "CONST", "3", "CALL_END",
        "IF_BEGIN", "PRINT", "ELSE_BEGIN", "IF_END",
    ])
    assert failed in (None, 0)
    assert out == [
        "BC_FUNC_BEGIN", "Add", "BC_PARAM", "A", "Integers",
        "BC_LOADVAR", "A", "BC_RETURN", "BC_FUNC_END",
        "BC_CALL_BEGIN", "Add", "BC_CONST", "3", "BC_CALL_END",
        "BC_IF_BEGIN", "BC_PRINT", "BC_ELSE_BEGIN", "BC_IF_END",
    ]


def test_bytecode_encoder_handles_data_and_declaration_instructions():
    out, failed = encode([
        "DECLTYPE", "N", "Integers", "CONST", "4", "CONST", "9",
        "CMP", "lt", "ISCLASS", "digit", "STORE_LIST", "Answer", "GET", "N", "0",
        "LENGTH", "N", "SET", "N", "INPUT", "N",
    ])
    assert failed in (None, 0)
    assert out == [
        "BC_DECLTYPE", "N", "Integers", "BC_CONST", "4", "BC_CONST", "9",
        "BC_CMP", "lt", "BC_ISCLASS", "digit", "BC_STORE_LIST", "Answer", "BC_GET", "N", "0",
        "BC_LENGTH", "N", "BC_SET", "N", "BC_INPUT", "N",
    ]
