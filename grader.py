import subprocess
import tempfile
import json
import uuid
from datetime import datetime

def grade_submission(code: str, problem_id: str, user_id: str):
    try:
        with open(f"test_cases/{problem_id}.json", "r") as f:
            test_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Test cases for '{problem_id}' not found.")

    all_tests = test_data.get("public_tests", []) + test_data.get("hidden_tests", [])
    total_cases = len(all_tests)
    passed_count = 0

    for case in all_tests:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as tmp:
            tmp.write(code + "\n")
            tmp.write("""
if __name__ == "__main__":
    import sys
    from io import StringIO

    input_data = \"\"\"{}\"\"\"
    sys.stdin = StringIO(input_data)

    solve()
""".format(case["input"]))
            tmp.flush()

            try:
                result = subprocess.run(
                    ["python", tmp.name],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                user_output = result.stdout.strip()
                expected_output = case["expected_output"].strip()

                if user_output == expected_output:
                    passed_count += 1
            except subprocess.TimeoutExpired:
                continue

    replay_result = "passed" if passed_count == total_cases else (
        "partially" if passed_count > 0 else "failed"
    )

    submission_entry = {
        "submission_id": str(uuid.uuid4()),
        "user_id": user_id,
        "problem_id": problem_id,
        "score": passed_count,
        "replay_result": replay_result,
        "timestamp": datetime.utcnow()
    }

    return {
        "score": passed_count,
        "total": total_cases,
        "replay_result": replay_result,
        "submission_entry": submission_entry
    }
