from compiler.pipeline import run_source


def test_record_values_support_named_fields():
    result = run_source(
        'Call MakeRecord "User";\n'
        'Call RecordSet @_, "name", "Kuro";\n'
        'Call RecordSet @_, "version", 1;\n'
        'Call RecordGet @_, "name";\nPrint @_.\n'
    )
    assert result.ok
    assert result.stdout == "Kuro\n"


def test_enum_values_support_variant_matching():
    result = run_source(
        'Call MakeEnum "Color", "Green";\n'
        'Call EnumIs @_, "Green";\nPrint @_.\n'
    )
    assert result.ok
    assert result.stdout == "True\n"
