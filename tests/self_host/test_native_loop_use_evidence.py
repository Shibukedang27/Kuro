"""Per-use boundary-origin evidence; this module grants no native permission."""
import json
from itertools import product

import pytest

from loop_flow_facts import analyze
from test_native_codegen import run_codegen
from test_native_loop_flow_facts import LOOP_FLOW_POSITIVE_CASES, LOOP_FLOW_REJECTION_CASES

TARGETS = ("x86_64-linux", "x86_64-macos", "aarch64-macos")


def _store(value="1.5", name="Fresh"):
    return ["BC_CONST", value, "BC_STORE_LIST", name]


def _read(name="Fresh"):
    return ["BC_LOADVAR", name, "BC_PRINT"]


def _if(yes, no=None):
    return ["BC_CONST", "1", "BC_IF_BEGIN", *yes,
            *(["BC_ELSE_BEGIN", *no] if no is not None else []), "BC_IF_END"]


def _repeat(body, count="2"):
    return ["BC_CONST", count, "BC_REPEAT_BEGIN", *body, "BC_REPEAT_END"]


def loop_use_rejection_cases():
    """Named raw fixtures used by hosted and freshly compiled native generators."""
    cases = {}
    for count in ("2", "9"):
        bodies = {
            "then-read": _if(_read(), []) + _store() + _read(),
            "else-read": _if([], _read()) + _store() + _read(),
            "no-else-read": _if(_read()) + _store() + _read(),
            "nested-then-read": _if(_if(_read(), []), []) + _store() + _read(),
            "nested-else-read": _if([], _if([], _read())) + _store() + _read(),
            "read-before-complete-arms": _if(_read() + _store(), _store("2.5")) + _read(),
            "sibling-read-before-complete-arms": _if(_read(), [])
                + _if(_store(), _store("2.5")) + _read(),
            "complete-arms-still-unpromoted": _if(_store(), _store("2.5")) + _read(),
        }
        for name, body in bodies.items():
            cases[f"use-{count}-{name}"] = _repeat(body, count) + _read()
    cases["use-integer-entry-branch-read"] = _store("1") + _repeat(
        _if(_read(), []) + _store() + _read()) + _read()
    cases["use-unknown-inner-repeat-read"] = _repeat([
        "BC_LOADVAR", "N", "BC_REPEAT_BEGIN", *_if(_read(), []), "BC_REPEAT_END",
        *_store(), *_read(),
    ]) + _read()
    cases["use-while-condition-read"] = [
        "BC_WHILE_BEGIN", *_read(), "BC_CONST", "1", "BC_WHILE_TEST",
        *_if([], _read()), *_store(), "BC_WHILE_END", *_read(),
    ]
    return cases


def loop_use_control_cases():
    """Previously accepted controls: tokens and actual selected-arm stdout."""
    return {
        "use-direct-store-before-branches": (
            _repeat(_store() + _if(_read(), _read()) + _read()) + _read(),
            "1.5\n" * 5,
        ),
        "use-established-before-loop": (
            _store() + _repeat(_if(_read(), _read())) + _read(), "1.5\n" * 3,
        ),
        "use-exact-once-complete-arms": (
            _repeat(_if(_store(), _store("2.5")) + _read(), "1") + _read(),
            "1.5\n" * 2,
        ),
    }


def _outer(result):
    return min(result["loops"], key=lambda loop: loop["begin"])


def _fresh_uses(loop):
    return [use for use in loop["uses"] if use["name"] == "Fresh"]


@pytest.mark.parametrize("arm", ["then-read", "else-read", "no-else-read",
                                     "nested-then-read", "nested-else-read"])
def test_branch_restoration_cannot_erase_an_earlier_read(arm):
    result = analyze(loop_use_rejection_cases()[f"use-2-{arm}"])
    uses = _fresh_uses(_outer(result))
    assert len(uses) == 2
    assert uses[0]["entry_kinds"] == {"?"}
    assert uses[0]["backedge_kinds"] == {"D"}
    assert uses[0]["kinds"] == {"?", "D"}
    assert uses[1]["entry_kinds"] == uses[1]["backedge_kinds"] == {"D"}
    assert result["loads"][-1]["kinds"] == {"D"}  # exit alone hides the bad use
    assert result["loads"][-1]["pc"] not in {use["pc"] for use in uses}


