# NTU OA Platform

A Replit-based Online Assessment (OA) system designed for Coding Nights, a technical event hosted by IEEE NTU and Women in Tech.

This platform allows users to write code inside Replit, submit it via an API, automatically evaluate it against test cases, and view rankings on a leaderboard.

## Directory Structure

```
aryand43-dsa-oa-platform/
├── README.md
├── requirements.txt
├── boilerplate/
│   ├── main.py              # User-facing solve() scaffold
│   └── test_cases.json      # Public and hidden test cases
└── backend/
    ├── server.py            # FastAPI API server (handles /submit)
    ├── grader.py            # Evaluates user code safely using exec()
    ├── leaderboard.py       # (To be implemented) Tracks user scores
    └── models.py            # (Optional) Pydantic schemas
```

## Features (So Far)

* Accepts user code and username via POST `/submit`
* Grades the code using predefined test cases
* Supports public and hidden test cases
* Logs submissions and scores (to be implemented)
* Displays real-time leaderboard (to be implemented)
* Stress test support for Replit backend (planned)

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

Run the FastAPI server:

```
uvicorn backend.server:app --reload
```

## Sample POST Request

```
POST /submit
{
  "username": "john_doe",
  "code": "def solve():\n    print('Hello')\n\nif __name__ == '__main__':\n    solve()"
}
```

## Work In Progress

This repository is under active development. Expect regular updates as we add:

* Full leaderboard logic
* Docker-based sandboxing
* Test case randomization
* Replit UI integration
