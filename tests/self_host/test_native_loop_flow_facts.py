"""Fixed-point loop-flow witnesses plus unchanged native acceptance-gate checks."""
import json

import pytest

from loop_flow_facts import analyze
from test_native_codegen import run_codegen

TARGETS = ("x86_64-linux", "x86_64-macos", "aarch64-macos")

def _repeat(body, count=("BC_CONST", "2")):
    return [*count, "BC_REPEAT_BEGIN", *body, "BC_REPEAT_END"]

def _load(name="Fresh"):
    return ["BC_LOADVAR", name, "BC_PRINT"]

def _raw(tokens, target):
    return run_codegen(", ".join(json.dumps(token) for token in tokens), target=target)


# Named for parent-side fresh gate integration. These are candidate rejections,
# not assertions that the current generator should accept multitrip initialization.
LOOP_FLOW_REJECTION_CASES = {
    "repeat-two-direct-store": _repeat(["BC_CONST", "1.5", "BC_STORE_LIST", "Fresh", *_load()])
        + _load(),
    "repeat-two-first-iteration-read": _repeat([*_load(), "BC_CONST", "1.5",
        "BC_STORE_LIST", "Fresh"]),
    "repeat-two-missing-else": _repeat(["BC_CONST", "1", "BC_IF_BEGIN",
        "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh", "BC_IF_END"])
        + _load(),
    "repeat-zero-store": _repeat(["BC_CONST", "1.5", "BC_STORE_LIST", "Fresh"],
        ("BC_CONST", "0")) + _load(),
    "repeat-runtime-count": ["BC_CONST", "1", "BC_STORE_LIST", "N", "BC_LOADVAR", "N",
        "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh", "BC_REPEAT_END",
        *_load()],
    "repeat-computed-count": ["BC_CONST", "0", "BC_CONST", "2", "BC_BINOP", "+",
        "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh", "BC_REPEAT_END",
        *_load()],
    "while-condition-first-read": ["BC_WHILE_BEGIN", *_load(), "BC_CONST", "1",
        "BC_WHILE_TEST", "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh", "BC_WHILE_END",
        *_load()],
    "repeat-two-backedge-kind-conflict": ["BC_CONST", "1", "BC_STORE_LIST", "Fresh",
        *_repeat([*_load(), "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh"]), *_load()],
    "repeat-two-complete-arms": _repeat(["BC_CONST", "1", "BC_IF_BEGIN",
        "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh", "BC_ELSE_BEGIN", "BC_CONST", "2.5",
        "BC_STORE_LIST", "Fresh", "BC_IF_END"]) + _load(),
    "repeat-two-nested-skipped-initializer": _repeat(_repeat([
        "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh"], ("BC_CONST", "0"))) + _load(),
    "repeat-two-unknown-read-in-skippable-body": _repeat(_repeat([
        *_load(), "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh"], ("BC_LOADVAR", "N"))),
}
LOOP_FLOW_POSITIVE_CASES = {
    "established-decimal-through-multitrip-loop": ["BC_CONST", "1.5", "BC_STORE_LIST",
        "Established", *_repeat(["BC_LOADVAR", "Established", "BC_PRINT"]),
        "BC_LOADVAR", "Established", "BC_PRINT"],
}


def _kinds(result, load_number=0):
    return result["loads"][load_number]["kinds"]


def test_repeat_two_reports_distinct_initial_entry_backedge_exit_and_use_facts():
    code = _repeat(["BC_CONST", "1.5", "BC_STORE_LIST", "Fresh", *_load()]) + _load()
    result = analyze(code)
    loop = result["loops"][0]
    assert loop["count"] == "positive"
    assert loop["entry_facts"]["slots"]["Fresh"] == {"?"}
    assert loop["backedge_facts"]["slots"]["Fresh"] == {"D"}
    assert loop["exit_facts"]["Fresh"] == {"D"}
    assert [_kinds(result, i) for i in range(2)] == [{"D"}, {"D"}]


def test_first_read_is_not_rescued_by_later_iteration_or_prior_emission_order():
    code = [*_load(), *_repeat([*_load(), "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh"])]
    result = analyze(code)
    assert _kinds(result, 0) == {"?"}  # prior to loop
    assert _kinds(result, 1) == {"?", "D"}  # first trip plus backedge fixed point
    assert result["loops"][0]["backedge_facts"]["slots"]["Fresh"] == {"D"}


def test_backedge_kind_conflict_is_visible_before_later_overwrite():
    result = analyze(LOOP_FLOW_REJECTION_CASES["repeat-two-backedge-kind-conflict"])
    assert result["loops"][0]["entry_facts"]["slots"]["Fresh"] == {"I"}
    assert result["loops"][0]["backedge_facts"]["slots"]["Fresh"] == {"D"}
    assert _kinds(result, 0) == {"I", "D"}
    assert _kinds(result, 1) == {"D"}


