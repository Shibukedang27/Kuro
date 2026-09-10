from compiler.pipeline import run_source


def run(src, input_fn=None):
    return run_source(src, input_fn=input_fn or (lambda prompt: (_ for _ in ()).throw(AssertionError("no input"))))


def out(src, input_fn=None):
    r = run(src, input_fn)
    assert r.ok, (r.compile.diags.render_all() if not r.compile.ok else r.runtime_error)
    return r.stdout


def test_print_literal():
    assert out('Print "hello".') == "hello\n"


def test_arithmetic():
    assert out("Action Add A, B;\nReturn A + B;\nDone.\nCall Add 3, 4;\nPrint @_.") == "7\n"


def test_operator_precedence():
    assert out("Print 2 + 3 * 4.") == "14\n"
    assert out("Print (2 + 3) * 4.") == "20\n"


def test_integer_division_stays_integer_when_exact():
    assert out("Print 10 / 2.") == "5\n"


def test_division_by_zero_is_a_controlled_error():
    r = run("Print 1 / 0.")
    assert not r.ok
    assert r.runtime_error.code == "E6003"


def test_string_concatenation():
    assert out('Print "foo" + "bar".') == "foobar\n"


def test_recursion():
    src = (
        "Action Fact N;\n"
        "If N is less than or equal to 1;\n"
        "Return 1;\n"
        "Done.\n"
        "Call Fact N - 1;\n"
        "Return N * @_;\n"
        "Done.\n"
        "Call Fact 5;\n"
        "Print @_."
    )
    assert out(src) == "120\n"


def test_uncontrolled_deep_recursion_becomes_structured_error_not_a_crash():
    src = "Action Loop N;\nCall Loop N + 1;\nReturn @_;\nDone.\nCall Loop 0;"
    r = run(src)
    assert not r.ok
    assert r.runtime_error.code == "E6005"


def test_repeat_and_index():
    assert out("Repeat 3;\nPrint Index.\nDone.") == "0\n1\n2\n"


def test_get_and_length_no_longer_auto_print():
    # ADR: Get/Length only set @_, they don't print on their own (see
    # docs/architecture/current-state.md section 7).
    assert out('Name = "Kuro";\nGet Name 0;\nLength Name;') == ""
    assert out('Name = "Kuro";\nGet Name 0;\nPrint @_.') == "K\n"
    assert out('Name = "Kuro";\nLength Name;\nPrint @_.') == "4\n"


def test_set_text_and_list():
    assert out('Name = "Kuro";\nSet Name 0 to "k";\nPrint Name.') == "kuro\n"
    assert out('Names = "A", "B", "C";\nSet Names 1 to "X";\nPrint Names.') == "A\nX\nC\n"


def test_index_out_of_range_is_controlled():
    r = run('Name = "Kuro";\nGet Name 99;')
    assert not r.ok
    assert r.runtime_error.code == "E6001"


def test_append_builds_a_growable_collection():
    src = 'Tokens = "a";\nAppend "b" to Tokens;\nAppend "c" to Tokens;\nPrint Tokens.'
    assert out(src) == "a\nb\nc\n"


def test_is_class_predicates():
    src = (
        'C = "5";\n'
        "If C is digit;\n"
        'Print "yes".\n'
        "Else;\n"
        'Print "no".\n'
        "Done."
    )
    assert out(src) == "yes\n"
    src2 = src.replace('"5"', '"x"')
    assert out(src2) == "no\n"


def test_and_or_combinators():
    src = (
        "N = 5;\n"
        "If N is greater than 1 and N is less than 10;\n"
        'Print "in range".\n'
        "Done."
    )
    assert out(src) == "in range\n"


def test_globals_visible_and_mutable_inside_actions():
    # matches bootstrap scoping: Update inside an Action writes the global.
    src = (
        "Counter is Integers;\nCounter = 0;\n"
        "Action Bump;\nUpdate Counter to 99;\nReturn Counter;\nDone.\n"
        "Call Bump;\nPrint Counter."
    )
    assert out(src) == "99\n"


