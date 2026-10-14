"""A small, self-contained public demonstration of an auditable AI workflow.

It is intentionally independent from private KC 3Agent source code.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class Event:
    step: str
    status: str
    detail: str


def _event(step: str, status: str, detail: str) -> dict[str, str]:
    return asdict(Event(step=step, status=status, detail=detail))


def run_task(task: dict[str, Any], force_test_failure: bool = False) -> dict[str, Any]:
    """Execute a deterministic TASK → ARCHITECT → RUNNER → TESTER → CONTROLLER flow."""
    title = str(task["title"])
    expected_phrase = str(task["expected_phrase"])
    audit = [_event("TASK", "accepted", title)]

    plan = {
        "objective": title,
        "acceptance_criterion": f"Output contains: {expected_phrase}",
    }
    audit.append(_event("ARCHITECT", "planned", plan["acceptance_criterion"]))

    output = f"Implementation completed with {expected_phrase}."
    audit.append(_event("RUNNER", "completed", output))

    test_passed = expected_phrase in output and not force_test_failure
    tester_status = "passed" if test_passed else "failed"
    tester_detail = "Deterministic assertion passed." if test_passed else "Expected phrase assertion failed."
    audit.append(_event("TESTER", tester_status, tester_detail))

    if test_passed:
        result = {"status": "passed", "summary": "Task completed and verified."}
    else:
        result = {
            "status": "failed",
            "summary": "Task was not released because the test gate failed.",
            "error_code": "TEST_GATE_FAILED",
        }
    audit.append(_event("CONTROLLER", result["status"], result["summary"]))

    return {"task": task, "plan": plan, "runner_output": output, "result": result, "audit_trail": audit}
