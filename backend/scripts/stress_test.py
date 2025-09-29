# scripts/stress_test.py
import asyncio
import random
import httpx

URL = "http://127.0.0.1:8000"

# Wrong code 
WRONG_CODE = "print(5)"

# Correct code that solves the sample problem for checking duplicates
CORRECT_CODE = """def solve():
    import sys
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    nums = list(map(int, data[1:1+n]))
    print("True" if len(set(nums)) < n else "False")

if __name__ == "__main__":
    solve()
"""

async def submit(client, username, code):
    r = await client.post(
        f"{URL}/submit",
        json={"username": username, "code": code},
        timeout=10.0
    )
    return username, r.status_code, r.json()

async def main(n: int = 40):
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(n):
            username = f"user_{i%5}"  # 5 users 
            code = CORRECT_CODE if random.random() < 0.5 else WRONG_CODE
            tasks.append(submit(client, username, code))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        ac_count = 0
        for res in results:
            if isinstance(res, Exception):
                print("Error:", res)
                continue
            user, status, body = res
            print(f"{user}: HTTP {status}, passed={body['results']['public'][0]['passed']}")
            # Count how many submissions passed at least one public test
            if any(tc["passed"] for tc in body["results"]["public"]):
                ac_count += 1

        print(f"Submissions: {len(results)}, some-pass count: {ac_count}")

        # pring leaderboard
        lb = (await client.get(f"{URL}/leaderboard")).json()
        print("Leaderboard:", lb)


if __name__ == "__main__":
    asyncio.run(main(40))
