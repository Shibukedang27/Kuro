from compiler.pipeline import compile_source, run_source


def test_generic_action_parameter_unifies_at_call_site():
    source = (
        'Action Identity<T> Value: T;\n'
        '    Return Value;\n'
        'Done.\n'
        'Call Identity 42;\nPrint @_.\n'
    )
    result = run_source(source)
    assert result.ok
    assert result.stdout == "42\n"


def test_generic_type_syntax_is_parsed_and_invalid_generic_types_rejected():
    assert compile_source("Items is List<Text>;\nPrint \"ok\".").ok
    result = compile_source("Items is Unknown<Text>;\n")
    assert not result.ok
    assert any(d.code == "E3003" for d in result.diags.diagnostics)


def test_typed_generic_lists_check_each_element():
    good = compile_source('Items: List<Text> = "a", "b";\nPrint "ok".')
    assert good.ok
    bad = compile_source('Items: List<Text> = "a", 2;\n')
    assert not bad.ok
    assert any(d.code == "E3016" for d in bad.diags.diagnostics)


def test_generic_list_action_unifies_element_type():
    source = (
        'Action First<T> Values: List<T>;\n'
        '    Get Values 0;\n'
        '    Return @_;\n'
        'Done.\n'
        'Items: List<Text> = "first", "second";\n'
        'Call First Items;\nPrint @_.\n'
    )
    result = run_source(source)
    assert result.ok
    assert result.stdout == "first\n"
