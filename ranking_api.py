"""Supabase REST API helpers for the Halli Galli leaderboard."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def _config():
    url = os.getenv('SUPABASE_URL', '').strip().rstrip('/')
    key = os.getenv('SUPABASE_PUBLISHABLE_KEY', '').strip()
    if not url or not key:
        raise ValueError('Supabase 설정이 없습니다. .env 파일을 확인하세요.')
    if not url.startswith('https://') or '/rest/v1' in url:
        raise ValueError('SUPABASE_URL에는 https://...supabase.co 기본 주소만 입력하세요.')
    return f'{url}/rest/v1/rankings', {'apikey': key}


def submit_score(nickname, score):
    nickname = nickname.strip()
    if not 1 <= len(nickname) <= 20:
        raise ValueError('닉네임은 1~20자로 입력하세요.')
    if not isinstance(score, int) or not 0 <= score <= 100000:
        raise ValueError('점수 범위가 올바르지 않습니다.')
    endpoint, headers = _config()
    response = requests.post(endpoint, headers={**headers, 'Content-Type': 'application/json'},
                             json={'nickname': nickname, 'score': score}, timeout=8)
    response.raise_for_status()


def get_top_rankings(limit=5):
    endpoint, headers = _config()
    response = requests.get(endpoint, headers=headers,
                            params={'select': 'nickname,score', 'order': 'score.desc,created_at.asc', 'limit': str(limit)},
                            timeout=8)
    response.raise_for_status()
    return response.json()
