from compiler.pipeline import run_source


def test_optional_and_result_builtins_are_real_runtime_values():
    result = run_source(
        'Call Some 7;\nPrint @_.\n'
        'Call IsSome @_;\nPrint @_.\n'
        'Call Ok "done";\nPrint @_.\n'
        'Call Unwrap @_;\nPrint @_.\n'
    )
    assert result.ok
    assert result.stdout == "Some(7)\nTrue\nOk(done)\ndone\n"


def test_none_and_err_predicates():
    result = run_source(
        'Call None;\nCall IsNone @_;\nPrint @_.\n'
        'Call Err "bad";\nCall IsErr @_;\nPrint @_.\n'
    )
    assert result.ok
    assert result.stdout == "True\nTrue\n"


def test_optional_and_result_are_nominal_declaration_types():
    result = run_source("Maybe is Optional;\nOutcome is Result;\nPrint \"types\".")
    assert result.ok
    assert result.stdout == "types\n"
