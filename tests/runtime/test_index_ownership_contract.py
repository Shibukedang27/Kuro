"""Reference-only characterization of current captured Index ownership.

These source-compiled cases record current interpreter compatibility behavior,
not a normative semantic contract or a parity claim about other runtimes.
"""
import io

from compiler.interpreter import Interpreter
from compiler.pipeline import compile_source
from compiler.values import ClosureValue

_BUDGET = 10_000


def run_bounded(source, *, initial_env=None):
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    steps = 0

    def trace(_instruction, _environment, _depth, _pc):
        nonlocal steps
        steps += 1
        assert steps <= _BUDGET, "Index ownership compatibility budget exhausted"

    output = io.StringIO()
    runtime = Interpreter(compiled.ir, output=output, trace=trace)
    runtime.env.update(initial_env or {})
    dollar_globals_before = {
        name: value for name, value in runtime.env.items() if name.endswith("$")
    }
    runtime.run()
    assert runtime.frames == []
    assert {
        name: value for name, value in runtime.env.items() if name.endswith("$")
    } == dollar_globals_before
    return output.getvalue(), runtime


def test_current_compatibility_characterization_omits_absent_index_from_capture():
    output, runtime = run_bounded(
        'Index is Integers;\n'
        'Action Reader Dummy;\nReturn Index;\nDone.\n'
        'Call MakeClosure "Reader";\nHandle = @_;\n'
        'Update Index to 9;\nCall Invoke Handle, 0;\nPrint @_.',
        initial_env={"Marker": 4},
    )
    assert output == "9\n"
    assert isinstance(runtime.env["Handle"], ClosureValue)
    assert runtime.env["Handle"].captured == {"Marker": 4}
    assert runtime.env["Index"] == 9


def test_current_compatibility_characterization_snapshots_present_global_index():
    output, runtime = run_bounded(
        'Index is Integers;\n'
        'Action Reader Dummy;\nReturn Index;\nDone.\n'
        'Call MakeClosure "Reader";\nHandle = @_;\n'
        'Update Index to 99;\nCall Invoke Handle, 0;\nPrint @_.',
        initial_env={"Index": 41},
    )
    assert output == "41\n"
    assert runtime.env["Index"] == 99
    assert runtime.env["Handle"].captured == {"Index": 41}


def test_current_compatibility_characterization_capture_beats_repeat_index_writes():
    output, runtime = run_bounded(
        'Index is Integers;\n'
        'Action Reader Dummy;\nRepeat 2;\nPrint Index.\nDone.\n'
        'Return Index;\nDone.\n'
        'Call MakeClosure "Reader";\nHandle = @_;\n'
        'Call Invoke Handle, 0;\nPrint @_.',
        initial_env={"Index": 41},
    )
    assert output == "41\n41\n41\n"
    assert runtime.env["Index"] == 41
    assert runtime.env["Handle"].captured == {"Index": 41}


def test_current_compatibility_characterization_index_parameter_overrides_capture():
    output, runtime = run_bounded(
        'Index is Integers;\n'
        'Action Reader Index;\nReturn Index;\nDone.\n'
        'Call MakeClosure "Reader";\nHandle = @_;\n'
        'Call Invoke Handle, 7;\nPrint @_.',
        initial_env={"Index": 41},
    )
    assert output == "7\n"
    assert runtime.env["Handle"].captured == {"Index": 41}
    assert runtime.env["Index"] == 41


def test_current_compatibility_characterization_direct_call_and_closure_read_top_frame():
    output, runtime = run_bounded(
        'Index is Integers;\n'
        'Action Inner Dummy;\nReturn Index;\nDone.\n'
        'Action Outer Index;\nCall Inner 0;\nDirectResult = @_;\n'
        'Call MakeClosure "Inner";\nReturn @_;\nDone.\n'
        'Call Outer 19;\nHandle = @_;\nPrint DirectResult.\n'
        'Call Invoke Handle, 0;\nPrint @_.',
        initial_env={"Index": 5},
    )
    assert output == "5\n19\n"
    assert runtime.env["Index"] == 5
    assert runtime.env["Handle"].captured["Index"] == 19


def test_current_compatibility_characterization_nested_repeat_normal_cleanup():
    output, runtime = run_bounded(
        'Index is Integers;\n'
        'Repeat 2;\nRepeat 2;\nPrint Index.\nDone.\nDone.\nPrint Index.',
        initial_env={
            "Index": 41,
            "__repeat_i1$": 73,
            "__repeat_i2$": 89,
            "User$": 101,
        },
    )
    assert output == "0\n1\n0\n1\n41\n"
    assert runtime.env["Index"] == 41
    assert runtime.env["__repeat_i1$"] == 73
    assert runtime.env["__repeat_i2$"] == 89
    assert runtime.env["User$"] == 101


def test_current_compatibility_characterization_nested_repeat_early_return_cleanup():
    output, runtime = run_bounded(
        'Index is Integers;\n'
        'Action Escape;\nRepeat 2;\nRepeat 3;\n'
        'Return Index + 10;\nDone.\nDone.\nReturn -1;\nDone.\n'
        'Repeat 2;\nCall Escape;\nPrint Index.\nPrint @_.\nDone.\nPrint Index.',
        initial_env={
            "Index": 41,
            "__repeat_i1$": 73,
            "__repeat_i2$": 89,
            "User$": 101,
        },
    )
    assert output == "0\n10\n1\n10\n41\n"
    assert runtime.env["Index"] == 41
    assert runtime.env["__repeat_i1$"] == 73
    assert runtime.env["__repeat_i2$"] == 89
    assert runtime.env["User$"] == 101


def test_current_compatibility_characterization_nested_snapshot_prefers_top_frame():
    output, runtime = run_bounded(
        'Index is Integers;\n'
        'Action Leaf Dummy;\nReturn Index;\nDone.\n'
        'Action Inner Index;\nCall MakeClosure "Leaf";\nReturn @_;\nDone.\n'
        'Action Outer Index;\nCall Inner 22;\nReturn @_;\nDone.\n'
        'Call Outer 11;\nHandle = @_;\nCall Invoke Handle, 0;\nPrint @_.',
        initial_env={"Index": 5},
    )
    assert output == "22\n"
    assert runtime.env["Index"] == 5
    assert runtime.env["Handle"].captured["Index"] == 22
