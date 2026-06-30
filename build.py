#!/usr/bin/env python3
"""바로GO — 강동 출장마사지·홈타이 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import html
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, NAV, PHONE, PHONE_DISPLAY,
                          INDEXNOW_KEY)
from content.schema import build_jsonld, review_block_html
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_related(current_path: str) -> str:
    """지역(행정동·역·생활권) 페이지 하단에 들어가는 전지역 내부링크 블록.

    NAV 데이터를 그대로 활용해 동·역·생활권 전체를 롱테일 앵커로 연결한다.
    페이지마다 동일한 사이트 내비게이션 성격의 컨텍스트 링크 모음이다."""
    cur = "/" + current_path
    cols = []
    for label, href, children in NAV:
        if not href.startswith("/gangdong"):
            continue
        links = []
        for c_label, c_href in children:
            if c_href == href:  # "…전체" 항목은 그룹 제목 링크로 대체
                continue
            active = ' class="is-current" aria-current="page"' if c_href == cur else ""
            links.append(f'<li><a href="{c_href}"{active}>{c_label} 출장마사지</a></li>')
        cols.append(
            '<div class="related-col">'
            f'<p class="related-col-title"><a href="{href}">{label}</a></p>'
            f'<ul>{"".join(links)}</ul></div>'
        )
    cols.append(
        '<div class="related-col">'
        '<p class="related-col-title"><a href="/reservation/">이용 안내</a></p>'
        '<ul>'
        '<li><a href="/reservation/">예약안내 · 예약 방법</a></li>'
        '<li><a href="/checklist/">이용 전 확인사항</a></li>'
        '<li><a href="/hometai-guide/">홈타이 이용 가이드</a></li>'
        '<li><a href="/about/">운영자 소개</a></li>'
        '<li><a href="/support/">고객센터 · 자주 묻는 질문</a></li>'
        '</ul></div>'
    )
    return (
        '<section id="related-areas" class="related-areas" aria-label="강동구 전지역 안내 바로가기">'
        '<h2>강동구 전지역 출장마사지·홈타이 바로가기</h2>'
        '<p class="related-lead">찾으시는 동네·지하철역·생활권을 선택하면 해당 지역의 방문 조건과 예약 안내를 자세히 확인하실 수 있습니다.</p>'
        f'<div class="related-grid">{"".join(cols)}</div>'
        '</section>'
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    # 이용자 후기 블록(평점·후기) — 메인·지역 상세 페이지에 본문 끝에 붙인다.
    # JSON-LD 의 Review/AggregateRating 과 동일한 데이터로 생성되어 항상 일치한다.
    body = body + review_block_html(page)

    # 지역(행정동·역·생활권) 페이지에는 전지역 내부링크 블록을 본문 끝에 붙인다.
    if path.startswith("gangdong/"):
        body = body + render_related(path)

    # JSON-LD 구조화 데이터(전 페이지 공통 + 페이지 종류별)를 head 에 주입한다.
    extra_head = extra_head + build_jsonld(page, canonical)

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{BRAND} RSS" href="{BASE_URL.rstrip('/')}/rss.xml">
{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">바</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 강동구 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">강동구 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 서울특별시 강동구 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="지역 안내">
      <p class="footer-title">지역 안내</p>
      <ul>
        <li><a href="/gangdong/">대표 행정동별 안내</a></li>
        <li><a href="/gangdong/stations/">지하철역별 안내</a></li>
        <li><a href="/gangdong/areas/">생활권·거점 안내</a></li>
        <li><a href="/reservation/">예약안내</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/checklist/">이용 전 확인사항</a></li>
        <li><a href="/hometai-guide/">홈타이 이용 가이드</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">운영자 소개</a></li>
        <li><a href="/support/privacy/">개인정보처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/checklist/#hygiene">위생·안전 기준</a></li>
        <li><a href="/checklist/#prohibited">금지행위 안내</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <div class="footer-cta-group">
        <a class="footer-cta-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow"><svg class="tg-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M21.94 4.66 18.6 20.4c-.25 1.1-.9 1.37-1.83.86l-5.05-3.72-2.44 2.35c-.27.27-.5.5-1.02.5l.36-5.16 9.39-8.48c.41-.36-.09-.56-.63-.2L4.16 13.2.16 11.94c-1.09-.34-1.11-1.09.23-1.61l17.6-6.78c.91-.34 1.7.2 1.4 1.61z"/></svg>웹사이트 제작문의 ↗</a>
        <a class="footer-cta-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow"><svg class="tg-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M21.94 4.66 18.6 20.4c-.25 1.1-.9 1.37-1.83.86l-5.05-3.72-2.44 2.35c-.27.27-.5.5-1.02.5l.36-5.16 9.39-8.48c.41-.36-.09-.56-.63-.2L4.16 13.2.16 11.94c-1.09-.34-1.11-1.09.23-1.61l17.6-6.78c.91-.34 1.7.2 1.4 1.61z"/></svg>제휴문의 ↗</a>
      </div>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    indexed = []  # (url, title, desc) — 색인 허용 페이지

    base = BASE_URL.rstrip("/")
    desc_warnings = []
    for page in PAGES:
        path = page["path"]  # "" 또는 "gangdong/cheonho-dong-chuljangmassage/" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        # 메타 description 은 80자 이내 규칙
        desc_len = len(page.get("desc", ""))
        if desc_len > 80:
            desc_warnings.append((path or "/", desc_len))

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            indexed.append((base + "/" + path, page["title"], page["desc"]))
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    today = datetime.date.today().isoformat()
    now_rfc822 = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S +0000"
    )

    # sitemap.xml — lastmod·changefreq·priority 포함(색인 속도에 도움)
    # 페이지 성격별로 우선순위·갱신주기를 차등화해 크롤러가 중요한 페이지를
    # 더 자주, 먼저 수집하도록 유도한다.
    hub_paths = {"gangdong/", "gangdong/stations/", "gangdong/areas/"}

    def sitemap_meta(url):
        rel = url[len(base) + 1 :]  # base 뒤 경로("" = 메인)
        if rel == "":
            return "1.0", "daily"
        if rel in hub_paths:
            return "0.9", "weekly"
        if rel.startswith("gangdong/"):
            return "0.8", "weekly"
        return "0.6", "monthly"

    rows = []
    for url, _, _ in indexed:
        priority, changefreq = sitemap_meta(url)
        rows.append(
            f"  <url><loc>{url}</loc><lastmod>{today}</lastmod>"
            f"<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>"
        )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows)
            + "\n</urlset>\n"
        )

    # rss.xml — 색인 봇이 신규/변경 페이지를 빠르게 수집하도록 RSS 2.0 피드 제공
    items = []
    for url, title, desc in indexed:
        items.append(
            "    <item>\n"
            f"      <title>{html.escape(title)}</title>\n"
            f"      <link>{url}</link>\n"
            f"      <guid isPermaLink=\"true\">{url}</guid>\n"
            f"      <description>{html.escape(desc)}</description>\n"
            f"      <pubDate>{now_rfc822}</pubDate>\n"
            "    </item>"
        )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{html.escape(BRAND)} — 강동 출장마사지·홈타이</title>\n"
            f"    <link>{base}/</link>\n"
            f"    <atom:link href=\"{base}/rss.xml\" rel=\"self\" type=\"application/rss+xml\"/>\n"
            "    <description>강동구 전지역 방문 출장마사지·홈타이 안내</description>\n"
            "    <language>ko-KR</language>\n"
            f"    <lastBuildDate>{now_rfc822}</lastBuildDate>\n"
            + "\n".join(items)
            + "\n  </channel>\n</rss>\n"
        )

    # robots.txt — 전 봇 허용 + 주요 봇 명시 + sitemap 위치
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\n"
            "Allow: /\n\n"
            "# 구글\nUser-agent: Googlebot\nAllow: /\n\n"
            "# 네이버\nUser-agent: Yeti\nAllow: /\n\n"
            "# 빙 (IndexNow)\nUser-agent: bingbot\nAllow: /\n\n"
            "# 다음\nUser-agent: Daum\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
        )

    # IndexNow 키 파일 — 루트에 "{key}.txt" (내용은 키 그 자체)
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    # 색인 통보용 URL 목록 (tools/indexnow.py 가 읽음)
    with open(os.path.join(ROOT, "indexnow-urls.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(url for url, _, _ in indexed) + "\n")

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    sitemap_urls = indexed

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")
    if desc_warnings:
        print("\n⚠ description 80자 초과 페이지:")
        for p, n in desc_warnings:
            print(f"  {p}  ({n}자)")
    else:
        print("모든 페이지 description 80자 이내 ✓")


if __name__ == "__main__":
    build()
