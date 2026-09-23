from compiler.profiler import profile_source
from cli.kuro import main


def test_profiler_counts_instructions_and_preserves_output():
    report = profile_source('Name = "Kuro";\nPrint Name.')
    assert report.program_output == "Kuro\n"
    assert report.instruction_counts["CONST"] == 1
    assert report.instruction_counts["STORE_LIST"] == 1
    assert report.instruction_counts["PRINT"] == 1
    assert report.elapsed_seconds >= 0
    document = report.to_dict()
    assert document["instruction_counts"]["PRINT"] == 1
    assert document["runtime_stats"]["instruction_count"] >= 3
    assert document["runtime_stats"]["action_call_count"] == 0
    assert '"max_call_depth"' in report.to_json()


def test_profile_json_cli_is_machine_readable(tmp_path, capsys):
    path = tmp_path / "main.kuro"
    path.write_text('Print "profile".', encoding="utf-8")
    assert main(["kuro", "profile", str(path), "--json"]) == 0
    import json
    document = json.loads(capsys.readouterr().out)
    assert document["program_output"] == "profile\n"
    assert document["instruction_counts"]["PRINT"] == 1


def test_profiler_reports_action_and_task_activity():
    report = profile_source(
        'Action Work Value;\nReturn Value + 1;\nDone.\n'
        'Call MakeClosure "Work";\nCall Spawn @_, 4;\nCall Await @_;\nPrint @_.\n'
    )
    assert report.program_output == "5\n"
    assert report.runtime_stats["action_call_count"] >= 3
    assert report.runtime_stats["task_count"] == 1
    assert report.runtime_stats["task_states"] == {"done": 1}
