#!/usr/bin/env python3
"""Google Indexing API 색인 통보 스크립트 (선택 사항).

구글은 IndexNow에 참여하지 않으므로, 구글에 '즉시' 통보하려면 Indexing API를
써야 한다. 단, 공식적으로는 JobPosting·BroadcastEvent 페이지용 API이며 일반
페이지에 대한 효과는 보장되지 않는다. 평소 구글 색인은 sitemap.xml +
Search Console 등록이 가장 확실하다.

사전 준비:
  1) Google Cloud 프로젝트에서 Indexing API 사용 설정
  2) 서비스 계정 생성 → JSON 키 다운로드
  3) Search Console 속성에 그 서비스 계정 이메일을 '소유자'로 추가
  4) pip install google-auth requests

사용법:
  python3 build.py
  GOOGLE_APPLICATION_CREDENTIALS=service-account.json \
      python3 tools/google_indexing.py            # 전체 URL
  GOOGLE_APPLICATION_CREDENTIALS=service-account.json \
      python3 tools/google_indexing.py URL …       # 특정 URL

참고: 구글/빙 sitemap ping 엔드포인트(/ping?sitemap=)는 2023년 폐지되어
더 이상 동작하지 않는다. 그래서 ping 대신 이 API 또는 Search Console을 쓴다.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from content.site import BASE_URL  # noqa: E402

ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def load_urls(args):
    if args:
        return args
    path = os.path.join(ROOT, "indexnow-urls.txt")
    if not os.path.exists(path):
        sys.exit("indexnow-urls.txt 가 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def main():
    cred = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred or not os.path.exists(cred):
        sys.exit("GOOGLE_APPLICATION_CREDENTIALS 에 서비스 계정 JSON 경로를 지정하세요.")
    try:
        import google.auth.transport.requests
        from google.oauth2 import service_account
        import requests
    except ImportError:
        sys.exit("필요 패키지가 없습니다. `pip install google-auth requests` 후 다시 실행하세요.")

    creds = service_account.Credentials.from_service_account_file(cred, scopes=SCOPES)
    creds.refresh(google.auth.transport.requests.Request())
    headers = {"Authorization": f"Bearer {creds.token}",
               "Content-Type": "application/json"}

    urls = load_urls(sys.argv[1:])
    print(f"Google Indexing API 통보 {len(urls)}개")
    ok = 0
    for u in urls:
        body = {"url": u, "type": "URL_UPDATED"}
        r = requests.post(ENDPOINT, headers=headers, json=body, timeout=30)
        mark = "✓" if r.status_code == 200 else "✗"
        if r.status_code == 200:
            ok += 1
        print(f"  {mark} {u} → {r.status_code}")
    print(f"\n완료: {ok}/{len(urls)} 접수")


if __name__ == "__main__":
    main()
