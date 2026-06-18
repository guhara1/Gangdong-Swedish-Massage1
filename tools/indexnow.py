#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 스크립트.

빌드(`python3 build.py`)로 생성된 indexnow-urls.txt 의 URL을
IndexNow 참여 검색엔진(Bing·Naver·Yandex·Seznam)에 한 번에 통보한다.
api.indexnow.org 로 보내면 참여 엔진 전체로 전파된다.

사용법:
  python3 build.py                 # URL 목록 갱신
  python3 tools/indexnow.py        # 전체 URL 일괄 통보
  python3 tools/indexnow.py URL …  # 특정 URL만 통보(글 올릴 때마다)

표준 라이브러리만 사용하므로 별도 설치가 필요 없다.
"""
import json
import os
import sys
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = BASE_URL.rstrip("/")
HOST = BASE.split("://", 1)[-1]
KEY_LOCATION = f"{BASE}/{INDEXNOW_KEY}.txt"

# api.indexnow.org 하나면 참여 엔진 전체로 전파된다.
# 개별 엔드포인트도 함께 두어 전파 지연을 줄인다.
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://searchadvisor.naver.com/indexnow",
]


def load_urls(args):
    if args:
        return args
    path = os.path.join(ROOT, "indexnow-urls.txt")
    if not os.path.exists(path):
        sys.exit("indexnow-urls.txt 가 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def submit(endpoint, urls):
    payload = json.dumps({
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(
        endpoint, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read(200).decode("utf-8", "ignore").strip()
    except urllib.error.HTTPError as e:
        return e.code, e.read(200).decode("utf-8", "ignore").strip()
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def main():
    urls = load_urls(sys.argv[1:])
    if not urls:
        sys.exit("통보할 URL이 없습니다.")
    print(f"호스트: {HOST}")
    print(f"키 파일: {KEY_LOCATION}")
    print(f"통보 URL {len(urls)}개")
    for ep in ENDPOINTS:
        status, body = submit(ep, urls)
        # 200/202 = 접수, 그 외는 메시지 확인
        mark = "✓" if status in (200, 202) else "✗"
        print(f"  {mark} {ep} → {status} {body}")
    print("\n완료. (200/202 응답이면 정상 접수입니다.)")
    print("참고: 키 파일이 실제 도메인에 배포된 뒤에 통보해야 검증을 통과합니다.")


if __name__ == "__main__":
    main()
