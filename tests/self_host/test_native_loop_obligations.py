"""Bounded Kuro-owned test ledger for per-use Decimal loop obligations.

The caller supplies complete boundary-origin facts from loop_flow_facts; this
prototype is deliberately neither a solver nor production permission.
"""
import json
import platform
import subprocess
from pathlib import Path

import pytest

from compiler.pipeline import compile_source, run_source
from loop_flow_facts import analyze
from test_native_codegen import run_codegen
from test_native_loop_flow_facts import LOOP_FLOW_POSITIVE_CASES, LOOP_FLOW_REJECTION_CASES
from test_native_loop_use_evidence import (
    loop_use_control_cases, loop_use_rejection_cases,
)
from test_native_loop_use_evidence import TARGETS

ROOT = Path(__file__).resolve().parents[2]
LEDGER = Path(__file__).with_name("loop_use_obligations.kuro")


def _q(value):
    return json.dumps(str(value))


def ledger_source(obligations, *, capacity=None, event_overrides=None):
    """Generate a tiny Kuro harness; obligations use oracle-shaped facts.

    Each item is (identity=(loop_begin, load_pc, slot), entry_kinds, backedge_kinds).
    None is an explicitly unreachable boundary; a set containing '?' is reachable
    unknown. event_overrides maps obligation index to an event list for adversarial
    omissions, duplicates, ordering, malformed records, and identity corruption.
    """
    obligations = list(obligations)
    capacity = len(obligations) if capacity is None else capacity
    overrides = event_overrides or {}
    calls = [f"Call LedgerReset {capacity};"]
    for ix, (identity, entry, backedge) in enumerate(obligations):
        loop, pc, slot = identity
        need_e = "None" if entry is None else "R"
        need_b = "None" if backedge is None else "R"
        calls.append("Call LedgerBegin " + ", ".join(map(_q, (loop, pc, slot, need_e, need_b))) + ";")
        default = [(origin, kind) for origin, facts in (("E", entry), ("B", backedge))
                   if facts is not None for kind in sorted(facts)]
        for origin, kind, *wrong in overrides.get(ix, default):
            event_id = wrong[0] if wrong else identity
            calls.append("Call LedgerObserve " + ", ".join(map(_q, (*event_id, origin, kind))) + ";")
        calls.append("Call LedgerFinish;")
    template = LEDGER.read_text(encoding="utf-8")
    marker = 'Print "LEDGER_HARNESS_GOES_HERE".'
    assert template.count(marker) == 1
    return template.replace(marker, "\n".join(calls))


def run_ledger(obligations, **kwargs):
    source = ledger_source(obligations, **kwargs)
    result = run_source(source, filename="<loop obligation ledger>")
    assert result.ok, (result.compile.diags.diagnostics, result.runtime_error)
    return result.stdout, source


def oracle_obligations(tokens):
    facts = analyze(tokens)
    obligations = []
    for loop in facts["loops"]:
        for use in loop["uses"]:
            obligations.append(((loop["begin"], use["pc"], use["name"]),
                                use["entry_kinds"], use["backedge_kinds"]))
    return facts, obligations


def oracle_discharge(entry, backedge):
    return all(kinds is None or (bool(kinds) and kinds == {"D"})
               for kinds in (entry, backedge))


def test_kuro_ledger_matches_independent_oracle_over_named_corpus():
    cases = {**LOOP_FLOW_POSITIVE_CASES, **LOOP_FLOW_REJECTION_CASES,
             **loop_use_rejection_cases(),
             **{name: tokens for name, (tokens, _) in loop_use_control_cases().items()}}
    checked = 0
    for name, tokens in cases.items():
        _, obligations = oracle_obligations(tokens)
        expected = all(oracle_discharge(entry, back) for _, entry, back in obligations)
        output, _ = run_ledger(obligations)
        assert output.endswith(f"{int(expected)}\n"), (name, output, obligations)
        checked += len(obligations)
    assert checked >= 20