def test_nested_if_inside_repeat():
    src = (
        "Repeat 3;\n"
        "If Index is greater than 0;\n"
        "Print Index.\n"
        "Done.\n"
        "Done."
    )
    assert out(src) == "1\n2\n"


def test_take_input_reads_and_converts():
    values = iter(["42"])
    src = "Age is Integers;\nTake user Age;\nPrint Age."
    r = run(src, input_fn=lambda prompt: next(values))
    assert r.ok
    assert r.stdout == "42\n"


def test_while_basic_loop():
    src = "N is Integers;\nN = 0;\nWhile N is less than 3;\nPrint N.\nAdd 1 to N;\nDone."
    assert out(src) == "0\n1\n2\n"


def test_while_runs_zero_times_when_condition_starts_false():
    src = "N is Integers;\nN = 5;\nWhile N is less than 3;\nPrint N.\nDone."
    assert out(src) == ""


def test_while_and_or_condition_runtime():
    src = (
        "N is Integers;\nN = 0;\n"
        "While N is greater than -1 and N is less than 3;\nPrint N.\nAdd 1 to N;\nDone."
    )
    assert out(src) == "0\n1\n2\n"


def test_while_variable_first_assigned_inside_it_visible_after():
    src = "N is Integers;\nN = 0;\nWhile N is less than 3;\nX = N;\nAdd 1 to N;\nDone.\nPrint X."
    assert out(src) == "2\n"


def test_nested_while_independent_counters():
    src = (
        "A is Integers;\nA = 0;\n"
        "While A is less than 2;\n"
        "B is Integers;\nB = 0;\n"
        "While B is less than 2;\n"
        "Print B.\nAdd 1 to B;\n"
        "Done.\n"
        "Add 1 to A;\n"
        "Done."
    )
    assert out(src) == "0\n1\n0\n1\n"


def test_while_flag_pattern_replaces_lexer_style_padded_repeat():
    # The exact idiom ADR-0009 says should now be O(n) instead of the
    # padded O(n^2) Repeat-plus-flag pattern self_host/lexer.kuro used.
    src = (
        'Buf = "";\nPos = 0;\nLen = 5;\nScanning = 1;\n'
        "While Scanning is equal to 1 and Pos is less than Len;\n"
        'Buf = Buf + "x";\nAdd 1 to Pos;\n'
        "Done.\n"
        "Print Buf."
    )
    assert out(src) == "xxxxx\n"


def test_infinite_while_raises_structured_error_not_a_hang():
    r = run_source(
        "Forever = 1;\nWhile Forever is equal to 1;\nAdd 0 to Forever;\nDone.",
        max_while_iterations=1000,
    )
    assert not r.ok
    assert r.runtime_error.code == "E6006"


def test_while_iteration_cap_is_per_loop_not_global():
    # Two sequential (not nested) small While loops, each well under the
    # cap, must not accumulate against a shared counter.
    r = run_source(
        "A is Integers;\nA = 0;\n"
        "While A is less than 5;\nAdd 1 to A;\nDone.\n"
        "B is Integers;\nB = 0;\n"
        "While B is less than 5;\nAdd 1 to B;\nDone.\n"
        "Print A + B.",
        max_while_iterations=10,
    )
    assert r.ok, r.runtime_error
    assert r.stdout == "10\n"


def test_repeat_negative_count_is_a_controlled_error():
    r = run("Repeat -1;\nPrint Index.\nDone.")
    assert not r.ok
    assert r.runtime_error.code == "E6004"


def test_take_input_invalid_conversion_is_controlled_error():
    r = run("Age is Integers;\nTake user Age;", input_fn=lambda prompt: "not-a-number")
    assert not r.ok
    assert r.runtime_error.code == "E6002"
