from cli.kuro import cmd_test


def test_kuro_test_runner_discovers_and_runs_sources(tmp_path, capsys):
    (tmp_path / "pass.kuro").write_text('Print "ok".', encoding="utf-8")
    assert cmd_test(str(tmp_path)) == 0
    assert "tests: 1/1 passed" in capsys.readouterr().out


def test_kuro_test_runner_returns_failure_for_bad_source(tmp_path, capsys):
    (tmp_path / "bad.kuro").write_text("Print Missing.", encoding="utf-8")
    assert cmd_test(str(tmp_path)) == 1
    assert "FAIL" in capsys.readouterr().out
