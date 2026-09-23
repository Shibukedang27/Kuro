import io

from cli.debugger import debug_main


def test_debugger_emits_instruction_trace(tmp_path):
    path = tmp_path / "main.kuro"
    path.write_text('Name = "Kuro";\nPrint Name.', encoding="utf-8")
    output = io.StringIO()
    assert debug_main(str(path), output) == 0
    trace = output.getvalue()
    assert "CONST" in trace
    assert "STORE_LIST" in trace
    assert "PRINT" in trace


def test_debugger_honors_source_breakpoint_and_step_limit(tmp_path):
    path = tmp_path / "main.kuro"
    path.write_text('Name = "Kuro";\nPrint Name.', encoding="utf-8")
    output = io.StringIO()
    assert debug_main(str(path), output, breakpoints={2}) == 0
    assert "breakpoint reached" in output.getvalue()
    output = io.StringIO()
    assert debug_main(str(path), output, max_steps=1) == 0
    assert "step limit reached" in output.getvalue()


def test_debugger_json_stream_is_editor_consumable(tmp_path):
    path = tmp_path / "main.kuro"
    path.write_text('Name = "Kuro";\nPrint Name.', encoding="utf-8")
    output = io.StringIO()
    assert debug_main(str(path), output, json_output=True) == 0
    import json
    events = [json.loads(line) for line in output.getvalue().splitlines()]
    assert events[0]["event"] == "instruction"
    assert events[0]["path"] == str(path)
    assert any(event["op"] == "PRINT" for event in events)


def test_debugger_json_watch_reports_selected_variables(tmp_path):
    path = tmp_path / "main.kuro"
    path.write_text('Count is Integers;\nCount = 2;\nPrint Count.', encoding="utf-8")
    output = io.StringIO()
    assert debug_main(str(path), output, json_output=True, watches={"Count", "Missing"}) == 0
    import json
    events = [json.loads(line) for line in output.getvalue().splitlines() if json.loads(line)["event"] == "instruction"]
    assert any(event["watches"].get("Count") == 2 for event in events)
    assert all("Missing" in event["watches"] for event in events)
