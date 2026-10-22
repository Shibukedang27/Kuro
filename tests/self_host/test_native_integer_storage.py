"""Actual Kuro-owned generator storage, not the Python-authored native emitter."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess

import pytest

from test_native_codegen import x86_linux_codegen
from test_native_collection_bounds import _logical_runtimes
from test_native_indexed_state_contract import compiler_tokens, frame_artifact

LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}
requires_linux = pytest.mark.skipif(not LINUX_X86, reason="executes generated Linux x86-64 image")

# Horner construction never overflows on the way to the signed endpoint, so
# bounds failures cannot be mistaken for an earlier arithmetic-overflow exit.
MAX_INDEX = "127"
for _ in range(7):
    MAX_INDEX = f"({MAX_INDEX} * 256 + 255)"
MIN_INDEX = "(0 - EndpointMaximum - 1)"
assert eval(MAX_INDEX) == (1 << 63) - 1
assert eval(MIN_INDEX, {"EndpointMaximum": (1 << 63) - 1}) == -(1 << 63)


def endpoint_setup(expression):
    # Keep the explicit scalar endpoint construction as an independent witness.
    return f"EndpointMaximum = {MAX_INDEX};\n" if "EndpointMaximum" in str(expression) else ""


def generate(generator, tokens, tmp_path):
    wire = frame_artifact(tokens)
    generated = subprocess.run([str(generator)], input=wire, text=True,
                               capture_output=True, timeout=30)
    (tmp_path / "submitted.bc").write_text(wire, encoding="utf-8")
    (tmp_path / "generated.s").write_text(generated.stdout, encoding="utf-8")
    return generated


def execute(generator, source, tmp_path, *, tokens=None):
    if tokens is None:
        tokens = compiler_tokens(source)
    generated = generate(generator, tokens, tmp_path)
    assert (generated.returncode, generated.stderr) == (0, "")
    assert generated.stdout
    image = tmp_path / "integer-storage"
    subprocess.run(["clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib",
                    "-Wl,-e,_start", "-x", "assembler", "-", "-o", str(image)],
                   input=generated.stdout, text=True, capture_output=True, check=True)
    undefined = subprocess.run(["nm", "-u", str(image)], text=True,
                               capture_output=True, check=True)
    assert undefined.stdout.strip() == ""
    result = subprocess.run([str(image)], text=True, capture_output=True, timeout=5)
    (tmp_path / "execution.json").write_text(json.dumps({
        "generator_sha256": hashlib.sha256(generator.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "assembly_sha256": hashlib.sha256(generated.stdout.encode()).hexdigest(),
        "image_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
        "exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
        "bootstrap": "Python-hosted generator seed; external clang assembler/linker",
    }, indent=2) + "\n", encoding="utf-8")
    return result


def access_source(operation, index):
    if operation == "get":
        access = f"Get Items {index};\nPrint @_.\n"
    else:
        access = (f"Set Items {index} to 99;\n"
                  "Get Items 0;\nPrint @_.\nGet Items 1;\nPrint @_.\n")
    return "Items = 11, 22;\n" + endpoint_setup(index) + access


@requires_linux
@pytest.mark.parametrize("operation,index,expected", [
    ("get", 0, "11\n"), ("get", 1, "22\n"),
    ("get", -2, "11\n"), ("get", -1, "22\n"),
    ("set", 0, "99\n22\n"), ("set", 1, "11\n99\n"),
])
def test_actual_generator_integer_storage_valid(tmp_path, x86_linux_codegen, operation, index, expected):
    source = access_source(operation, index)
    logical = _logical_runtimes(source)
    assert all(runtime["stdout"] == expected for runtime in logical.values())
    assert logical["hosted"]["error"] is None
    assert logical["bytecode"]["error"] is None
    assert not logical["kuro_vm"]["failed"]
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
@pytest.mark.parametrize("operation,index", [
    ("get", -3), ("get", 2), ("get", 63),
    ("get", MAX_INDEX), ("get", MIN_INDEX),
    ("set", -1), ("set", 2), ("set", 63),
    ("set", MAX_INDEX), ("set", MIN_INDEX),
])
def test_actual_generator_integer_storage_runtime_bounds(tmp_path, x86_linux_codegen, operation, index):
    source = access_source(operation, index)
    logical = _logical_runtimes(source)
    assert logical["hosted"]["error"][0] == "E6001"
    assert logical["bytecode"]["error"][0] == "E6001"
    assert logical["kuro_vm"]["failed"]
    assert all(runtime["stdout"] == "" for runtime in logical.values())
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (1, "", "")


UNSUPPORTED_SOURCES = [
    ('text-elements', 'Items = "left", "right";\nGet Items 0;\nPrint @_.\n'),
    ('decimal-elements', 'Items = 1.5, 2.5;\nGet Items 0;\nPrint @_.\n'),
    ('text-set', 'Items = 11, 22;\nSet Items 0 to "wrong";\n'),
    ('decimal-set', 'Items = 11, 22;\nSet Items 0 to 1.5;\n'),
    ('decimal-index', 'Items = 11, 22;\nGet Items 0.5;\nPrint @_.\n'),
    ('text-index', 'Items = 11, 22;\nGet Items "0";\nPrint @_.\n'),
    ('alias', 'Items = 11, 22;\nAlias = Items;\nGet Alias 0;\nPrint @_.\n'),
    ('append', 'Items = 11, 22;\nAppend 33 to Items;\nGet Items 2;\nPrint @_.\n'),
    ('scalar-length', 'Items = 11, 22;\nCount = 2;\nLength Count;\nPrint @_.\n'),
    ('conditional-init', 'If 1 is equal to 1;\nItems = 11, 22;\nDone.\nGet Items 0;\nPrint @_.\n'),
    ('repeat-init', 'Repeat 1;\nItems = 11, 22;\nDone.\nGet Items 0;\nPrint @_.\n'),
    ('capture', 'Items = 11, 22;\nAction Read;\nGet Items 0;\nReturn @_;\nDone.\nCall Read;\nPrint @_.\n'),
]


@requires_linux
@pytest.mark.parametrize('name,source', UNSUPPORTED_SOURCES, ids=[case[0] for case in UNSUPPORTED_SOURCES])
def test_actual_generator_integer_storage_unsupported_rejects(tmp_path, x86_linux_codegen, name, source):
    result = generate(x86_linux_codegen, compiler_tokens(source), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (1, '', '')


INITIALIZATION = ['BC_MULTI_BEGIN', 'BC_CONST', '11', 'BC_CONST', '22', 'BC_STORE_MULTI', 'Items']
MALFORMED_SUFFIXES = [
    ['BC_CONST', '0', 'BC_GET', 'Items'],
    ['BC_CONST', '0', 'BC_GET', 'Items', '0'],
    ['BC_CONST', '0', 'BC_GET', 'Items', '2'],
    ['BC_GET', 'Items', '1'],
    ['BC_CONST', '0', 'BC_SET', 'Items'],
    ['BC_CONST', '0', 'BC_CONST', '7', 'BC_SET'],
    ['BC_CONST', '0', 'BC_GET', 'Unknown', '1'],
    ['BC_CONST', '0', 'BC_CONST', '7', 'BC_SET', 'Unknown'],
    ['BC_LOADVAR', 'Items', 'BC_PRINT'],
    ['BC_CONST', '3', 'BC_STORE_LIST', 'Items'],
    ['BC_CONST', '3', 'BC_UPDATE', 'Items'],
    ['BC_CONST', '3', 'BC_ADD', 'Items'],
]


@requires_linux
@pytest.mark.parametrize('suffix', MALFORMED_SUFFIXES, ids=[f'raw-{i}' for i in range(len(MALFORMED_SUFFIXES))])
def test_actual_generator_integer_storage_raw_boundary(tmp_path, x86_linux_codegen, suffix):
    result = generate(x86_linux_codegen, INITIALIZATION + suffix, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (1, '', '')


@requires_linux
def test_actual_generator_bounded_indexed_state(tmp_path, x86_linux_codegen):
    source = ("Masks = " + ", ".join(["1"] * 16) + ";\n"
              "Snapshots = " + ", ".join(["1"] * 16) + ";\n"
              "Slot = 15;\nFrame = 3;\nPosition = Frame * 4 + 3;\n"
              "Set Masks Slot to 4;\nSet Snapshots Position to 2;\n"
              "Get Masks Slot;\nPrint @_.\nGet Snapshots Position;\nPrint @_.\n"
              "Get Masks 0;\nPrint @_.\nGet Snapshots 0;\nPrint @_.\n")
    expected = "4\n2\n1\n1\n"
    assert all(runtime["stdout"] == expected for runtime in _logical_runtimes(source).values())
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
@pytest.mark.parametrize('name', ['target', 't0', '__bag', 'Items'])
def test_actual_generator_owner_names_are_not_pointer_heuristics(tmp_path, x86_linux_codegen, name):
    source = (f'{name} = 11, 22;\nOther = 33, 44, 55;\n'
              f'Set {name} 0 to 99;\nGet {name} -1;\nPrint @_.\n'
              'Get Other -3;\nPrint @_.\nGet Other 2;\nPrint @_.\n'
              f'Get {name} 0;\nPrint @_.\n')
    expected = '22\n33\n55\n99\n'
    assert all(runtime['stdout'] == expected for runtime in _logical_runtimes(source).values())
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, '')


@requires_linux
@pytest.mark.parametrize('count', [32, 33])
def test_actual_generator_previous_cell_capacity_is_accepted(tmp_path, x86_linux_codegen, count):
    source = 'Items = ' + ', '.join(str(i) for i in range(count)) + ';\nGet Items 31;\nPrint @_.\n'
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, '31\n', '')


@requires_linux
def test_actual_generator_sixteen_small_owners(tmp_path, x86_linux_codegen):
    source = ''.join(f'Owner{i} = {i}, {i + 1};\n' for i in range(16))
    source += 'Set Owner15 1 to 99;\nGet Owner0 0;\nPrint @_.\nGet Owner15 -1;\nPrint @_.\n'
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, '0\n99\n', '')


@requires_linux
@pytest.mark.parametrize('count', [15, 16])
def test_actual_generator_scalar_metadata_capacity(tmp_path, x86_linux_codegen, count):
    # GET's compiler-generated '_' is a real scalar slot, not collection storage.
    source = 'Items = 11, 22;\n' + ''.join(f'Scalar{i} = {i};\n' for i in range(count))
    source += 'Get Items 0;\nPrint @_.\nPrint Scalar14.\n'
    if count == 15:
        result = execute(x86_linux_codegen, source, tmp_path)
        assert (result.returncode, result.stdout, result.stderr) == (0, '11\n14\n', '')
    else:
        result = generate(x86_linux_codegen, compiler_tokens(source), tmp_path)
        assert (result.returncode, result.stdout, result.stderr) == (1, '', '')


@requires_linux
@pytest.mark.parametrize('expression,expected', [(MAX_INDEX, '9223372036854775807\n'),
                                                (MIN_INDEX, '-9223372036854775808\n')], ids=['int64-max', 'int64-min'])
def test_actual_generator_endpoint_construction_reaches_value(tmp_path, x86_linux_codegen, expression, expected):
    source = f'Items = 11, 22;\n{endpoint_setup(expression)}Value = {expression};\nPrint Value.\n'
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, '')


@requires_linux
@pytest.mark.parametrize('value,operation', [(MAX_INDEX, '+ 1'), (MIN_INDEX, '- 1'),
                                           (MAX_INDEX, '* 2')], ids=['add-overflow', 'subtract-overflow', 'multiply-overflow'])
def test_actual_generator_arithmetic_overflow_rejects_without_wrapping(tmp_path, x86_linux_codegen, value, operation):
    source = (f'Items = 11, 22;\n{endpoint_setup(value)}EndpointValue = {value};\n'
              f'Index = EndpointValue {operation};\nGet Items Index;\nPrint @_.\n')
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (1, '', '')


@requires_linux
@pytest.mark.parametrize('tokens', [
    ['BC_MULTI_BEGIN', 'BC_STORE_MULTI', 'Items'],
    ['BC_MULTI_BEGIN', 'BC_CONST', '1', 'BC_STORE_MULTI', 'Items'],
    ['BC_MULTI_BEGIN', 'BC_CONST', '1'],
    ['BC_MULTI_BEGIN', 'BC_MULTI_BEGIN', 'BC_CONST', '1', 'BC_CONST', '2', 'BC_STORE_MULTI', 'Items'],
    INITIALIZATION + INITIALIZATION,
    INITIALIZATION + ['BC_CONST', '1', 'BC_PRINT'] + INITIALIZATION,
    INITIALIZATION + ['BC_LOADVAR', 'Unassigned', 'BC_PRINT'],
    INITIALIZATION + ['BC_CONST', '1', 'BC_CONST', '1', 'BC_BINOP', '/', 'BC_PRINT'],
    INITIALIZATION + ['BC_CONST', '1', 'BC_PRINT', 'BC_CONST', '2'],
], ids=['empty', 'singleton', 'truncated', 'nested', 'duplicate-owner', 'late-init',
        'unassigned-scalar', 'division', 'stack-residue'])
def test_actual_generator_initialization_and_grammar_boundary(tmp_path, x86_linux_codegen, tokens):
    result = generate(x86_linux_codegen, tokens, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (1, '', '')


@requires_linux
@pytest.mark.parametrize('literal', ['10000', '-10000', '+1', '-', '1;syscall', '١', '9' * 64])
@pytest.mark.parametrize('position', ['initializer', 'body'])
def test_actual_generator_literal_spellings_reject(tmp_path, x86_linux_codegen, literal, position):
    if position == 'initializer':
        tokens = ['BC_MULTI_BEGIN', 'BC_CONST', literal, 'BC_CONST', '2', 'BC_STORE_MULTI', 'Items',
                  'BC_CONST', '0', 'BC_GET', 'Items', '1', 'BC_PRINT']
    else:
        tokens = INITIALIZATION + ['BC_CONST', literal, 'BC_PRINT']
    result = generate(x86_linux_codegen, tokens, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (1, '', '')


@pytest.mark.parametrize('target', ['aarch64-macos', 'x86_64-macos'])
def test_integer_storage_target_boundary(target):
    from test_native_codegen import run_codegen
    tokens = INITIALIZATION + ['BC_CONST', '0', 'BC_GET', 'Items', '1', 'BC_PRINT']
    env = run_codegen(', '.join(json.dumps(token) for token in tokens), target=target)
    assert (env['NativeFailed'], env['NativeOut']) == (1, '')


@pytest.mark.parametrize('target', ['aarch64-macos', 'x86_64-macos', 'x86_64-linux'])
@pytest.mark.parametrize('literal', ['BC_MULTI_BEGIN', 'BC_STORE_MULTI'])
def test_scalar_text_operand_cannot_activate_integer_storage(target, literal):
    from test_native_codegen import run_codegen
    env = run_codegen(', '.join(json.dumps(token) for token in ['BC_CONST_TEXT', literal, 'BC_PRINT']), target=target)
    assert env['NativeFailed'] == 0
    assert f'.asciz "{literal}"' in env['NativeOut']


@requires_linux
@pytest.mark.parametrize('length', [4096, 4097])
def test_actual_generator_indexed_token_ceiling(tmp_path, x86_linux_codegen, length):
    tokens = INITIALIZATION + ['BC_CONST', '1', 'BC_PRINT'] * 1363
    if length == 4097:
        tokens = INITIALIZATION + ['BC_CONST', '1', 'BC_PRINT'] * 1362 + ['BC_CONST', '1', 'BC_STORE_LIST', 'Scalar']
    assert len(tokens) == length
    result = generate(x86_linux_codegen, tokens, tmp_path)
    if length == 4096:
        assert result.returncode == 0 and result.stdout and result.stderr == ''
    else:
        assert (result.returncode, result.stdout, result.stderr) == (1, '', '')


def test_nested_subtraction_lowering_preserves_source_operator():
    # Pin the exact bytecode as well as the value: this previously emitted +,+.
    from compiler.pipeline import run_source
    from test_vm_cross import run_kuro_vm_environment
    source = 'Value = 0 - (2 + 1);\nPrint Value.\n'
    hosted = run_source(source)
    assert hosted.ok and hosted.stdout == '-3\n'
    tokens = compiler_tokens(source)
    assert tokens == ['BC_CONST', '0', 'BC_CONST', '2', 'BC_CONST', '1',
                      'BC_BINOP', '+', 'BC_BINOP', '-', 'BC_STORE_LIST', 'Value',
                      'BC_LOADVAR', 'Value', 'BC_PRINT']
    vm = run_kuro_vm_environment(source)
    assert vm['VMFailed'] == 0 and vm['VMOutput'] == [-3]


@requires_linux
@pytest.mark.parametrize('body,expected', [
    ('Get Items 1 - (1 + 1);\nPrint @_.\n', '22\n'),
    ('Set Items 2 - (0 + 1) to 20 - (2 + 3);\nGet Items 1;\nPrint @_.\n', '15\n'),
    ('Value = 3 * (8 - (2 + 1));\nPrint Value.\n', '15\n'),
])
def test_actual_generator_nested_integer_expression_parity(tmp_path, x86_linux_codegen, body, expected):
    source = 'Items = 11, 22;\n' + body
    logical = _logical_runtimes(source)
    assert all(runtime['stdout'] == expected for runtime in logical.values())
    assert logical['hosted']['error'] is None and logical['bytecode']['error'] is None
    assert not logical['kuro_vm']['failed']
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, '')


@requires_linux
def test_actual_generator_nested_negative_write_still_rejects(tmp_path, x86_linux_codegen):
    # Before the parser repair this became index +1 and silently wrote a cell.
    source = 'Items = 11, 22;\nSet Items 0 - (0 + 1) to 99;\nPrint 777.\n'
    logical = _logical_runtimes(source)
    assert logical['hosted']['error'][0] == 'E6001'
    assert logical['bytecode']['error'][0] == 'E6001'
    assert logical['kuro_vm']['failed']
    assert all(runtime['stdout'] == '' for runtime in logical.values())
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (1, '', '')


def test_actual_generator_integer_storage_execution_host_boundary(tmp_path, x86_linux_codegen):
    # A Linux output ABI does not qualify a Darwin-built generator. Unsupported
    # execution hosts must reject before entry, never crash or emit partial code.
    source = 'Items = 11, 22;\nSet Items 0 to 99;\nGet Items -2;\nPrint @_.\n'
    generated = generate(x86_linux_codegen, compiler_tokens(source), tmp_path)
    if not LINUX_X86:
        assert (generated.returncode, generated.stdout, generated.stderr) == (1, '', '')
        return
    assert (generated.returncode, generated.stderr) == (0, '')
    assert '.Lku_index_array_0:' in generated.stdout
    assert 'movq %rcx, (%rdx,%rax,8)' in generated.stdout
    subprocess.run(['clang', '-target', 'x86_64-unknown-linux-gnu', '-c', '-x', 'assembler', '-',
                    '-o', str(tmp_path / 'integer-storage.o')], input=generated.stdout,
                   text=True, capture_output=True, check=True)
    assert (tmp_path / 'integer-storage.o').stat().st_size > 0


@requires_linux
@pytest.mark.parametrize('literal,expected', [('0011', '11\n'), ('09', '9\n'), ('0000', '0\n')])
def test_actual_generator_decimal_spelling_normalization(tmp_path, x86_linux_codegen, literal, expected):
    source = (f'Items = {literal}, 0022;\nGet Items 0;\nPrint @_.\n'
              f'Value = {literal};\nSet Items 1 to Value;\nGet Items 1;\nPrint @_.\n')
    logical = _logical_runtimes(source)
    assert all(runtime['stdout'] == expected * 2 for runtime in logical.values())
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected * 2, '')


@requires_linux
@pytest.mark.parametrize('literal,expected', [('-0011', '-11\n'), ('-0000', '0\n')])
def test_actual_generator_raw_signed_decimal_normalization(tmp_path, x86_linux_codegen, literal, expected):
    result = generate(x86_linux_codegen, INITIALIZATION + ['BC_CONST', literal, 'BC_PRINT'], tmp_path)
    assert (result.returncode, result.stderr) == (0, '')
    image = tmp_path / 'signed-normalization'
    subprocess.run(['clang', '-target', 'x86_64-unknown-linux-gnu', '-nostdlib', '-Wl,-e,_start',
                    '-x', 'assembler', '-', '-o', str(image)], input=result.stdout,
                   text=True, capture_output=True, check=True)
    executed = subprocess.run([str(image)], text=True, capture_output=True, timeout=5)
    assert (executed.returncode, executed.stdout, executed.stderr) == (0, expected, '')


@requires_linux
def test_actual_generator_normalization_preserves_each_decimal_digit(tmp_path, x86_linux_codegen):
    # Exercise every digit in initializer and executable constant positions, not
    # merely zero padding around a single value. The generator must preserve both.
    spellings = [f'{digit:04d}' for digit in range(10)]
    source = 'Items = ' + ', '.join(spellings) + ';\n'
    source += ''.join(f'Get Items {digit};\nPrint @_.\n' for digit in range(10))
    source += ''.join(f'Print {spelling}.\n' for spelling in spellings)
    expected = ''.join(f'{digit}\n' for digit in range(10)) * 2
    assert all(runtime['stdout'] == expected for runtime in _logical_runtimes(source).values())
    result = execute(x86_linux_codegen, source, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, '')


@pytest.mark.parametrize('output_target', ['aarch64-macos', 'x86_64-macos', 'x86_64-linux'])
@pytest.mark.parametrize('execution_target', ['unverified', 'aarch64-macos', 'x86_64-macos', 'x86_64-linux'])
def test_integer_storage_requires_qualified_execution_and_output_targets(output_target, execution_target):
    from test_native_codegen import run_codegen
    tokens = INITIALIZATION + ['BC_CONST', '0', 'BC_GET', 'Items', '1', 'BC_PRINT']
    env = run_codegen(', '.join(json.dumps(t) for t in tokens), target=output_target,
                      execution_target=execution_target)
    if output_target == execution_target == 'x86_64-linux':
        assert env['NativeFailed'] == 0 and '.quad 11, 22' in env['NativeOut']
    else:
        assert (env['NativeFailed'], env['NativeOut']) == (1, '')