def test_integer_entry_and_read_before_complete_join_keep_distinct_evidence():
    cases = loop_use_rejection_cases()
    integer = _fresh_uses(_outer(analyze(cases["use-integer-entry-branch-read"])))
    assert integer[0]["entry_kinds"] == {"I"}
    assert integer[0]["backedge_kinds"] == {"D"}
    for name in ("read-before-complete-arms", "sibling-read-before-complete-arms"):
        result = analyze(cases[f"use-2-{name}"])
        uses = _fresh_uses(_outer(result))
        assert uses[0]["entry_kinds"] == {"?"}
        assert uses[0]["backedge_kinds"] == {"D"}
        assert uses[-1]["entry_kinds"] == uses[-1]["backedge_kinds"] == {"D"}


def test_nested_runtime_loop_and_while_condition_preserve_read_evidence():
    cases = loop_use_rejection_cases()
    nested = _outer(analyze(cases["use-unknown-inner-repeat-read"]))
    assert _fresh_uses(nested)[0]["entry_kinds"] == {"?"}
    assert _fresh_uses(nested)[0]["backedge_kinds"] == {"D"}
    condition = _fresh_uses(_outer(analyze(cases["use-while-condition-read"])))
    assert condition[0]["entry_kinds"] == {"?"}
    assert condition[0]["backedge_kinds"] == {"D"}
    assert condition[1]["entry_kinds"] == {"?"}
    assert condition[1]["backedge_kinds"] == {"D"}


def test_zero_exact_once_empty_and_missing_path_boundaries():
    zero = _outer(analyze(_repeat(_read() + _store(), "0") + _read()))
    assert len(zero["uses"]) == 1
    assert zero["uses"][0]["entry_kinds"] is None
    assert zero["uses"][0]["backedge_kinds"] is None
    assert zero["uses"][0]["kinds"] == frozenset()
    once = _outer(analyze(_repeat(_read() + _store() + _read(), "1")))
    uses = _fresh_uses(once)
    assert [use["entry_kinds"] for use in uses] == [{"?"}, {"D"}]
    assert all(use["backedge_kinds"] is None for use in uses)
    empty = _outer(analyze(_repeat([])))
    assert empty["uses"] == []
    missing = _outer(analyze(_repeat(_if(_store()) + _read())))
    use = _fresh_uses(missing)[0]
    assert use["entry_kinds"] == use["backedge_kinds"] == {"?", "D"}


def test_structural_backedge_beneath_zero_count_loop_has_no_fabricated_evidence():
    result = analyze(_repeat(_repeat(_read() + _store()), "0") + _read())
    outer, inner = sorted(result["loops"], key=lambda loop: loop["begin"])
    assert inner["backedge"] is not None  # present in CFG, but not reachable
    for loop in (outer, inner):
        assert loop["entry_facts"] is loop["backedge_facts"] is None
        assert len(loop["uses"]) == 1
        use = loop["uses"][0]
        assert use["entry_kinds"] is use["backedge_kinds"] is None
        assert use["kinds"] == frozenset()
        assert use["pc"] not in {load["pc"] for load in result["loads"]}


def test_nested_entry_is_not_misreported_as_first_ever_iteration():
    # The inner exact-once loop is entered on every outer trip. Its entry edge
    # already joins '?' on the first outer trip and D on later outer trips.
    code = _repeat(_repeat(_read(), "1") + _store())
    result = analyze(code)
    outer, inner = sorted(result["loops"], key=lambda loop: loop["begin"])
    assert _fresh_uses(outer)[0]["entry_kinds"] == {"?"}
    assert _fresh_uses(outer)[0]["backedge_kinds"] == {"D"}
    assert _fresh_uses(inner)[0]["entry_kinds"] == {"?", "D"}
    assert _fresh_uses(inner)[0]["backedge_kinds"] is None


