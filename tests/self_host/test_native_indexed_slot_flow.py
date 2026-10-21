"""Indexed 16-slot state and snapshot regressions for the bounded analyzer."""
import platform
import subprocess
from itertools import product

import pytest

from compiler.pipeline import compile_source, run_source
from test_native_dynamic_slot_flow import _if, _read, _repeat, _run_kuro, _source, _store


SLOTS = tuple(f"slot{i:02d}" for i in range(16))


def _records_for_reads(tokens, masks):
    records = {}
    for pc, token in enumerate(tokens):
        if token == "BC_LOADVAR":
            name = tokens[pc + 1]
            for origin in ("E", "B"):
                records[(pc, name, origin)] = masks[name]
    return records


def _nested_late_discovery_tokens():
    body = (
        _if(_store(name=SLOTS[0]), _read(SLOTS[0])) +
        _if(_store("1.5", SLOTS[1])) + _read(SLOTS[1]) +
        _if(_store(name=SLOTS[2]), _store("1.5", SLOTS[3])) +
        _read(SLOTS[2]) + _read(SLOTS[3]) +
        _if(_if(_store("1", SLOTS[4]), _store("1.5", SLOTS[5])),
            _if(_store("1.5", SLOTS[6]), _read(SLOTS[7]))) +
        sum((_read(name) for name in SLOTS[4:8]), [])
    )
    return _repeat(body)


NESTED_HAND_MASKS = {
    SLOTS[0]: (1, 5),
    SLOTS[1]: (5, 5),
    SLOTS[2]: (5, 5),
    SLOTS[3]: (5, 5),
    SLOTS[4]: (3, 3),
    SLOTS[5]: (5, 5),
    SLOTS[6]: (5, 5),
    SLOTS[7]: (1, 1),
}


def _nested_hand_records(tokens):
    records = {}
    for pc, token in enumerate(tokens):
        if token == "BC_LOADVAR":
            name = tokens[pc + 1]
            entry, backedge = NESTED_HAND_MASKS[name]
            records[(pc, name, "E")] = entry
            records[(pc, name, "B")] = backedge
    return records


def test_all_sixteen_indexed_slots_are_independent_and_ordered():
    prefix_masks = {name: (2 if i % 2 == 0 else 4) for i, name in enumerate(SLOTS)}
    prefix = sum((_store("1" if i % 2 == 0 else "1.5", name)
                  for i, name in enumerate(SLOTS)), [])
    tokens = prefix + _repeat(sum((_read(name) for name in SLOTS), []), "2")
    records, decision = _run_kuro(tokens)
    assert records == _records_for_reads(tokens, prefix_masks)
    assert not decision
    assert {name for _, name, _ in records} == set(SLOTS)
    assert all(records[(pc, name, origin)] == prefix_masks[name]
               for (pc, name, origin) in records)


def test_indexed_slot_repeated_names_reuse_capacity_without_aliasing():
    prefix = sum((_store("1" if i % 2 == 0 else "1.5", name)
                  for i, name in enumerate(SLOTS)), [])
    tokens = prefix + _store("2.5", SLOTS[0]) + _repeat(
        sum((_read(name) for name in SLOTS), []))
    masks = {name: (4 if i == 0 or i % 2 == 1 else 2) for i, name in enumerate(SLOTS)}
    records, decision = _run_kuro(tokens)
    assert records == _records_for_reads(tokens, masks)
    assert not decision


def test_pointwise_joins_preserve_late_discovery_across_arms_and_missing_else():
    # Slots 0-3 exercise read-after-snapshot and missing-else joins. Slots 4-7
    # are written/read in nested opposite arms, so late identities must be
    # added to and restored through already-taken snapshots.
    tokens = _nested_late_discovery_tokens()
    records, decision = _run_kuro(tokens)
    assert records == _nested_hand_records(tokens)
    assert not decision


def test_exact_sixteen_capacity_and_seventeenth_discovery_rejects_everywhere():
    full_prefix = sum((_store(name=name) for name in SLOTS), [])
    assert _run_kuro(full_prefix + _repeat(sum((_read(name) for name in SLOTS), []))) is not None
    overflow = "slot16"
    fixtures = [
        full_prefix + _store(name=overflow) + _repeat([]),
        _repeat(sum((_store(name=name) for name in (*SLOTS, overflow)), [])),
    ]
    for tokens in fixtures:
        assert _run_kuro(tokens) is None
    # Discovery still visits zero-trip bodies and both arms. This spelling is
    # only one distinct name here, not an overflow without 16 prior names.
    assert _run_kuro(_repeat(_if([], _store(name=overflow)), "0")) == ({}, True)
    assert _run_kuro(_repeat(_read(overflow), "0")) == (
        {(3, overflow, "E"): 0, (3, overflow, "B"): 0}, True)


def test_indexed_state_snapshots_work_at_exact_if_depth_and_reject_depth_seventeen():
    body = _store("1.5", SLOTS[-1]) + _read(SLOTS[-1])
    for _ in range(16):
        body = _if(body, [])
    tokens = _repeat(body)
    records, decision = _run_kuro(tokens)
    read_pc = tokens.index("BC_LOADVAR")
    assert records == {(read_pc, SLOTS[-1], "E"): 4,
                       (read_pc, SLOTS[-1], "B"): 4}
    assert decision
    assert _run_kuro(_repeat(_if(body))) is None


