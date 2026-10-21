"""Kuro-owned bounded raw-bytecode loop-use facts; hosted-bootstrap scope only."""
import json
import platform
import subprocess
from pathlib import Path

import pytest

from compiler.pipeline import compile_source, run_source
from loop_flow_facts import analyze

ROOT = Path(__file__).resolve().parents[2]
FLOW_SOURCE = Path(__file__).with_name("loop_use_flow.kuro")


def _store(value="1.5", name="Fresh"):
    return ["BC_CONST", value, "BC_STORE_LIST", name]


def _read(name="Fresh"):
    return ["BC_LOADVAR", name, "BC_PRINT"]


def _if(yes, no=None):
    return ["BC_CONST", "1", "BC_IF_BEGIN", *yes,
            *(["BC_ELSE_BEGIN", *no] if no is not None else []), "BC_IF_END"]


def _repeat(body, count="2"):
    return ["BC_CONST", count, "BC_REPEAT_BEGIN", *body, "BC_REPEAT_END"]


def _source(tokens):
    source = FLOW_SOURCE.read_text(encoding="utf-8")
    assert source.count("RawTokens is Text;") == 1
    # Kuro has no JSON-style Unicode escape decoder: preserve the actual
    # characters, including NUL, rather than testing a different ASCII name.
    appended = "\n".join(
        "Append " + json.dumps(token, ensure_ascii=False).replace(r"\u0000", "\x00")
        + " to RawTokens;" for token in tokens
    )
    if not tokens:
        appended = 'RawTokens = "";'
    source = source.replace("RawTokens is Text;", "RawTokens is Text;\n" + appended)
    return source


def _run_kuro(tokens):
    result = run_source(_source(tokens), filename="<bounded loop-use analyzer>")
    assert result.ok, (result.compile.diags.render_all(), result.runtime_error)
    lines = result.stdout.splitlines()
    if lines == ["REJECT"]:
        return None
    assert lines[-2:] in (["DECISION", "0"], ["DECISION", "1"]), result.stdout
    records = {}
    i = 0
    while i < len(lines) - 2:
        assert lines[i] == "USE", result.stdout
        pc, name, origin, mask = int(lines[i + 1]), lines[i + 2], lines[i + 3], int(lines[i + 4])
        assert name == tokens[pc + 1]
        assert tokens[pc:pc + 2] == ["BC_LOADVAR", name]
        assert origin in ("E", "B") and 0 <= mask <= 7
        key = (pc, name, origin)
        records[key] = records.get(key, 0) | mask
        i += 5
    return records, lines[-1] == "1"


def _mask(kinds):
    if kinds is None:
        return 0
    return sum({"?": 1, "I": 2, "D": 4}[kind] for kind in kinds)


def _expected(tokens):
    oracle = analyze(tokens)
    loop = oracle["loops"][0]
    records = {}
    for use in loop["uses"]:
        records[(use["pc"], use["name"], "E")] = _mask(use["entry_kinds"])
        records[(use["pc"], use["name"], "B")] = _mask(use["backedge_kinds"])
    decision = all(mask in (0, 4) for mask in records.values())
    return records, decision


@pytest.mark.parametrize("count", ["0", "1", "2", "9"])
def test_kuro_owns_raw_token_parse_and_per_use_masks_for_all_count_classes(count):
    tokens = _repeat(_read() + _store(), count)
    assert _run_kuro(tokens) == _expected(tokens)


def test_nested_arms_read_before_write_overwrite_and_missing_else():
    bodies = [
        _if(_read(), []) + _store() + _read(),
        _if([], _read()) + _store() + _read(),
        _if(_if(_read(), []), []) + _store() + _read(),
        _if(_store(), _store("2.5")) + _read(),
        _if(_store()) + _read(),
        _store("1") + _if(_read(), _read()) + _read(),
        _read() + _store("2.5") + _read(),
    ]
    for body in bodies:
        tokens = _repeat(body)
        assert _run_kuro(tokens) == _expected(tokens)


def test_optional_integer_entry_and_zero_count_unreachable_are_distinct():
    integer_entry = _store("1") + _repeat(_read() + _store())
    assert _run_kuro(integer_entry) == _expected(integer_entry)
    zero = _repeat(_read() + _store(), "0")
    result = _run_kuro(zero)
    assert result == _expected(zero)
    assert result[0] and set(result[0].values()) == {0}


