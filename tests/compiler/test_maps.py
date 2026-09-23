from compiler.pipeline import run_source


def test_kuro_map_values_support_set_get_and_membership():
    result = run_source(
        'Store = 0;\nCall MakeMap;\nUpdate Store to @_;\n'
        'Call MapSet Store, "answer", 42;\n'
        'Call MapHas Store, "answer";\nPrint @_.\n'
        'Call MapGet Store, "answer";\nPrint @_.\n'
    )
    assert result.ok
    assert result.stdout == "True\n42\n"


def test_collection_mutation_through_action_parameter_is_shared():
    source = (
        'Action AddItem Values;\n'
        'Append "new" to Values;\n'
        'Set Values 0 to "changed";\n'
        'Return Values;\nDone.\n'
        'Items = "old", "seed";\nCall AddItem Items;\nPrint @_.\n'
    )
    result = run_source(source)
    assert result.ok
    assert result.stdout == "changed\nseed\nnew\n"


def test_bytecode_vm_preserves_collection_parameter_identity():
    from io import StringIO
    from compiler.bytecode import BytecodeVM, encode_ir
    from compiler.pipeline import compile_source

    source = (
        'Action AddItem Values;\nAppend "new" to Values;\n'
        'Set Values 0 to "changed";\nReturn Values;\nDone.\n'
        'Items = "old", "seed";\nCall AddItem Items;\nPrint @_.\n'
    )
    compiled = compile_source(source)
    assert compiled.ok
    output = StringIO()
    BytecodeVM(encode_ir(compiled.ir), output=output).run()
    assert output.getvalue() == "changed\nseed\nnew\n"
