import io

from cli.repl import repl_main


def test_repl_preserves_state_between_inputs():
    inputs = iter(["Name = \"Kuro\";", "Print Name.", ".exit"])
    output = io.StringIO()
    assert repl_main(lambda _prompt: next(inputs), output) == 0
    assert output.getvalue() == "Kuro\n"


def test_repl_buffers_incomplete_block_until_done():
    inputs = iter(["If 1 is equal to 1;", 'Print "inside".', "Done.", ".exit"])
    prompts = []
    output = io.StringIO()

    def read_line(prompt):
        prompts.append(prompt)
        return next(inputs)

    assert repl_main(read_line, output) == 0
    assert output.getvalue() == "inside\n"
    assert prompts == ["kuro> ", "...> ", "...> ", "kuro> "]


def test_repl_discards_invalid_line_but_keeps_incomplete_block():
    inputs = iter(["If 1 is equal to 1;", "Bogus;", 'Print "recovered".', "Done.", ".exit"])
    prompts = []
    output = io.StringIO()

    def read_line(prompt):
        prompts.append(prompt)
        return next(inputs)

    assert repl_main(read_line, output) == 0
    assert "error[E2001]" in output.getvalue()
    assert output.getvalue().endswith("recovered\n")
    assert prompts == ["kuro> ", "...> ", "...> ", "...> ", "kuro> "]


def test_repl_check_and_clear():
    inputs = iter(["Name = \"Kuro\";", ".check", ".clear", ".check", ".exit"])
    output = io.StringIO()
    assert repl_main(lambda _prompt: next(inputs), output) == 0
    assert output.getvalue() == "ok\nok\n"
