import subprocess
import tempfile
import json
import uuid
from datetime import datetime

def grade_submission(user_code: str, test_data: dict):
    question = test_data["question"]
    test_cases = test_data["test_cases"]

    # Build the namespace for execution
    namespace = {}
    try:
        exec(user_code, namespace)
    except Exception as e:
        return {"error": f"Code execution failed: {e}", "score": 0}

    passed = 0
    total = len(test_cases)
    results = []

    for case in test_cases:
        test_case_id = case.get("test_case_id", None)
        input_data = case["input"]
        expected_output = case["expected_output"]

        try:
            # Dynamically call the function with unpacked input
            result = namespace[question](**input_data)
            passed_test = result == expected_output
        except Exception as e:
            result = f"Error: {e}"
            passed_test = False

        if passed_test:
            passed += 1

        results.append({
            "test_case_id": test_case_id,
            "input": input_data,
            "expected_output": expected_output,
            "actual_output": result,
            "passed": passed_test
        })

    score = int((passed / total) * 100)

    return {
        "question": question,
        "score": score,
        "passed": passed,
        "total": total,
        "results": results
    }