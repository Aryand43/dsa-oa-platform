# backend/server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.grader import grade_submission
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Submission(BaseModel):
    username: str
    code: str  # Code content from user

@app.get("/")
def read_root():
    return {"msg": "NTU OA backend is live."}

@app.post("/submit")
def submit_code(submission: Submission):
    try:
        results = grade_submission(submission.code)
        return {
            "username": submission.username,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leaderboard")
def get_leaderboard():
    from backend.leaderboard import get_scores
    return get_scores()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
