# backend/models.py
from __future__ import annotations
from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, Field


# Request submit
class SubmissionRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    code: str = Field(..., min_length=1)


# Grader result shapes (optional but useful for validation)
class TestCasePublicResult(BaseModel):
    input: str
    expected: str
    output: str
    passed: bool

class TestCaseHiddenResult(BaseModel):
    output: str
    passed: bool

class GradeDetails(BaseModel):
    public: List[TestCasePublicResult]
    hidden: List[TestCaseHiddenResult]

OverallStatus = Literal["AC", "PARTIAL", "WA", "RE", "TLE"]

class GradeResponse(BaseModel):
    username: str
    passed: int
    total: int
    status: OverallStatus
    details: GradeDetails


# Leaderboard shapes (for future use)
class LeaderboardEntry(BaseModel):
    username: str
    score: int
    total: int
    submissions: int
    last_submission: datetime

class LeaderboardResponse(BaseModel):
    entries: List[LeaderboardEntry]

# --- Helpers to build GradeResponse from raw grader dict ---

def _calc_status(passed: int, total: int, had_runtime: bool, had_tle: bool) -> OverallStatus:
    if had_tle:
        return "TLE"
    if total == 0:
        return "RE"
    if passed == total:
        return "AC"
    if passed == 0:
        # If there were runtime errors on all, you may still prefer RE; keep WA here.
        return "WA"
    return "PARTIAL"


def grade_response_from_grader(username: str, raw: dict) -> GradeResponse:
    """
    Convert grader raw dict into a structured GradeResponse.

    Expected raw shape:
      {
        "public": [{"input": "...", "expected": "...", "output": "...", "passed": bool}, ...],
        "hidden": [{"output": "...", "passed": bool}, ...]
      }
    """
    # Build details (validate against the Pydantic models)
    public_items = [TestCasePublicResult(**tc) for tc in raw.get("public", [])]
    hidden_items = [TestCaseHiddenResult(**tc) for tc in raw.get("hidden", [])]

    total = len(public_items) + len(hidden_items)
    passed = sum(int(tc.passed) for tc in public_items) + sum(int(tc.passed) for tc in hidden_items)

    # Detect errors encoded in output strings (optional but helpful)
    def _has_prefix(xs, prefix: str) -> bool:
        for tc in xs:
            out = getattr(tc, "output", "")
            if isinstance(out, str) and out.startswith(prefix):
                return True
        return False

    had_runtime = _has_prefix(public_items, "[Runtime Error]") or _has_prefix(hidden_items, "[Runtime Error]")
    had_tle = _has_prefix(public_items, "[Time Limit Exceeded]") or _has_prefix(hidden_items, "[Time Limit Exceeded]")

    status = _calc_status(passed, total, had_runtime, had_tle)

    return GradeResponse(
        username=username,
        passed=passed,
        total=total,
        status=status,
        details=GradeDetails(public=public_items, hidden=hidden_items),
    )