@pytest.mark.parametrize("tokens", [
    ["BC_CONST"],
    ["BC_CONST", "nan", "BC_REPEAT_BEGIN", "BC_REPEAT_END"],
    ["BC_CONST", "10", "BC_REPEAT_BEGIN", "BC_REPEAT_END"],
    ["BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1.25", "BC_STORE_LIST", "Fresh", "BC_REPEAT_END"],
    ["BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST"],
    ["BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1", "BC_IF_BEGIN", "BC_ELSE_BEGIN", "BC_ELSE_BEGIN", "BC_IF_END", "BC_REPEAT_END"],
    ["BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1", "BC_IF_BEGIN", "BC_REPEAT_END", "BC_IF_END"],
    ["BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_LOADVAR", "BC_Fifth", "BC_PRINT", "BC_REPEAT_END"],
    ["BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_LOADVAR", "Fresh", "BC_CONST", "1", "BC_PRINT", "BC_REPEAT_END"],
])
def test_malformed_truncated_invalid_literals_and_unsupported_ops_fail_closed(tokens):
    assert _run_kuro(tokens) is None


def test_token_and_branch_depth_bounds_fail_closed():
    too_long = _repeat(_store() + _read(), "2") + ["BC_PRINT"] * 120
    assert len(too_long) > 128
    assert _run_kuro(too_long) is None
    deep = _read()
    for _ in range(17):
        deep = _if(deep, [])
    assert _run_kuro(_repeat(deep)) is None


@pytest.mark.skipif(platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
                    reason="native execution requires Linux x86-64")
@pytest.mark.parametrize("body, expected", [
    (_store() + _read(), "1"),
    (_if(_read(), []) + _store() + _read(), "0"),
])
def test_analyzer_itself_runs_as_hosted_bootstrap_native_image(tmp_path, body, expected):
    from compiler.native import build_native
    tokens = _repeat(body)
    compiled = compile_source(_source(tokens), filename="<native bounded flow>")
    assert compiled.ok, compiled.diags.diagnostics
    image = tmp_path / "bounded-flow"
    build_native(compiled.ir, image, target="x86_64-linux")
    result = subprocess.run([str(image)], text=True, capture_output=True, timeout=15)
    assert result.returncode == 0 and result.stderr == ""
    hosted = run_source(_source(tokens))
    assert hosted.ok
    assert result.stdout == hosted.stdout
    assert result.stdout.endswith("DECISION\n" + expected + "\n")


def test_exact_depth_and_token_bounds_are_inclusive():
    depth16 = _read()
    for _ in range(16):
        depth16 = _if(depth16, [])
    tokens = _repeat(depth16)
    assert _run_kuro(tokens) == _expected(tokens)

    exact_128 = _repeat(_if([], None) * 31)
    assert len(exact_128) == 128
    assert _run_kuro(exact_128) == _expected(exact_128)
    over_128 = _repeat(_if([], None) * 32)
    assert len(over_128) > 128
    assert _run_kuro(over_128) is None


@pytest.mark.parametrize("body", [
    ["BC_CONST", "1"],
    ["BC_CONST", "1", "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh"],
    ["BC_CONST", "1", *_read(), "BC_STORE_LIST", "Fresh"],
    _if(["BC_CONST", "1"], _store()),
    _if(_store(), ["BC_CONST", "1"]),
    ["BC_STORE_LIST", "Fresh"],
    ["BC_PRINT"],
    ["BC_BINOP", "+"],
    _repeat(_read()),
    ["BC_WHILE_BEGIN", "BC_WHILE_END"],
    ["BC_CONST", "1", "BC_IF_BEGIN"],
    ["BC_ELSE_BEGIN"],
])
def test_incomplete_stack_and_unreachable_bad_body_reject(body):
    for count in ("0", "2"):
        assert _run_kuro(_repeat(body, count)) is None


@pytest.mark.parametrize("tokens", [
    [], _store(), _repeat([]) + _read(), _repeat([]) + _repeat([]),
    _repeat([], "01"), _repeat([], "-1"), _repeat([], "1.0"),
    _repeat([], "N"), _repeat([], ""),
])
def test_entire_stream_and_exact_count_grammar_are_required(tokens):
    assert _run_kuro(tokens) is None


