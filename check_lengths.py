#!/usr/bin/env python3
"""각 페이지의 실제 본문(태그 제거·요금블록 제외) 글자수를 출력한다.
build.py 의 text_length 와 동일한 기준. 2000자 미만이면 noindex 처리된다."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import text_length, MIN_INDEX_CHARS
from content import PAGES

rows = []
for p in PAGES:
    n = text_length(p["body"])
    rows.append((p["path"] or "/", n, p.get("noindex", False)))

for path, n, forced in sorted(rows):
    status = "noindex" if (forced or n < MIN_INDEX_CHARS) else "index"
    flag = "  <-- under 2000" if (not forced and n < MIN_INDEX_CHARS) else ""
    print(f"{n:5d}  {status:8s}  {path}{flag}")

under = [r for r in rows if not r[2] and r[1] < MIN_INDEX_CHARS]
print(f"\n{len(rows)} pages, {len(under)} under threshold (excluding intentional noindex).")
