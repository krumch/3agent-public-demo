import unittest

from workflow import run_task


TASK = {"title": "Validate a profile update", "expected_phrase": "input validation"}


class WorkflowTests(unittest.TestCase):
    def test_successful_task_has_complete_audit_trail(self) -> None:
        result = run_task(TASK)
        self.assertEqual(result["result"]["status"], "passed")
        self.assertEqual(
            [event["step"] for event in result["audit_trail"]],
            ["TASK", "ARCHITECT", "RUNNER", "TESTER", "CONTROLLER"],
        )

    def test_failed_test_gate_blocks_release(self) -> None:
        result = run_task(TASK, force_test_failure=True)
        self.assertEqual(result["result"]["status"], "failed")
        self.assertEqual(result["result"]["error_code"], "TEST_GATE_FAILED")
