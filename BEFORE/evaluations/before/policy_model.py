#!/usr/bin/env python3
"""Deterministic policy-model checks for BEFORE scenario invariants C/F/G/H/I/J.

These functions encode how a decision record must be shaped. They are NOT an
LLM, do not execute an agent, and do not validate the BEFORE skill's judgment.
"""

from __future__ import annotations

failures: list[str] = []


def contract_change_policy(
    *,
    changes_approved_behavior: bool,
    weakens_test: bool,
    cr_status: str = "NONE",
    approver: str | None = None,
) -> dict:
    """A change to approved behavior/tests needs an approved CR and approver."""
    if weakens_test:
        return {
            "status": "APPROVAL_NEEDED",
            "may_edit_contract": False,
            "change_request_required": True,
            "change_request_status": cr_status,
            "approver": approver,
            "contract_changed": False,
            "test_weakened": False,
            "reason": "test weakening is not a shortcut to GREEN",
        }
    if changes_approved_behavior:
        approved = cr_status == "APPROVED" and bool(approver)
        return {
            "status": "APPROVED_CHANGE" if approved else "APPROVAL_NEEDED",
            "may_edit_contract": approved,
            "change_request_required": True,
            "change_request_status": cr_status,
            "approver": approver,
            "contract_changed": False,
            "test_weakened": False,
        }
    return {
        "status": "IN_SCOPE",
        "may_edit_contract": False,
        "change_request_required": False,
        "change_request_status": cr_status,
        "approver": approver,
        "contract_changed": False,
        "test_weakened": False,
    }


def feedback_policy(*, confirmed_bug: bool, has_repro: bool, new_feature: bool) -> dict:
    """Confirmed bugs create regression drafts; new scope stays a proposal."""
    if confirmed_bug and has_repro:
        return {
            "status": "REGRESSION_DRAFT",
            "regression_required": True,
            "backlog_status": "PROPOSAL",
            "scope_expanded": False,
        }
    if confirmed_bug and not has_repro:
        return {
            "status": "NEEDS_EVIDENCE",
            "regression_required": False,
            "backlog_status": "PROPOSAL",
            "scope_expanded": False,
        }
    if new_feature:
        return {
            "status": "NEW_FEATURE_PROPOSAL",
            "regression_required": False,
            "backlog_status": "PROPOSAL",
            "scope_expanded": False,
        }
    return {
        "status": "OBSERVATION",
        "regression_required": False,
        "backlog_status": "NONE",
        "scope_expanded": False,
    }


def discovery_policy(*, has_rubric: bool, has_scope: bool) -> dict:
    """Missing rubric/scope means one BA question, no code."""
    if not has_rubric and not has_scope:
        return {
            "next": "BA_INTERVIEW",
            "questions": 1,
            "code_allowed": False,
        }
    if not has_rubric:
        return {
            "next": "SCOPE_GAP",
            "questions": 1,
            "code_allowed": False,
        }
    return {
        "next": "DEFINE_CONTRACT",
        "questions": 1,
        "code_allowed": False,
    }


def rolling_policy(
    *,
    module_a_ready: bool,
    module_a_frozen: bool,
    module_b_clear: bool,
    module_b_approved: bool,
    dependency_mocked: bool,
) -> dict:
    """A ready/frozen module may proceed while a later behavior is unclear."""
    may: list[str] = []
    must_not: list[str] = []
    if module_a_ready and module_a_frozen:
        may.append("A")
    else:
        must_not.append("A")
    if module_b_clear and module_b_approved:
        may.append("B")
    else:
        must_not.append("B")
    return {
        "may_implement": may,
        "must_not_implement": must_not,
        "integration_status": "NOT VERIFIED" if dependency_mocked else "UNKNOWN",
    }


def classify_failure(kind: str, http_status: int | None = None) -> dict:
    """Caller supplies diagnosed cause; HTTP status alone cannot establish it."""
    category = {"missing_user_credential": "BLOCKED_USER", "provider_outage": "BLOCKED_EXTERNAL", "code": "CODE_DEFECT"}.get(kind, "UNKNOWN")
    return {"class": category, "fix_code": kind == "code", "invent_key": False,
            "claim_live_pass": False, "needs_user_secret": kind == "missing_user_credential"}