def test_kind_join_is_exact_for_every_mask_pair():
    source = _source([])
    calls = []
    for left in range(8):
        for right in range(8):
            calls += [f"Call FlowJoin {left}, {right};", "Print @_."]
    source = source.replace("Call FlowAnalyze;", "\n".join(calls))
    result = run_source(source)
    assert result.ok, result.runtime_error
    assert list(map(int, result.stdout.splitlines())) == [a | b for a in range(8) for b in range(8)]


def test_specialized_depth_actions_do_not_drift():
    # Kuro Action scratch names are shared, so recursion is explicitly specialized
    # by depth. Verify all 16 callable levels use the same parser/transfer logic.
    import re
    source = FLOW_SOURCE.read_text(encoding="utf-8")
    bodies = []
    for depth in range(16):
        start = source.index(f"Action FlowSequence{depth} ")
        end = source.index("\nDone.", start)
        body = source[start:end]
        body = body.replace(f"FlowSequence{depth + 1}", "NEXT")
        body = body.replace(f"FlowSequence{depth}", "CURRENT")
        bodies.append(re.sub(rf"FlowSeq{depth}_", "LOCAL_", body))
    assert len(set(bodies)) == 1


def test_finite_trip_enumeration_independently_checks_branch_evidence():
    from itertools import product
    arms = ((), ("read",), ("D",), ("read", "D"), ("I", "read"))
    for yes, no in product(arms, repeat=2):
        def encode(events):
            return [token for event in events for token in
                    (_read() if event == "read" else _store("1" if event == "I" else "1.5"))]
        body = _if(encode(yes), encode(no)) + _store() + _read()
        tokens = _repeat(body, "3")
        actual, decision = _run_kuro(tokens)
        pcs = sorted(pc for pc, name, origin in actual if origin == "E")
        expected = {(pc, "Fresh", origin): 0 for pc in pcs for origin in ("E", "B")}
        for choices in product((0, 1), repeat=3):
            kind = 1
            for trip, choice in enumerate(choices):
                origin = "E" if trip == 0 else "B"
                cursor = 0 if choice == 0 else yes.count("read")
                for event in (yes, no)[choice]:
                    if event == "read":
                        expected[(pcs[cursor], "Fresh", origin)] |= kind
                        cursor += 1
                    else:
                        kind = 2 if event == "I" else 4
                kind = 4
                expected[(pcs[-1], "Fresh", origin)] |= kind
        assert actual == expected, (yes, no, actual, expected)
        assert decision == all(mask == 4 for mask in expected.values())


def test_every_proper_prefix_of_nested_program_rejects_without_runtime_error():
    tokens = _store() + _repeat(_if(_if(_read(), _store()), _store()) + _read())
    for length in range(len(tokens)):
        assert _run_kuro(tokens[:length]) is None, length


SLOTS = ("Fresh", "Other", "Third", "Fourth")


@pytest.mark.parametrize("count", ["0", "1", "2", "9"])
@pytest.mark.parametrize("name", SLOTS)
def test_all_slots_retain_independent_entry_and_backedge_kinds(name, count):
    prefix = sum((_store("1.5", slot) for slot in SLOTS if slot != name), [])
    tokens = prefix + _repeat(_read(name) + _store("2.5", name) + _read(name), count)
    actual = _run_kuro(tokens)
    assert actual == _expected(tokens)
    assert actual[1] == (count == "0")


def test_interleaved_cross_slot_stores_never_repair_other_slot_reads():
    tokens = (_store("1.5", "Fresh") + _store("1", "Other") +
              _store("2.5", "Fresh") + _repeat(
                  _read("Other") + _store("3.5", "Third") + _read("Fourth") +
                  _if(_store("4.5", "Other"), _store("5.5", "Fourth")) +
                  sum((_read(name) for name in SLOTS), [])))
    records, decision = _run_kuro(tokens)
    assert (records, decision) == _expected(tokens)
    assert not decision
    entry = {(name, mask) for (pc, name, origin), mask in records.items() if origin == "E"}
    assert ("Fresh", 4) in entry and ("Other", 2) in entry
    assert ("Third", 4) in entry and ("Fourth", 1) in entry


