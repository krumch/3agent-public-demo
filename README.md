# 3Agent Public Demo

This is a small, independent demonstration of an auditable engineering workflow:

```text
TASK → ARCHITECT → RUNNER → TESTER → CONTROLLER → RESULT
```

It is **not** private KC 3Agent source code. It exists solely to demonstrate the working style: explicit state, deterministic test gates, controlled failure, and an audit trail.

## Run

```bash
python run_demo.py
python -m unittest discover -s tests -v
```

`run_demo.py` creates three inspectable files in `artifacts/`:

- `state_success.json` — complete passing state;
- `audit_trail.json` — ordered decisions and status transitions;
- `failure_log.json` — a deliberately failed test gate that prevents release.

## Design Notes

- The controller only releases a result after the tester passes.
- A failure is represented explicitly with `TEST_GATE_FAILED`; it is not silently converted into success.
- The code uses only Python's standard library; no package installation is needed.
