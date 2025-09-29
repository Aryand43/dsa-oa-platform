# backend/leaderboard.py
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

_LEADERBOARD_PATH = os.environ.get(
    "OA_LEADERBOARD_PATH",
    os.path.join(os.path.dirname(__file__), "leaderboard.json"),
)
_LOCK = threading.Lock()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load() -> Dict[str, dict]:
    if not os.path.exists(_LEADERBOARD_PATH):
        return {}
    try:
        with open(_LEADERBOARD_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save(store: Dict[str, dict]) -> None:
    os.makedirs(os.path.dirname(_LEADERBOARD_PATH), exist_ok=True)
    tmp = _LEADERBOARD_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _LEADERBOARD_PATH)


def _compute_passed_total(results: Dict[str, Any]) -> Tuple[int, int]:
    public = results.get("public", [])
    hidden = results.get("hidden", [])
    passed = sum(int(x.get("passed", False)) for x in public) + \
             sum(int(x.get("passed", False)) for x in hidden)
    total = len(public) + len(hidden)
    return passed, total


def update_scores(username: str, results: Dict[str, Any]) -> Dict[str, Any]:
    """Update leaderboard with a submission; keep best score."""
    passed, total = _compute_passed_total(results)
    with _LOCK:
        store = _load()
        prev = store.get(username)
        if prev is None:
            entry = {
                "username": username,
                "score": passed,
                "total": total,
                "submissions": 1,
                "last_submission": _now_iso(),
            }
        else:
            best = max(int(prev.get("score", 0)), passed)  # use 'passed' to switch to "latest score"
            entry = {
                "username": username,
                "score": best,
                "total": total,
                "submissions": int(prev.get("submissions", 0)) + 1,
                "last_submission": _now_iso(),
            }
        store[username] = entry
        _save(store)
        return entry


def get_scores(top: Optional[int] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Return sorted leaderboard as {'entries': [...]}."""
    with _LOCK:
        store = _load()

    def sort_key(item):
        _, e = item
        try:
            ts = datetime.fromisoformat(e.get("last_submission", "1970-01-01T00:00:00+00:00"))
        except Exception:
            ts = datetime(1970, 1, 1, tzinfo=timezone.utc)
        return (-int(e.get("score", 0)), int(e.get("submissions", 0)), ts)

    items = sorted(store.items(), key=sort_key)
    if top:
        items = items[:top]
    return {"entries": [v for _, v in items]}


def reset() -> None:
    with _LOCK:
        _save({})
