"""Dynamic identities in the test-only bounded Kuro-owned flow analyzer."""
import platform
import subprocess
from itertools import permutations, product

import pytest

from compiler.pipeline import compile_source, run_source
from test_native_loop_use_flow import _store, _read, _if, _repeat, _source, _run_kuro, _expected

NAMES = ("alpha", "Alpha", "_scratch2", "Z" + "9" * 31)
CAPACITY_NAMES = tuple(f"slot{i:02d}" for i in range(16))


@pytest.mark.parametrize("name", ["Fifth", "fresh", "_", "a0", "bc_loadvar", "BC", "B", *NAMES])
def test_dynamic_identifier_grammar_and_exact_identity(name):
    tokens = _store(name=name) + _repeat(_read(name))
    assert _run_kuro(tokens) == _expected(tokens)
    assert _run_kuro(tokens)[1]


@pytest.mark.parametrize("name", ["", "0a", "a-b", "a.b", "a b", "a\nb", "a\tb", "a\x00b", "é", "aé", "中", "BC_", "BC_unknown", "BC_LOADVAR", "a" * 33, "a" * 256])
def test_invalid_names_reject_before_any_evidence_even_unreachable(name):
    for tokens in (_store(name=name) + _repeat([]), _repeat(_store(name=name)),
                   _repeat(_if([], _read(name)), "0")):
        assert _run_kuro(tokens) is None


@pytest.mark.parametrize("count", ["0", "1", "2", "9"])
def test_seventeenth_distinct_name_rejects_in_all_discovery_positions(count):
    prefix = sum((_store(name=name) for name in CAPACITY_NAMES), [])
    overflow = "slot16"
    for tokens in (prefix + _store(name=overflow) + _repeat([], count),
                   prefix + _repeat(_store(name=overflow), count),
                   prefix + _repeat(_if([], _read(overflow)), count),
                   _repeat(sum((_read(name) for name in (*CAPACITY_NAMES, overflow)), []), count)):
        assert _run_kuro(tokens) is None


def test_repeated_names_reuse_capacity_without_aliasing_prefix_or_case():
    tokens = sum((_store("1" if i % 2 else "1.5", name) for i, name in enumerate(NAMES)), [])
    tokens += _store("2.5", "alpha") + _repeat(sum((_read(name) for name in NAMES), []))
    actual, decision = _run_kuro(tokens)
    assert (actual, decision) == _expected(tokens)
    assert not decision
    assert {(name, mask) for (pc, name, origin), mask in actual.items()} == set(zip(NAMES, (4, 2, 4, 2)))


@pytest.mark.parametrize("count", ["0", "1", "2", "9"])
def test_names_first_discovered_in_opposite_nested_arms_restore_unknown(count):
    # Names are first registered AFTER entry snapshots, including in the Else.
    tokens = _repeat(_if(_if(_store(name="alpha"), _store("1", "Alpha")),
                         _if(_store(name="_scratch2"), _store("1", NAMES[3]))) +
                     sum((_read(name) for name in NAMES), []), count)
    actual, decision = _run_kuro(tokens)
    assert (actual, decision) == _expected(tokens)
    masks = (5, 3, 5, 3)
    expected = {}
    for pc, token in enumerate(tokens):
        if token == "BC_LOADVAR":
            name = tokens[pc + 1]
            for origin in ("E", "B"):
                expected[(pc, name, origin)] = (0 if count == "0" or (count == "1" and origin == "B") else masks[NAMES.index(name)])
    assert actual == expected
    assert decision == (count == "0")


def test_late_discovery_else_read_is_not_repaired_by_then_store():
    tokens = _repeat(_if(_store(name="late"), _read("late")))
    pc = tokens.index("BC_LOADVAR")
    assert _run_kuro(tokens) == ({(pc, "late", "E"): 1, (pc, "late", "B"): 5}, False)
    tokens = _repeat(_if(_store(name="late")) + _read("late"))
    pc = tokens.index("BC_LOADVAR")
    assert _run_kuro(tokens) == ({(pc, "late", "E"): 5, (pc, "late", "B"): 5}, False)


