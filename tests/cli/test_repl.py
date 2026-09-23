import io

from cli.repl import repl_main


def test_repl_preserves_state_between_inputs():
    inputs = iter(["Name = \"Kuro\";", "Print Name.", ".exit"])
    output = io.StringIO()
    assert repl_main(lambda _prompt: next(inputs), output) == 0
    assert output.getvalue() == "Kuro\n"


def test_repl_check_and_clear():
    inputs = iter(["Name = \"Kuro\";", ".check", ".clear", ".check", ".exit"])
    output = io.StringIO()
    assert repl_main(lambda _prompt: next(inputs), output) == 0
    assert output.getvalue() == "ok\nok\n"