def test_generated_branch_events_match_independent_bounded_trip_enumeration():
    # Independent finite event semantics, not the oracle parser or transfer.
    # Each trip nondeterministically chooses either arm. A direct trailing D
    # store ensures later trips start D, without repairing any earlier use.
    arms = ((), ("read",), ("D",), ("read", "D"), ("D", "read"))
    for initial, count, yes, no in product(("?", "I"), (2, 3), arms, arms):
        def tokens(events):
            return [token for event in events
                    for token in (_read() if event == "read" else _store())]

        code = ([] if initial == "?" else _store("1")) + _repeat(
            _if(tokens(yes), tokens(no)) + _store() + _read(), str(count)) + _read()
        result = analyze(code)
        uses = _fresh_uses(_outer(result))
        # Enumerate complete arm-choice histories for every concrete trip.
        expected = [{"entry": set(), "backedge": set()} for _ in uses]
        offsets = (0, yes.count("read"))
        for choices in product((0, 1), repeat=count):
            kind = initial
            for trip, choice in enumerate(choices):
                phase = "entry" if trip == 0 else "backedge"
                cursor = offsets[choice]
                for event in (yes, no)[choice]:
                    if event == "read":
                        expected[cursor][phase].add(kind)
                        cursor += 1
                    else:
                        kind = "D"
                kind = "D"  # trailing direct store
                expected[-1][phase].add(kind)
        assert len(uses) == yes.count("read") + no.count("read") + 1
        for use, concrete in zip(uses, expected):
            assert use["entry_kinds"] == concrete["entry"], (initial, count, yes, no, use)
            assert use["backedge_kinds"] == concrete["backedge"], (initial, count, yes, no, use)


def test_boundary_partition_can_be_more_precise_than_global_nonrelational_arithmetic():
    # First trip A=I,B=?; later trips A=?,B=I. Each real sum is unknown.
    # A merged header loses that phase correlation and invents the I+I pair.
    code = _store("1", "A") + _repeat([
        "BC_LOADVAR", "A", "BC_LOADVAR", "B", "BC_BINOP", "+", "BC_STORE_LIST", "C",
        *_read("C"), "BC_LOADVAR", "U", "BC_STORE_LIST", "A", *_store("1", "B"),
    ])
    expected = analyze(code)
    for order, successors in product(("fifo", "lifo"), ("forward", "reverse")):
        assert analyze(code, worklist=order, successors=successors) == expected
    use = next(use for use in _outer(expected)["uses"] if use["name"] == "C")
    global_use = next(load for load in expected["loads"] if load["pc"] == use["pc"])
    assert use["entry_kinds"] == use["backedge_kinds"] == use["kinds"] == {"?"}
    assert use["kinds"] < global_use["kinds"] == {"?", "I"}


def test_named_boundary_use_unions_reconstruct_global_facts_and_ignore_schedule():
    cases = {**LOOP_FLOW_REJECTION_CASES, **LOOP_FLOW_POSITIVE_CASES,
             **loop_use_rejection_cases(),
             **{name: tokens for name, (tokens, _) in loop_use_control_cases().items()}}
    for name, code in cases.items():
        expected = analyze(code)
        for order in ("fifo", "lifo"):
            for successors in ("forward", "reverse"):
                result = analyze(code, worklist=order, successors=successors)
                assert result == expected, (name, order, successors)
        loads = {use["pc"]: use for use in expected["loads"]}
        for loop in expected["loops"]:
            for use in loop["uses"]:
                joined = (use["entry_kinds"] or frozenset()) | (use["backedge_kinds"] or frozenset())
                assert joined == use["kinds"], (name, use)
                if joined:
                    assert joined == loads[use["pc"]]["kinds"], (name, use)
                else:
                    assert use["pc"] not in loads, (name, use)


@pytest.mark.parametrize("target", TARGETS)
def test_native_loop_use_witnesses_preserve_acceptance_boundary(target):
    for name, tokens in loop_use_rejection_cases().items():
        env = run_codegen(", ".join(json.dumps(token) for token in tokens), target=target)
        assert env["NativeFailed"] == 1 and env["NativeOut"] == "", name
    for name, (tokens, _) in loop_use_control_cases().items():
        env = run_codegen(", ".join(json.dumps(token) for token in tokens), target=target)
        assert env["NativeFailed"] == 0 and env["NativeOut"], name
