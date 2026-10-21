#!/usr/bin/env python3
"""Deterministic fixture for BEFORE mechanics.

This script runs real unittest suites against real candidate implementations.
It demonstrates actual RED/GREEN for scenarios A, B, D, E. It is NOT an agent
forward-evaluation and does not prove that the BEFORE skill makes good decisions.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "fixture"
CANDIDATES = FIXTURE / "candidates"

ACCEPTANCE = "acceptance"
SAFETY = "safety"

failures: list[str] = []


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}" + (f" - {detail}" if detail else ""))
        failures.append(name)


def run_candidate(candidate: str, suite: str) -> tuple[int, str, str]:
    cmd_display = f"python -m unittest -v tests.{suite}.test_order_total"
    with tempfile.TemporaryDirectory(prefix="before-eval-") as tmp:
        workspace = Path(tmp)
        shutil.copytree(FIXTURE / "tests", workspace / "tests")
        (workspace / "app").mkdir()
        shutil.copy2(FIXTURE / "app" / "__init__.py", workspace / "app" / "__init__.py")
        shutil.copy2(CANDIDATES / f"{candidate}.py", workspace / "app" / "order_total.py")
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "-v", f"tests.{suite}.test_order_total"],
            cwd=workspace,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode, output, cmd_display


def excerpt(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    interesting = [
        line
        for line in lines
        if line.startswith(("OK", "FAILED", "NotImplementedError", "AssertionError"))
        or line.startswith("FAIL:")
        or line.startswith("ERROR:")
    ]
    return " | ".join(interesting[-4:]) if interesting else " | ".join(lines[-3:])


def observe(label: str, candidate: str, suite: str) -> tuple[int, str, str]:
    code, output, command = run_candidate(candidate, suite)
    print(f"  [{label}] {command} -> exit={code}")
    print(f"           {excerpt(output)}")
    return code, output, command


def main() -> int:
    print("BEFORE deterministic fixture")
    print(f"root: {ROOT}")
    print("Note: actual unittest runs; this is not an LLM forward-eval.\n")

    contract_hash = digest(FIXTURE / "contract.md")
    acceptance_hash = digest(FIXTURE / "tests" / "acceptance" / "test_order_total.py")
    safety_hash = digest(FIXTURE / "tests" / "safety" / "test_order_total.py")

    print("A - atomic mini-goal: RED because behavior is missing, then GREEN")
    a_red_code, a_red_out, _ = observe("A-RED", "baseline", ACCEPTANCE)
    check("A RED fails", a_red_code != 0, f"exit={a_red_code}")
    check(
        "A RED reason is missing behavior",
        "NotImplementedError" in a_red_out,
        "expected NotImplementedError",
    )
    a_green_code, a_green_out, _ = observe("A-GREEN", "good", ACCEPTANCE)
    check("A GREEN acceptance passes", a_green_code == 0, f"exit={a_green_code}")
    a_safety_code, a_safety_out, _ = observe("A-SAFETY", "good", SAFETY)
    check("A safety baseline passes", a_safety_code == 0, f"exit={a_safety_code}")
    check(
        "A contract/tests unchanged",
        contract_hash == digest(FIXTURE / "contract.md")
        and acceptance_hash == digest(FIXTURE / "tests" / "acceptance" / "test_order_total.py")
        and safety_hash == digest(FIXTURE / "tests" / "safety" / "test_order_total.py"),
    )

    print("\nB - in-scope failure: fix implementation, never tests/contract")
    b_fail_code, b_fail_out, _ = observe("B-FAIL", "buggy", ACCEPTANCE)
    check("B failing test is observed", b_fail_code != 0, f"exit={b_fail_code}")
    check(
        "B failure is the rounding behavior",
        "test_half_up_rounding" in b_fail_out,
        "expected test_half_up_rounding failure",
    )
    b_fix_code, b_fix_out, _ = observe("B-FIX", "good", ACCEPTANCE)
    check("B final acceptance passes", b_fix_code == 0, f"exit={b_fix_code}")
    check(
        "B contract/tests unchanged",
        contract_hash == digest(FIXTURE / "contract.md")
        and acceptance_hash == digest(FIXTURE / "tests" / "acceptance" / "test_order_total.py")
        and safety_hash == digest(FIXTURE / "tests" / "safety" / "test_order_total.py"),
    )

    print("\nD - safety failure: acceptance green is not release-ready")
    d_acc_code, d_acc_out, _ = observe("D-ACCEPTANCE", "unsafe", ACCEPTANCE)
    check("D acceptance passes", d_acc_code == 0, f"exit={d_acc_code}")
    d_safety_code, d_safety_out, _ = observe("D-SAFETY", "unsafe", SAFETY)
    check("D safety fails", d_safety_code != 0, f"exit={d_safety_code}")
    check(
        "D failure is the integer-cents invariant",
        "test_total_is_integer_cents" in d_safety_out,
        "expected test_total_is_integer_cents failure",
    )
    release_ready_unsafe = (d_acc_code == 0) and (d_safety_code == 0)
    check("D not release-ready", release_ready_unsafe is False)
    d_fix_acc_code, d_fix_acc_out, _ = observe("D-FIX-ACCEPTANCE", "good", ACCEPTANCE)
    d_fix_code, d_fix_out, _ = observe("D-FIX-SAFETY", "good", SAFETY)
    check("D fixed acceptance passes", d_fix_acc_code == 0, f"exit={d_fix_acc_code}")
    check("D fixed safety passes", d_fix_code == 0, f"exit={d_fix_code}")
    release_ready_fixed = (d_fix_acc_code == 0) and (d_fix_code == 0)
    check("D fixed becomes release-ready for the fixture gate", release_ready_fixed is True)

    print("\nE - refactor of already-GREEN code: no fake RED")
    e_baseline_code, e_baseline_out, _ = observe("E-BASELINE", "good", ACCEPTANCE)
    check("E baseline is GREEN before refactor", e_baseline_code == 0, f"exit={e_baseline_code}")
    e_bad_code, e_bad_out, _ = observe("E-BAD-REFACTOR", "refactor_bad", ACCEPTANCE)
    check("E regression catches changed output", e_bad_code != 0, f"exit={e_bad_code}")
    check(
        "E failure is half-up behavior",
        "test_half_up_rounding" in e_bad_out,
        "expected test_half_up_rounding failure",
    )
    e_restore_code, e_restore_out, _ = observe("E-RESTORE", "good", ACCEPTANCE)
    check("E compatible behavior restored", e_restore_code == 0, f"exit={e_restore_code}")
    check("E no fake initial RED created", e_baseline_code == 0)
    check(
        "E contract/tests unchanged",
        contract_hash == digest(FIXTURE / "contract.md")
        and acceptance_hash == digest(FIXTURE / "tests" / "acceptance" / "test_order_total.py")
        and safety_hash == digest(FIXTURE / "tests" / "safety" / "test_order_total.py"),
    )

    print("\nSummary")
    if failures:
        print(f"RESULT: FAIL ({len(failures)} check(s))")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("RESULT: PASS - A/B/D/E observed with real unittest exit codes.")
    print("LIMITATION: deterministic fixture only; no LLM behavior was evaluated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
