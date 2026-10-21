#!/usr/bin/env python3
"""Structural and decision-sync checks for the BEFORE bundle (stdlib only)."""

from __future__ import annotations

from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
SKILL = PROJECT / ".agents" / "skills" / "before"
DECISIONS = PROJECT / "BEFORE_DECISIONS.md"
SNAPSHOT = SKILL / "references" / "decisions.md"
USAGE = PROJECT / "BEFORE_USAGE.md"

failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}" + (f" - {detail}" if detail else ""))
        failures.append(name)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    print("BEFORE bundle structure and decision-sync check")
    print(f"project: {PROJECT}\n")

    required = [
        DECISIONS,
        USAGE,
        SKILL / "SKILL.md",
        SKILL / "references" / "contract-and-discovery.md",
        SKILL / "references" / "execution-gates-lifecycle.md",
        SKILL / "references" / "feedback-and-pilot.md",
        SKILL / "references" / "decisions.md",
        SKILL / "assets" / "project-rubric.template.md",
        SKILL / "assets" / "behavior-contract.template.md",
        SKILL / "assets" / "mini-goal.template.md",
        SKILL / "assets" / "evidence.template.md",
        SKILL / "assets" / "change-request.template.md",
        SKILL / "assets" / "decision-assumption.template.md",
        SKILL / "assets" / "uat-regression.template.md",
        SKILL / "assets" / "pilot-log.template.md",
        PROJECT / "evaluations" / "before" / "run_fixture.py",
        PROJECT / "evaluations" / "before" / "policy_model.py",
        PROJECT / "evaluations" / "before" / "forward-scenarios.md",
    ]
    missing = [str(path.relative_to(PROJECT)) for path in required if not path.is_file()]
    check("required files exist", not missing, f"missing={missing}")

    root_text = read(DECISIONS)
    snapshot_text = read(SNAPSHOT)
    skill_text = read(SKILL / "SKILL.md")
    usage_text = read(USAGE)

    decision_ids = [f"D-{index:02d}" for index in range(1, 15)]
    interview_ids = [f"PI-{index:02d}" for index in range(1, 9)]
    history_ids = [f"HM-{index:02d}" for index in range(1, 8)]

    for label, ids in (
        ("D-01..D-14", decision_ids),
        ("PI-01..PI-08", interview_ids),
        ("HM-01..HM-07", history_ids),
    ):
        root_missing = [item for item in ids if item not in root_text]
        snap_missing = [item for item in ids if item not in snapshot_text]
        check(
            f"{label} present in canonical + snapshot",
            not root_missing and not snap_missing,
            f"root={root_missing}, snapshot={snap_missing}",
        )

    source_ids = (
        [f"U{index}" for index in range(1, 8)]
        + [f"P{index}" for index in range(1, 11)]
        + [f"O{index}" for index in range(1, 8)]
        + ["C1", "C2"]
    )
    missing_source = [item for item in source_ids if item not in root_text]
    check("U1-U7/P1-P10/O1-O7/C1-C2 in canonical", not missing_source, f"missing={missing_source}")

    modes = [
        "define-contract",
        "execute-mini-goal",
        "verify-gate",
        "refactor-safely",
        "capture-feedback/replan",
    ]
    missing_modes = [item for item in modes if item not in skill_text]
    check("five mode names in SKILL.md", not missing_modes, f"missing={missing_modes}")
    actions = ["capture-feedback", "replan"]
    missing_actions = [item for item in actions if item not in skill_text]
    check("capture-feedback + replan actions documented", not missing_actions, f"missing={missing_actions}")

    missing_refs = [
        item
        for item in (
            "references/contract-and-discovery.md",
            "references/execution-gates-lifecycle.md",
            "references/feedback-and-pilot.md",
            "references/decisions.md",
        )
        if item not in skill_text
    ]
    check("references are linked from SKILL.md", not missing_refs, f"missing={missing_refs}")

    check("usage has $before examples", "$before" in usage_text)
    check("root and snapshot share version 1.0", "1.0" in root_text and "1.0" in snapshot_text)
    check("no TODO scaffold placeholder", "TODO" not in skill_text and "TODO" not in snapshot_text)

    print("\nSummary")
    if failures:
        print(f"RESULT: FAIL ({len(failures)} check(s))")
        return 1
    print("RESULT: PASS - structure, mode names, references, decision IDs and snapshot sync markers hold.")
    print("LIMITATION: this checks presence/sync markers, not semantic correctness or runtime discovery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