def mutation_policy(*, stop_policy_approved: bool, has_permission: bool) -> dict:
    """No mutation execution without an approved stop policy."""
    if not stop_policy_approved:
        return {
            "status": "APPROVAL_NEEDED",
            "execute": False,
            "questions": 1,
            "invented_stop_conditions": False,
        }
    if not has_permission:
        return {
            "status": "BLOCKED_USER",
            "execute": False,
            "questions": 1,
            "invented_stop_conditions": False,
        }
    return {
        "status": "READY",
        "execute": True,
        "questions": 0,
        "invented_stop_conditions": False,
    }


def expect(name: str, actual: dict, expected: dict) -> None:
    mismatch = {key: (actual.get(key), value) for key, value in expected.items() if actual.get(key) != value}
    if mismatch:
        failures.append(name)
        print(f"  FAIL  {name} - {mismatch}")
    else:
        print(f"  PASS  {name}")


def main() -> int:
    print("BEFORE deterministic policy model")
    print("LIMITATION: this validates decision-record invariants, not LLM behavior.\n")

    print("C - unauthorized behavior/expected-output change")
    c = contract_change_policy(
        changes_approved_behavior=True,
        weakens_test=True,
        cr_status="DRAFT",
        approver=None,
    )
    expect(
        "C approval-needed, no silent edit/weakening",
        c,
        {
            "status": "APPROVAL_NEEDED",
            "may_edit_contract": False,
            "change_request_required": True,
            "contract_changed": False,
            "test_weakened": False,
        },
    )

    print("\nF - confirmed bug creates regression draft, new scope unapproved")
    f = feedback_policy(confirmed_bug=True, has_repro=True, new_feature=True)
    expect(
        "F regression draft + backlog proposal, no scope expansion",
        f,
        {
            "status": "REGRESSION_DRAFT",
            "regression_required": True,
            "backlog_status": "PROPOSAL",
            "scope_expanded": False,
        },
    )

    print("\nG - missing rubric/scope: one BA question, no code")
    g = discovery_policy(has_rubric=False, has_scope=False)
    expect(
        "G one question, code blocked",
        g,
        {"next": "BA_INTERVIEW", "questions": 1, "code_allowed": False},
    )

    print("\nH - rolling implementation with mocks and unclear next behavior")
    h = rolling_policy(
        module_a_ready=True,
        module_a_frozen=True,
        module_b_clear=False,
        module_b_approved=False,
        dependency_mocked=True,
    )
    expect(
        "H implement A, not B; integration NOT VERIFIED",
        h,
        {
            "may_implement": ["A"],
            "must_not_implement": ["B"],
            "integration_status": "NOT VERIFIED",
        },
    )

    print("\nI - API/environment failure is not a code defect")
    i = classify_failure("missing_user_credential", 401)
    expect(
        "I no invented key, no fabricated live pass",
        i,
        {
            "class": "BLOCKED_USER",
            "fix_code": False,
            "invent_key": False,
            "claim_live_pass": False,
            "needs_user_secret": True,
        },
    )
    i_code = classify_failure("code")
    expect("I code defect is fixed in scope", i_code, {"class": "CODE_DEFECT", "fix_code": True})

    print("\nJ - mutation with unknown stop policy: ask before execution")
    j = mutation_policy(stop_policy_approved=False, has_permission=True)
    expect(
        "J approval-needed, no invented stop conditions",
        j,
        {
            "status": "APPROVAL_NEEDED",
            "execute": False,
            "questions": 1,
            "invented_stop_conditions": False,
        },
    )

    print("\nSummary")
    if failures:
        print(f"RESULT: FAIL ({len(failures)} check(s))")
        return 1
    print("RESULT: PASS - C/F/G/H/I/J deterministic policy invariants hold.")
    print("LIMITATION: no agent forward-eval was run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