def test_nested_branch_snapshots_restore_and_join_every_slot():
    tokens = sum((_store("1.5", name) for name in SLOTS), []) + _repeat(
        _if(_if(_store("1", "Fresh") + _store("2", "Third"),
                _store("3", "Other") + _store("4", "Fourth")),
            _if(_store("5", "Fourth"), _store("6", "Fresh"))) +
        sum((_read(name) for name in SLOTS), []))
    result = _run_kuro(tokens)
    assert result == _expected(tokens)
    assert set(result[0].values()) == {6}


@pytest.mark.parametrize("bad_name", ["1Fifth", "fresh!", "", "BC_LOADVAR", "Fresh Other", "Fresh\nOther"])
def test_invalid_slot_names_reject_in_prefix_body_and_unreachable_arms(bad_name):
    fixtures = [
        _store(name=bad_name) + _repeat([]),
        _repeat(_store(name=bad_name)),
        _repeat(_if([], _read(bad_name)), "0"),
    ]
    for tokens in fixtures:
        assert _run_kuro(tokens) is None


def test_copy_and_cross_slot_expression_extensions_are_explicitly_rejected():
    for count in ("0", "2"):
        for body in (
            ["BC_LOADVAR", "Fresh", "BC_STORE_LIST", "Other"],
            ["BC_LOADVAR", "Fresh", "BC_LOADVAR", "Other", "BC_BINOP", "+", "BC_PRINT"],
            ["BC_CONST", "1.5", "BC_STORE_LIST"],
            ["BC_LOADVAR", "Fourth"],
        ):
            assert _run_kuro(_repeat(body, count)) is None


def test_multislot_prefix_and_nested_stream_all_proper_prefixes_reject():
    tokens = sum((_store(name=name) for name in SLOTS), []) + _repeat(
        _if(_read("Fourth"), _if(_store("1", "Other"), _read("Third"))) + _read())
    for length in range(len(tokens)):
        assert _run_kuro(tokens[:length]) is None, length


def test_multislot_token_limit_includes_prefix_and_never_truncates_reads():
    # 31 stores (124 tokens) plus the empty Repeat (4 tokens) hits 128 exactly.
    prefix = sum((_store(name=SLOTS[i % 4]) for i in range(31)), [])
    exact = prefix + _repeat([])
    assert len(exact) == 128
    assert _run_kuro(exact) == _expected(exact)
    assert _run_kuro(prefix + _repeat(_read("Fourth"))) is None
    assert _run_kuro(prefix + _store(name="Fourth") + _repeat([])) is None


def test_slot_renaming_preserves_evidence_without_aliasing():
    tokens = _store(name="Fresh") + _repeat(
        _if(_read("Other") + _store(name="Third"), _store("1", "Fourth")) +
        sum((_read(name) for name in SLOTS), []))
    original, decision = _run_kuro(tokens)
    rename = dict(zip(SLOTS, SLOTS[1:] + SLOTS[:1]))
    renamed = [rename.get(token, token) for token in tokens]
    actual = _run_kuro(renamed)
    assert actual == ({(pc, rename[name], origin): mask
                       for (pc, name, origin), mask in original.items()}, decision)
    assert actual == _expected(renamed)


@pytest.mark.parametrize("count", [0, 1, 2, 3, 9])
def test_independent_finite_paths_track_all_slots_across_literal_trips(count):
    from itertools import product
    # Enumerate every independent branch choice for every trip, not an abstract
    # fixed-point solve. Each arm overwrites a different pair of slots.
    yes = _read("Other") + _store("1.5", "Fresh") + _store("1", "Third")
    no = _read("Fresh") + _store("2.5", "Other") + _store("2", "Fourth")
    tokens = _repeat(_if(yes, no) + sum((_read(name) for name in SLOTS), []), str(count))
    actual, decision = _run_kuro(tokens)
    loads = [(pc, tokens[pc + 1]) for pc, token in enumerate(tokens) if token == "BC_LOADVAR"]
    expected = {(pc, name, origin): 0 for pc, name in loads for origin in ("E", "B")}
    for choices in product((0, 1), repeat=count):
        state = dict.fromkeys(SLOTS, 1)
        for trip, choice in enumerate(choices):
            origin = "E" if trip == 0 else "B"
            pc, name = loads[choice]
            expected[(pc, name, origin)] |= state[name]
            state.update({"Fresh": 4, "Third": 2} if choice == 0 else {"Other": 4, "Fourth": 2})
            for pc, name in loads[2:]:
                expected[(pc, name, origin)] |= state[name]
    assert actual == expected
    assert decision == all(mask in (0, 4) for mask in expected.values())
    assert (actual, decision) == _expected(tokens)


