# backend/grader.py

import io
import json
import contextlib
from typing import List, Dict


def load_test_cases(filepath: str = "boilerplate/test_cases.json") -> Dict:
    with open(filepath, "r") as f:
        return json.load(f)


def run_code_with_input(code: str, input_data: str) -> str:
    # Simulate input() calls using input_data
    stdin = io.StringIO(input_data)
    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stdin(stdin):
            exec(code, {})
    except Exception as e:
        return f"[Runtime Error] {str(e)}"

    return stdout.getvalue()


def compare_output(user_output: str, expected_output: str) -> bool:
    return user_output.strip() == expected_output.strip()


def grade_submission(user_code: str) -> Dict[str, List[Dict]]:
    test_data = load_test_cases()
    results = {"public": [], "hidden": []}

    for test_case in test_data["public_tests"]:
        output = run_code_with_input(user_code, test_case["input"])
        passed = compare_output(output, test_case["expected_output"])
        results["public"].append({
            "input": test_case["input"],
            "expected": test_case["expected_output"],
            "output": output,
            "passed": passed
        })

    for test_case in test_data["hidden_tests"]:
        output = run_code_with_input(user_code, test_case["input"])
        passed = compare_output(output, test_case["expected_output"])
        results["hidden"].append({
            "output": output,
            "passed": passed
        })

    return results