def test_ledger_blocks_overwrite_and_branch_snapshot_restore_counterexamples():
    # The final load sees D in both programs, but the first per-use obligation
    # retains entry '?' and cannot be erased by a later store/branch join.
    cases = loop_use_rejection_cases()
    for name in ("use-2-then-read", "use-2-else-read", "use-2-read-before-complete-arms",
                 "use-2-sibling-read-before-complete-arms"):
        _, obligations = oracle_obligations(cases[name])
        assert any(entry and "?" in entry for _, entry, _ in obligations)
        assert run_ledger(obligations)[0].endswith("0\n")


def test_caller_declares_missing_evidence_wrong_identity_and_unreachable_distinctly():
    identity = (7, 23, "S")
    required = [(identity, {"D"}, {"D"})]
    assert run_ledger(required, event_overrides={0: [("E", "D"), ("B", "D")]})[0].endswith("1\n")
    # A required origin without an observation is incomplete, not unreachable.
    assert run_ledger(required, event_overrides={0: [("E", "D")]})[0].endswith("0\n")
    # Observation identity mismatch is sticky even though both proper origins follow.
    events = [("E", "D", (7, 24, "S")), ("B", "D")]
    assert run_ledger(required, event_overrides={0: events})[0].endswith("0\n")
    # None is an explicit unreachable origin; '?' is reachable unknown evidence.
    assert run_ledger([(identity, {"D"}, None)], event_overrides={0: [("E", "D")]})[0].endswith("1\n")
    assert run_ledger([(identity, {"?"}, None)], event_overrides={0: [("E", "?")]})[0].endswith("0\n")
    assert run_ledger([(identity, None, None)])[0].endswith("1\n")
    assert run_ledger([(identity, None, None)], event_overrides={0: [("E", "D")]})[0].endswith("0\n")


def test_exact_once_zero_conflicting_kinds_and_malformed_events():
    ident = (2, 9, "Fresh")
    # Exact-once: entry required, no backedge; zero/unreachable: neither required.
    assert run_ledger([(ident, {"D"}, None)])[0].endswith("1\n")
    assert run_ledger([(ident, None, None)])[0].endswith("1\n")
    assert run_ledger([(ident, {"D", "I"}, None)])[0].endswith("0\n")
    assert run_ledger([(ident, {"D"}, None)], event_overrides={0: [("E", "bogus")]})[0].endswith("0\n")
    assert run_ledger([(ident, {"D"}, None)], event_overrides={0: [("X", "D")]})[0].endswith("0\n")


def test_duplicates_and_event_order_are_idempotent_and_permutation_invariant():
    ident = (1, 4, "Fresh")
    facts = [(ident, {"D"}, {"D"})]
    events = [("E", "D"), ("B", "D")]
    outputs = set()
    for order in (events, list(reversed(events)), events + events):
        outputs.add(run_ledger(facts, event_overrides={0: order})[0])
    assert outputs == {"1\n"}
    bad = [("E", "D"), ("E", "?"), ("B", "D")]
    for order in (bad, list(reversed(bad))):
        assert run_ledger(facts, event_overrides={0: order})[0] == "0\n"


def test_capacity_exact_boundary_overflow_and_failure_is_sticky():
    records = [((1, pc, "S"), {"D"}, None) for pc in range(3)]
    assert run_ledger(records, capacity=3)[0].endswith("1\n")
    assert run_ledger(records, capacity=2)[0].endswith("0\n")
    # A later valid row cannot repair capacity overflow or earlier bad evidence.
    assert run_ledger(records, capacity=1)[0].endswith("0\n")
    invalid_then_valid = {0: [("E", "?")], 1: [("E", "D")], 2: [("E", "D")]}
    assert run_ledger(records, capacity=3, event_overrides=invalid_then_valid)[0].endswith("0\n")


