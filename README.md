# NTU OA Platform

A Replit-integrated Online Assessment (OA) system built for Coding Nights, a technical event hosted by IEEE NTU and Women in Tech.

The platform allows users to submit code, evaluate it against test cases, and view scores on a leaderboard.

## Directory Structure

```
aryand43-dsa-oa-platform/
├── README.md
├── requirements.txt
├── Dockerfile
├── frontend/                  # Vite + React client
│   ├── index.html
│   ├── src/
│   └── ...
├── boilerplate/
│   ├── main.py                # User-facing solve() scaffold
│   └── test_cases.json        # Public + hidden test cases
└── backend/
    ├── server.py              # FastAPI app (API + static frontend)
    ├── grader.py              # Executes user code using exec()
    ├── leaderboard.py         # (WIP) Tracks scores + rankings
    └── models.py              # Optional Pydantic schemas
```

## Features

* Code submission via `/submit` endpoint
* Grading with public and hidden test cases
* Controlled code execution using `exec()`
* Dockerized backend and frontend
* Leaderboard logic (WIP)

## Quickstart

Install dependencies:

```
pip install -r requirements.txt
```

Run backend server:

```
uvicorn backend.server:app --reload
```

Run full stack with Docker:

```
docker build -t dsa-oa-backend .
docker run -p 8000:8000 dsa-oa-backend
```

Visit: [http://localhost:8000](http://localhost:8000)

## Sample POST Request

```
POST /submit
Content-Type: application/json

{
  "username": "john_doe",
  "code": "def solve():\n    print('Hello')\n\nif __name__ == '__main__':\n    solve()"
}
```

## Roadmap

* Full leaderboard logic
* Docker-based code sandboxing
* Test case randomization
* Replit UI integration