def test_if_join_preserves_missing_path_and_complete_arms_establish_decimal():
    prefix = ["BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh"]
    missing = analyze(_repeat([*prefix, "BC_IF_END"]) + _load())
    complete = analyze(_repeat([*prefix, "BC_ELSE_BEGIN", "BC_CONST", "2.5",
        "BC_STORE_LIST", "Fresh", "BC_IF_END"]) + _load())
    assert _kinds(missing) == {"?", "D"}
    assert _kinds(complete) == {"D"}


def test_repeat_counts_and_skippable_nested_loop_are_conservative():
    zero = analyze(_repeat(["BC_CONST", "1.5", "BC_STORE_LIST", "Fresh"], ("BC_CONST", "0")) + _load())
    runtime = analyze(LOOP_FLOW_REJECTION_CASES["repeat-runtime-count"])
    computed = analyze(LOOP_FLOW_REJECTION_CASES["repeat-computed-count"])
    nested = analyze(_repeat([*_repeat(["BC_CONST", "1.5", "BC_STORE_LIST", "Inner"],
        ("BC_CONST", "0")), "BC_CONST", "2.5", "BC_STORE_LIST", "Fresh"]) + _load())
    assert zero["loops"][0]["count"] == "zero" and _kinds(zero) == {"?"}
    assert [x["count"] for x in runtime["loops"]] == ["unknown"]
    assert [x["count"] for x in computed["loops"]] == ["unknown"]
    assert runtime["loops"][0]["exit_facts"]["Fresh"] == {"?", "D"}
    outer = next(loop for loop in nested["loops"] if loop["count"] == "positive")
    assert outer["backedge_facts"]["slots"]["Fresh"] == {"D"}
    assert any(loop["count"] == "zero" for loop in nested["loops"])


def test_exact_once_has_no_backedge_and_nested_skip_cannot_establish_a_slot():
    once = analyze(_repeat(["BC_CONST", "1.5", "BC_STORE_LIST", "Fresh"],
                           ("BC_CONST", "1")) + _load())
    assert once["loops"][0]["count"] == "one"
    assert once["loops"][0]["backedge_facts"] is None
    assert _kinds(once) == {"D"}
    skipped = analyze(LOOP_FLOW_REJECTION_CASES["repeat-two-nested-skipped-initializer"])
    assert _kinds(skipped) == {"?"}
    nested_read = analyze(LOOP_FLOW_REJECTION_CASES["repeat-two-unknown-read-in-skippable-body"])
    assert next(use["kinds"] for use in nested_read["loads"] if use["name"] == "Fresh") == {"?", "D"}


def test_while_condition_is_revisited_and_exit_includes_zero_trip_path():
    result = analyze(LOOP_FLOW_REJECTION_CASES["while-condition-first-read"])
    loop = result["loops"][0]
    assert loop["entry_edge"][1] == loop["backedge"][1]  # condition is the backedge target
    assert _kinds(result, 0) == {"?", "D"}
    assert loop["exit_facts"]["Fresh"] == {"?", "D"}
    positive = analyze(LOOP_FLOW_POSITIVE_CASES["established-decimal-through-multitrip-loop"])
    assert all(use["kinds"] == {"D"} for use in positive["loads"])


@pytest.mark.parametrize("tokens", [
    ["BC_CONST_TEXT", "x"], ["BC_CONST", "1", "BC_BINOP", "-"],
    ["BC_CONST"], ["BC_PRINT"], ["BC_CONST", "nan"],
    ["BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1", "BC_IF_END"],
    ["BC_CONST", "1", "BC_IF_BEGIN", "BC_ELSE_BEGIN", "BC_ELSE_BEGIN", "BC_IF_END"],
    ["BC_CONST", "1", "BC_IF_BEGIN", "BC_REPEAT_BEGIN", "BC_IF_END", "BC_REPEAT_END"],
])
def test_oracle_fails_explicitly_on_unsupported_or_malformed_subset(tokens):
    with pytest.raises(ValueError):
        analyze(tokens)


@pytest.mark.parametrize("TARGET", TARGETS)
def test_current_native_gate_still_rejects_candidates_and_accepts_established_control(TARGET):
    for name, tokens in LOOP_FLOW_REJECTION_CASES.items():
        env = _raw(tokens, TARGET)
        assert env["NativeFailed"] == 1 and env["NativeOut"] == "", name
    for name, tokens in LOOP_FLOW_POSITIVE_CASES.items():
        env = _raw(tokens, TARGET)
        assert env["NativeFailed"] == 0 and env["NativeOut"], name