def test_128_token_boundary_malformed_inputs_and_every_truncated_prefix_fail_closed():
    exact = sum((_store(name=SLOTS[0]) for _ in range(31)), []) + _repeat([])
    assert len(exact) == 128
    assert _run_kuro(exact) is not None
    assert _run_kuro(exact + ["BC_PRINT"]) is None

    nested = _store(name=SLOTS[0]) + _repeat(
        _if(_if(_read(SLOTS[0]), _store("1.5", SLOTS[1])), _store(name=SLOTS[2])))
    for length in range(len(nested)):
        assert _run_kuro(nested[:length]) is None, length

    malformed = [
        ["BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_LOADVAR", "BC_CONST", "BC_PRINT", "BC_REPEAT_END"],
        _repeat(["BC_LOADVAR", SLOTS[0], "BC_STORE_LIST", SLOTS[1]]),
        _repeat(["BC_LOADVAR", SLOTS[0], "BC_LOADVAR", SLOTS[1], "BC_BINOP", "+", "BC_PRINT"]),
        _repeat(_repeat(_read(SLOTS[0]))),
        _repeat(["BC_WHILE_BEGIN", "BC_WHILE_END"]),
        _repeat(_store("1.25", SLOTS[0]), "0"),
    ]
    for tokens in malformed:
        assert _run_kuro(tokens) is None


def test_literal_only_transfer_with_sixteen_names_rejects_copy_and_general_expression():
    for body in (
        ["BC_LOADVAR", SLOTS[0], "BC_STORE_LIST", SLOTS[1]],
        ["BC_LOADVAR", SLOTS[0], "BC_LOADVAR", SLOTS[1], "BC_BINOP", "+", "BC_PRINT"],
        ["BC_CONST", "1", "BC_LOADVAR", SLOTS[0], "BC_STORE_LIST", SLOTS[2]],
        _repeat(_read(SLOTS[0])),
    ):
        for count in ("0", "2"):
            assert _run_kuro(_repeat(body, count)) is None


@pytest.mark.parametrize("count", [0, 1, 2, 3, 9])
def test_sixteen_slot_finite_paths_are_independently_enumerated(count):
    # Enumerate all branch choices per concrete trip; this is intentionally
    # independent of the CFG oracle and bounded to 2**9 paths at most.
    yes = _read(SLOTS[0]) + _store("1.5", SLOTS[1]) + _store("1", SLOTS[2])
    no = _read(SLOTS[3]) + _store("1", SLOTS[4]) + _store("1.5", SLOTS[5])
    prefix = sum((_store("1" if i % 2 == 0 else "1.5", name)
                  for i, name in enumerate(SLOTS[:10])), [])
    tail = sum((_read(name) for name in SLOTS), [])
    tokens = prefix + _repeat(_if(yes, no) + tail, str(count))
    assert len(tokens) <= 128
    loads = [(pc, tokens[pc + 1]) for pc, op in enumerate(tokens) if op == "BC_LOADVAR"]
    expected = {(pc, name, origin): 0 for pc, name in loads for origin in ("E", "B")}
    initial = {name: 1 for name in SLOTS}
    initial.update({name: (2 if i % 2 == 0 else 4)
                    for i, name in enumerate(SLOTS[:10])})
    for choices in product((0, 1), repeat=count):
        state = dict(initial)
        origin = "E"
        for choice in choices:
            branch_pc = tokens.index("BC_LOADVAR", tokens.index("BC_REPEAT_BEGIN") + 2)
            if choice:
                branch_pc = tokens.index("BC_LOADVAR", branch_pc + 1)
            branch_name = tokens[branch_pc + 1]
            expected[(branch_pc, branch_name, origin)] |= state[branch_name]
            if choice == 0:
                state[SLOTS[1]], state[SLOTS[2]] = 4, 2
            else:
                state[SLOTS[4]], state[SLOTS[5]] = 2, 4
            for pc, name in loads[2:]:
                expected[(pc, name, origin)] |= state[name]
            origin = "B"
    records, decision = _run_kuro(tokens)
    assert records == expected
    assert decision == all(mask in (0, 4) for mask in expected.values())


NATIVE_CASES = [
    sum((_store(name=name) for name in SLOTS), []) +
    _repeat(sum((_read(name) for name in SLOTS), [])),
    _nested_late_discovery_tokens(),
    _repeat(sum((_store(name=name) for name in (*SLOTS, "slot16")), []), "0"),
]

NATIVE_HAND_EXPECTED = [
    (_records_for_reads(NATIVE_CASES[0], {name: 4 for name in SLOTS}), True),
    (_nested_hand_records(NATIVE_CASES[1]), False),
    None,
]


@pytest.mark.skipif(platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
                    reason="native execution requires Linux x86-64")
@pytest.mark.parametrize("tokens, hand_expected", list(zip(NATIVE_CASES, NATIVE_HAND_EXPECTED)))
def test_indexed_analyzer_hosted_native_matches_full_stdout(tmp_path, tokens, hand_expected):
    from compiler.native import build_native
    assert _run_kuro(tokens) == hand_expected
    source = _source(tokens)
    compiled = compile_source(source, filename="<native indexed slot flow>")
    assert compiled.ok, compiled.diags.diagnostics
    image = tmp_path / "indexed-slot-flow"
    build_native(compiled.ir, image, target="x86_64-linux")
    native = subprocess.run([str(image)], text=True, capture_output=True, timeout=15)
    hosted = run_source(source)
    assert hosted.ok, hosted.runtime_error
    assert native.returncode == 0 and native.stderr == ""
    assert native.stdout == hosted.stdout