@pytest.mark.parametrize("target", TARGETS)
def test_safe_complete_arm_multitrip_oracle_discharge_is_not_production_permission(target):
    tokens = loop_use_rejection_cases()["use-2-complete-arms-still-unpromoted"]
    _, obligations = oracle_obligations(tokens)
    assert obligations and all(oracle_discharge(e, b) for _, e, b in obligations)
    assert run_ledger(obligations)[0].endswith("1\n")
    # Hosted bootstrap/native codegen remains fail-closed: this ledger is a test
    # prototype, not wired into acceptance permission.
    raw = ", ".join(json.dumps(token) for token in tokens)
    env = run_codegen(raw, target=target)
    assert env["NativeFailed"] == 1 and env["NativeOut"] == ""


@pytest.mark.skipif(platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
                    reason="native execution probe requires Linux x86-64")
@pytest.mark.parametrize("events, expected", [
    ([("E", "D"), ("B", "D")], "1\n"),
    ([("E", "?"), ("E", "D"), ("B", "D")], "0\n"),
    ([("E", "I"), ("B", "D")], "0\n"),
    ([("E", "D")], "0\n"),
])
def test_kuro_ledger_executes_as_hosted_bootstrap_native_image(tmp_path, events, expected):
    # Call the Python bootstrap compiler directly, then execute its native image;
    # this does not claim the Kuro-owned native generator can compile this ledger.
    obligations = [((5, 11, "slot"), {"D"}, {"D"})]
    source = ledger_source(obligations, event_overrides={0: events})
    compiled = compile_source(source, filename="<native loop ledger>")
    assert compiled.ok, compiled.diags.diagnostics
    output = tmp_path / "loop-obligations-native"
    from compiler.native import build_native
    build_native(compiled.ir, output, target="x86_64-linux")
    result = subprocess.run([str(output)], check=True, capture_output=True, text=True, timeout=5)
    assert result.stdout == expected
    assert result.stderr == ""


def run_raw_stream(calls):
    """Bypass the well-formed Python adapter to attack the Kuro protocol itself."""
    source = LEDGER.read_text(encoding="utf-8").replace(
        'Print "LEDGER_HARNESS_GOES_HERE".', calls)
    result = run_source(source)
    assert result.ok, (result.compile.diags.diagnostics, result.runtime_error)
    return result.stdout


@pytest.mark.parametrize("calls", [
    'Call LedgerReset 1; Call LedgerFinish;',
    'Call LedgerReset 1; Call LedgerObserve "1", "2", "S", "E", "D";',
    'Call LedgerReset 1; Call LedgerBegin "1", "2", "S", "R", "None";',
    'Call LedgerReset 2; Call LedgerBegin "1", "2", "S", "R", "None"; '
    'Call LedgerBegin "1", "3", "S", "None", "None"; Call LedgerFinish;',
    'Call LedgerReset 1; Call LedgerBegin "1", "2", "S", "bogus", "None"; Call LedgerFinish;',
    'Call LedgerReset 1; Call LedgerBegin "1", "2", "S", "None", "bogus"; Call LedgerFinish;',
    'Call LedgerReset 1; Call LedgerSeal;',
    'Call LedgerReset 1; Call LedgerSeal; '
    'Call LedgerBegin "1", "2", "S", "None", "None"; Call LedgerFinish;',
    'Call LedgerReset -1;',
    'Call LedgerReset 65;',
])
def test_malformed_stream_protocol_fails_closed(calls):
    assert run_raw_stream(calls) == "0\n"


@pytest.mark.parametrize("identity", [(8, 23, "S"), (7, 24, "S"), (7, 23, "Other")])
def test_each_identity_component_is_checked(identity):
    obligations = [((7, 23, "S"), {"D"}, None)]
    assert run_ledger(obligations, event_overrides={0: [("E", "D", identity)]})[0] == "0\n"


def test_hard_capacity_boundary_and_empty_stream():
    rows = [((1, pc, "S"), {"D"}, None) for pc in range(65)]
    assert run_ledger(rows[:64], capacity=64)[0] == "1\n"
    assert run_ledger(rows, capacity=64)[0] == "0\n"
    assert run_ledger([], capacity=0)[0] == "1\n"
    assert run_ledger(rows[:1], capacity=0)[0] == "0\n"