@pytest.mark.skipif(platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
                    reason="native execution requires Linux x86-64")
@pytest.mark.parametrize("tokens", [
    sum((_store(name=name) for name in SLOTS), []) + _repeat(sum((_read(name) for name in SLOTS), [])),
    _repeat(_if(_read("Other"), _store(name="Third")) + _store(name="Other") + _read("Other")),
    _repeat(_read("Fourth"), "0"),
    sum((_store(name=name) for name in SLOTS), []) + _repeat(sum((_read(name) for name in SLOTS), []), "1"),
    _store("1", "Fresh") + _store("1.5", "Fresh") + _store("1", "Other") + _repeat(_read("Fresh") + _read("Other")),
    _repeat(_read("BC_Fifth"), "0"),
    sum((_store(name=SLOTS[i % 4]) for i in range(31)), []) + _repeat(_read("Fourth")),
])
def test_multislot_analyzer_hosted_native_matches_full_protocol(tmp_path, tokens):
    from compiler.native import build_native
    compiled = compile_source(_source(tokens), filename="<native multislot flow>")
    assert compiled.ok, compiled.diags.diagnostics
    image = tmp_path / "multislot-flow"
    build_native(compiled.ir, image, target="x86_64-linux")
    result = subprocess.run([str(image)], text=True, capture_output=True, timeout=15)
    hosted = run_source(_source(tokens))
    assert hosted.ok, hosted.runtime_error
    assert result.returncode == 0 and result.stderr == ""
    assert result.stdout == hosted.stdout


def test_all_slot_snapshots_work_at_exact_depth_bound():
    body = sum((_store("1", name) for name in SLOTS), [])
    for _ in range(16):
        body = _if(body)
    tokens = sum((_store(name=name) for name in SLOTS), []) + _repeat(
        body + sum((_read(name) for name in SLOTS), []))
    assert len(tokens) <= 128
    assert _run_kuro(tokens) == _expected(tokens)
    assert set(_run_kuro(tokens)[0].values()) == {6}


@pytest.mark.parametrize("literal", ["9" * 256, "1." + "0" * 256, "-9999999999999999999999", "1e999999"])
def test_oversized_numeric_operands_do_not_wrap_into_supported_values(literal):
    assert _run_kuro(_repeat([], literal)) is None
    assert _run_kuro(_store(literal, "Fourth") + _repeat([])) is None
    assert _run_kuro(_repeat(_store(literal, "Other"), "0")) is None


@pytest.mark.parametrize("count", ["0", "1", "9"])
def test_maximum_load_density_retains_all_82_origin_keys(count):
    tokens = _repeat(sum((_read(SLOTS[i % 4]) for i in range(41)), []), count)
    assert len(tokens) == 127
    actual = _run_kuro(tokens)
    assert actual == _expected(tokens)
    assert len(actual[0]) == 82
    assert _run_kuro(_repeat(sum((_read(SLOTS[i % 4]) for i in range(42)), []), count)) is None


@pytest.mark.parametrize("count", ["0", "1", "2", "9"])
def test_ordered_prefix_overwrites_have_direct_independent_expected_facts(count):
    prefix = (_store("1", "Fresh") + _store("1.5", "Fresh") +
              _store("1", "Other") + _store("2.5", "Fourth"))
    tokens = prefix + _repeat(sum((_read(name) for name in SLOTS), []), count)
    expected = {}
    for i, (name, mask) in enumerate(zip(SLOTS, (4, 2, 1, 4))):
        pc = len(prefix) + 3 + 3 * i
        expected[(pc, name, "E")] = 0 if count == "0" else mask
        expected[(pc, name, "B")] = mask if count in ("2", "9") else 0
    assert _run_kuro(tokens) == (expected, count == "0")
