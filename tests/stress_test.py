import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8000/submit"
USERNAMES = [f"user_{i}" for i in range(30)]

def simulate_submission(username):
    payload = {
        "username": username,
        "code": f"print('Hello from {username}')"
    }
    try:
        response = requests.post(URL, json=payload)
        print(f"[{username}] Status: {response.status_code}, Result: {response.json()}")
    except Exception as e:
        print(f"[{username}] Error: {str(e)}")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(simulate_submission, USERNAMES)