@pytest.mark.parametrize("body", [_if(_read("late"), []), _if([], _read("late"))])
def test_read_only_late_discovery_keeps_unknown_snapshots(body):
    tokens = _repeat(body)
    pc = tokens.index("BC_LOADVAR")
    assert _run_kuro(tokens) == ({(pc, "late", "E"): 1, (pc, "late", "B"): 1}, False)


def test_discovery_order_permutations_preserve_complete_slot_snapshots():
    for names in permutations(NAMES):
        tokens = sum((_store(name=name) for name in names), []) + _repeat(
            _if(_if(_store("1", NAMES[0]), _store("2", NAMES[1])),
                _if(_store("3", NAMES[2]), _store("4", NAMES[3]))) +
            sum((_read(name) for name in NAMES), []))
        actual = _run_kuro(tokens)
        assert actual == _expected(tokens)
        assert set(actual[0].values()) == {6}


@pytest.mark.parametrize("count", [0, 1, 2, 3, 9])
def test_dynamic_names_independent_finite_paths(count):
    yes = _read(NAMES[1]) + _store(name=NAMES[0]) + _store("1", NAMES[2])
    no = _read(NAMES[0]) + _store(name=NAMES[1]) + _store("1", NAMES[3])
    tokens = _repeat(_if(yes, no) + sum((_read(name) for name in NAMES), []), str(count))
    loads = [(pc, tokens[pc + 1]) for pc, op in enumerate(tokens) if op == "BC_LOADVAR"]
    expected = {(pc, name, origin): 0 for pc, name in loads for origin in ("E", "B")}
    for choices in product((0, 1), repeat=count):
        state = dict.fromkeys(NAMES, 1)
        for trip, choice in enumerate(choices):
            origin = "E" if trip == 0 else "B"
            pc, name = loads[choice]
            expected[(pc, name, origin)] |= state[name]
            state.update({NAMES[0]: 4, NAMES[2]: 2} if choice == 0 else {NAMES[1]: 4, NAMES[3]: 2})
            for pc, name in loads[2:]:
                expected[(pc, name, origin)] |= state[name]
    actual = _run_kuro(tokens)
    assert actual == (expected, all(mask in (0, 4) for mask in expected.values()))
    assert actual == _expected(tokens)


def test_dynamic_discovery_all_proper_prefixes_fail_closed():
    tokens = _store(name=NAMES[0]) + _repeat(_if(_read(NAMES[1]), _if(_store(name=NAMES[2]), _read(NAMES[3]))) + _read(NAMES[0]))
    for length in range(len(tokens)):
        assert _run_kuro(tokens[:length]) is None, length


def test_dynamic_names_keep_depth_token_and_evidence_bounds():
    body = sum((_store("1", name) for name in NAMES), [])
    for _ in range(16):
        body = _if(body)
    tokens = sum((_store(name=name) for name in NAMES), []) + _repeat(body + sum((_read(name) for name in NAMES), []))
    assert _run_kuro(tokens) == _expected(tokens)
    assert set(_run_kuro(tokens)[0].values()) == {6}
    assert _run_kuro(_repeat(_if(body))) is None
    exact = sum((_store(name=NAMES[i % 4]) for i in range(31)), []) + _repeat([])
    assert len(exact) == 128
    assert _run_kuro(exact) == _expected(exact)
    assert _run_kuro(exact + ["BC_PRINT"]) is None
    dense = _repeat(sum((_read(NAMES[i % 4]) for i in range(41)), []))
    assert len(_run_kuro(dense)[0]) == 82
    assert _run_kuro(dense) == _expected(dense)


