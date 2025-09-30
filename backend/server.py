from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.grader import grade_submission
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW: serve frontend build if present ---
frontend_path = os.getenv("FRONTEND_DIST", "frontend_dist")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_path, "index.html"))

# --- your existing code ---
class Submission(BaseModel):
    username: str
    code: str

@app.get("/ping")
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
