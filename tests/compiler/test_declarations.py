from compiler.pipeline import compile_source, run_source


def test_record_and_enum_declarations_are_part_of_the_type_environment():
    result = run_source(
        'Record User Name: Text, Age: Integers;\n'
        'Enum Color Red, Green;\n'
        'Person is User;\n'
        'Choice is Color;\n'
        'Print "declared".\n'
    )
    assert result.ok
    assert result.stdout == "declared\n"


def test_duplicate_record_and_enum_names_are_rejected():
    result = compile_source("Record Item;\nEnum Item One;\n")
    assert not result.ok
    assert any(d.code == "E4002" for d in result.diags.diagnostics)


def test_record_fields_and_enum_variants_are_checked_statically():
    bad_record = compile_source(
        'Record User Name: Text;\n'
        'Person is User;\n'
        'Call MakeRecord "User";\n'
        'Call RecordSet Person, "missing", "x";\n'
    )
    assert not bad_record.ok
    assert any(d.code == "E3015" for d in bad_record.diags.diagnostics)

    bad_enum = compile_source('Enum Color Red, Green;\nCall MakeEnum "Color", "Blue";\n')
    assert not bad_enum.ok
    assert any(d.code == "E3014" for d in bad_enum.diags.diagnostics)
