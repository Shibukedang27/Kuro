from compiler.pipeline import compile_source, run_source
from compiler.bytecode import BytecodeVM, encode_ir


SOURCE = (
    'Prefix = "Kuro ";\n'
    'Action Greet Name;\n'
    '    Return Prefix + Name;\n'
    'Done.\n'
    'Call MakeClosure "Greet";\n'
    'Call Invoke @_, "language";\n'
    'Print @_.\n'
)


def test_first_class_closure_captures_values_in_ir_vm():
    result = run_source(SOURCE)
    assert result.ok
    assert result.stdout == "Kuro language\n"


def test_first_class_closure_survives_bytecode_serialization():
    from io import StringIO

    compiled = compile_source(SOURCE)
    assert compiled.ok
    output = StringIO()
    vm = BytecodeVM(encode_ir(compiled.ir), output=output)
    vm.run()
    assert output.getvalue() == "Kuro language\n"


def test_closure_created_inside_action_captures_active_frame():
    source = (
        'Adder = 0;\n'
        'Action MakeAdder Base;\n'
        'Action AddBase Value;\n'
        'Return Base + Value;\n'
        'Done.\n'
        'Call MakeClosure "AddBase";\n'
        'Return @_;\n'
        'Done.\n'
        'Call MakeAdder 10;\nUpdate Adder to @_;\n'
        'Call Invoke Adder, 7;\nPrint @_.\n'
    )
    result = run_source(source)
    assert result.ok
    assert result.stdout == "17\n"

    from io import StringIO
    compiled = compile_source(source)
    assert compiled.ok
    output = StringIO()
    BytecodeVM(encode_ir(compiled.ir), output=output).run()
    assert output.getvalue() == "17\n"
