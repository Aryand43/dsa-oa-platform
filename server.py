from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import uuid
from grader import grade_submission
import os
import json

app = FastAPI()
if os.path.exists("leaderboard.json"):
    with open("leaderboard.json", "r") as f:
        submissions = json.load(f)
else:
    submissions = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for dev
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
submissions: List[Dict] = []

class Submission(BaseModel):
    user_id: str
    problem_id: str
    code: str

@app.post("/submit")
async def submit_code(submission: Submission):
    result = grade_submission(
    code=submission.code,
    problem_id=submission.problem_id,
    user_id=submission.user_id
    )

    global submissions

    # Find existing submission for the same user and problem
    existing = next(
        (entry for entry in submissions
        if entry["user_id"] == submission.user_id and entry["problem_id"] == submission.problem_id),
        None
    )

    # Replace only if the new score is higher
    if existing:
        if result["submission_entry"]["score"] > existing["score"]:
            submissions = [entry for entry in submissions if entry != existing]
            submissions.append(result["submission_entry"])
        else:
            pass  # keep the old higher score
    else:
        submissions.append(result["submission_entry"])

    # Save to leaderboard.json
    with open("leaderboard.json", "w") as f:
        json.dump(submissions, f, indent=2, default=str)

@app.get("/leaderboard")
async def get_leaderboard():
    if not submissions:
        return {"leaderboard": []}

    # Sort by score (descending), then by timestamp (ascending)
    sorted_subs = sorted(submissions, key=lambda x: (-x["score"], x["timestamp"]))

    leaderboard = []
    seen = set()

    for entry in sorted_subs:
        uid = entry["user_id"]
        # Keep only the best/latest score per user
        if uid not in seen:
            leaderboard.append({
                "user_id": uid,
                "score": entry["score"],
                "replay_result": entry["replay_result"],
                "timestamp": entry["timestamp"]
            })
            seen.add(uid)

    return {"leaderboard": leaderboard}

@app.get("/problems")
def list_problems():
    problems = []
    for file in os.listdir("test_cases"):
        if file.endswith(".json"):
            try:
                with open(f"test_cases/{file}", "r") as f:
                    data = json.load(f)
                    if "test_cases" in data:
                        problems.append(file.replace(".json", ""))
            except Exception as e:
                continue  # skip invalid JSON files
    return {"problems": problems}