import subprocess
import tempfile
import json
import uuid
from datetime import datetime

def grade_submission(code: str, problem_id: str, user_id: str) -> dict:
    # Load test cases from file
    try:
        with open(f"test_cases/{problem_id}.json", "r") as f:
            test_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Test cases for '{problem_id}' not found.")

    test_cases = test_data["test_cases"]
    total_cases = len(test_cases)
    passed_count = 0

    for case in test_cases:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as tmp:
            # Inject user code and input/output redirection logic
            tmp.write(code + "\n")
            tmp.write(f"""
if __name__ == "__main__":
    import sys
    from io import StringIO

    input_data = '''{case['input']}'''
    sys.stdin = StringIO(input_data)

    solve()
""")
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
                continue  # skip on timeout

    # Determine result label
    if passed_count == total_cases:
        replay_result = "passed"
    elif passed_count > 0:
        replay_result = "partially"
    else:
        replay_result = "failed"

    # Construct leaderboard submission entry
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
