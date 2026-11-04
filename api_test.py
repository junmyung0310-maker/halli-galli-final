
import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_PUBLISHABLE_KEY")

if not url or not key:
    raise ValueError(".env 파일의 Supabase 설정을 확인하세요.")

response = requests.post(
    f"{url.rstrip('/')}/rest/v1/rankings",
    headers={
        "apikey": key,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    },
    json={
        "nickname": "TestPlayer",
        "score": 100
    },
    timeout=10
)

print("상태 코드:", response.status_code)
print("서버 응답:", response.text)

response.raise_for_status()
print("점수 등록 성공!")


# Supabase에서 상위 5명 랭킹 조회
print("\n=== 온라인 랭킹 TOP 5 ===")

response = requests.get(
    f"{url.rstrip('/')}/rest/v1/rankings",
    headers={
        "apikey": key
    },
    params={
        "select": "nickname,score",
        "order": "score.desc",
        "limit": "5"
    },
    timeout=10
)

response.raise_for_status()
rankings = response.json()

for rank, player in enumerate(rankings, start=1):
    print(f"{rank}위: {player['nickname']} - {player['score']}점")
