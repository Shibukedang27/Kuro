from compiler.pipeline import run_source


def test_nested_action_is_lifted_and_can_capture_global_state():
    result = run_source(
        'Prefix = "Kuro ";\n'
        'If 1 is equal to 1;\n'
        '    Action Greet Name;\n'
        '        Return Prefix + Name;\n'
        '    Done.\n'
        'Done.\n'
        'Call Greet "language";\nPrint @_.\n'
    )
    assert result.ok
    assert result.stdout == "Kuro language\n"