@pytest.mark.parametrize("count", ["0", "2"])
def test_dynamic_identities_do_not_enable_value_transfer(count):
    for body in (["BC_LOADVAR", NAMES[0], "BC_STORE_LIST", NAMES[1]],
                 ["BC_LOADVAR", NAMES[0], "BC_LOADVAR", NAMES[1], "BC_BINOP", "+", "BC_PRINT"]):
        assert _run_kuro(_repeat(body, count)) is None


NATIVE_CASES = [
    sum((_store(name=name) for name in NAMES), []) + _repeat(sum((_read(name) for name in NAMES), [])),
    _repeat(_if(_store(name="late"), _read("late"))),
    _repeat(sum((_read(name) for name in NAMES), []), "0"),
    _repeat(sum((_read(name) for name in NAMES), []), "1"),
    _repeat(sum((_read(name) for name in (*CAPACITY_NAMES, "slot16")), []), "0"),
    _repeat(_read("BC_LOADVAR"), "0"),
    _repeat(_read("a" * 33)),
    _repeat(_read("é")),
]


@pytest.mark.skipif(platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"}, reason="native execution requires Linux x86-64")
@pytest.mark.parametrize("tokens", NATIVE_CASES)
def test_dynamic_analyzer_hosted_native_matches_full_protocol(tmp_path, tokens):
    from compiler.native import build_native
    source = _source(tokens)
    compiled = compile_source(source, filename="<native dynamic flow>")
    assert compiled.ok, compiled.diags.diagnostics
    image = tmp_path / "dynamic-flow"
    build_native(compiled.ir, image, target="x86_64-linux")
    result = subprocess.run([str(image)], text=True, capture_output=True, timeout=15)
    hosted = run_source(source)
    assert hosted.ok, hosted.runtime_error
    assert result.returncode == 0 and result.stderr == ""
    assert result.stdout == hosted.stdout


def test_dynamic_zero_trip_scanner_has_exact_unreachable_records():
    tokens = _repeat(sum((_read(name) for name in NAMES), []), "0")
    expected = {(3 + 3 * i, name, origin): 0 for i, name in enumerate(NAMES) for origin in ("E", "B")}
    assert _run_kuro(tokens) == (expected, True)


@pytest.mark.skipif(platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"}, reason="native execution requires Linux x86-64")
def test_native_nested_late_discovery_has_hand_stated_masks(tmp_path):
    from compiler.native import build_native
    tokens = _repeat(_if(_if(_store(name=NAMES[0]), _read(NAMES[1])),
                         _if(_store("1", NAMES[2]), _store(name=NAMES[3]))) +
                     sum((_read(name) for name in NAMES), []))
    expected = {}
    loads = [(pc, tokens[pc + 1]) for pc, op in enumerate(tokens) if op == "BC_LOADVAR"]
    for i, (pc, name) in enumerate(loads):
        mask = 1 if i == 0 else (5, 1, 3, 5)[i - 1]
        for origin in ("E", "B"):
            expected[(pc, name, origin)] = mask
    assert _run_kuro(tokens) == (expected, False)
    source = _source(tokens)
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.diagnostics
    image = tmp_path / "nested-dynamic"
    build_native(compiled.ir, image, target="x86_64-linux")
    native = subprocess.run([str(image)], text=True, capture_output=True, timeout=15)
    hosted = run_source(source)
    assert hosted.ok
    assert native.returncode == 0 and native.stderr == ""
    assert native.stdout == hosted.stdout


def test_symbol_table_is_lookup_only_after_dry_validation():
    source = _source([]).replace("Call FlowAnalyze;", '''Call FlowResolveName "known";
Print @_.
FlowEmit = 1;
Call FlowResolveName "known";
Print @_.
Call FlowResolveName "new";
Print @_.
Print FlowBad.
Print FlowNameCount.''')
    result = run_source(source)
    assert result.ok, result.runtime_error
    assert result.stdout == "0\n0\n-1\n1\n1\n"
