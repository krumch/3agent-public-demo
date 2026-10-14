"""Run both success and controlled-failure scenarios and write inspectable JSON artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from workflow import run_task


ROOT = Path(__file__).parent
TASK = {"title": "Validate a profile update", "expected_phrase": "input validation"}


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    artifacts = ROOT / "artifacts"
    artifacts.mkdir(exist_ok=True)
    successful = run_task(TASK)
    failed = run_task(TASK, force_test_failure=True)
    write_json(artifacts / "state_success.json", successful)
    write_json(artifacts / "audit_trail.json", successful["audit_trail"])
    write_json(artifacts / "failure_log.json", failed)
    print("Wrote success state, audit trail, and controlled failure log.")


if __name__ == "__main__":
    main()
