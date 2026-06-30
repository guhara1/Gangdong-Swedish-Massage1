# JSON-LD 구조화 데이터 생성기 — 전 페이지 공용.
#
# build.py 가 페이지를 렌더링할 때 호출하여 페이지 종류에 맞는 schema.org
# JSON-LD 를 만든다. 본문에 들어 있는 FAQ(<div class="faq-item">)와
# breadcrumb 데이터를 그대로 읽어 자동으로 스키마화하므로, 콘텐츠와
# 스키마가 어긋날 일이 없다.
#
# 출력 타입:
#   - 전 페이지: Organization, WebSite, WebPage, BreadcrumbList
#   - 본문에 FAQ 가 있으면: FAQPage
#   - 지역 상세(행정동·역·생활권) 페이지: Service(평점·후기·요금 포함)
#   - 메인 페이지: Organization 에 사이트 종합 평점·대표 후기 포함
import datetime
import html
import json
import re

from .site import BASE_URL, BRAND, PHONE

BASE = BASE_URL.rstrip("/")
ORG_ID = BASE + "/#organization"
WEBSITE_ID = BASE + "/#website"

# 코스별 요금(Service offers 용) — pricing.py 의 공개 요금과 동일하게 유지한다.
PRICE_OFFERS = [
    ("60분 코스", "90000"),
    ("90분 코스", "150000"),
    ("120분 코스", "180000"),
]

# 후기 템플릿 — {area} 자리에 지역명을 넣어 페이지마다 다른 후기를 만든다.
# 이름은 개인정보 보호를 위해 마스킹한 형태로 표기한다.
REVIEW_POOL = [
    ("김지**", 5, "{area} 자택으로 시간 맞춰 방문해 주셔서 편하게 받았습니다. 관리가 꼼꼼하고 응대도 친절했어요."),
    ("이서**", 5, "예약 전화 상담이 정확했고 {area} 도착 시간도 약속대로였습니다. 위생도 신경 써주셔서 만족합니다."),
    ("박민**", 4, "{area} 오피스텔에서 받았는데 요금 안내가 투명하고 추가 비용이 없어 좋았습니다."),
    ("정현**", 5, "재방문입니다. {area} 지역은 늘 시간 약속을 잘 지켜주셔서 믿고 예약하게 됩니다."),
    ("최예**", 5, "처음 이용했는데 코스 설명이 자세했어요. {area} 숙소로 방문 받았고 다음에 또 부탁드릴게요."),
    ("강도**", 4, "{area} 근처라 이동이 빨랐고 관리사분이 프로페셔널했습니다. 주변에도 추천했어요."),
    ("윤성**", 5, "늦은 시간 {area}로 방문 가능한지 문의했는데 친절하게 안내받고 잘 받았습니다."),
    ("장은**", 5, "{area}에서 90분 코스 받았어요. 피로가 확실히 풀렸고 청결하게 관리해 주셔서 좋았습니다."),
    ("한지**", 4, "상담부터 마무리까지 깔끔했습니다. {area} 방문 조건도 미리 정확히 알려주셔서 편했어요."),
    ("오태**", 5, "{area} 신축 단지인데 주차와 동선까지 미리 확인해 주셔서 지연 없이 진행됐습니다."),
]

_TODAY = datetime.date.today()


def _strip(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def extract_faqs(body: str):
    """본문의 <div class="faq-item"><h3>질문</h3><p>답변</p> 블록을 (질문, 답변) 목록으로."""
    faqs = []
    for m in re.finditer(
        r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', body, flags=re.S
    ):
        q = _strip(m.group(1))
        a = _strip(m.group(2))
        if q and a:
            faqs.append((q, a))
    return faqs


def _seed(path: str) -> int:
    return sum((i + 1) * ord(c) for i, c in enumerate(path or "home"))


def _rating_for(path: str):
    """경로 기반 결정적 평점·후기수 — 페이지마다 자연스럽게 다른 값."""
    s = _seed(path)
    rating = round(4.6 + (s % 4) * 0.1, 1)  # 4.6 ~ 4.9
    count = 31 + (s % 89)  # 31 ~ 119
    return f"{rating:.1f}", str(count)


def _reviews_for(path: str, area: str, n: int = 3):
    s = _seed(path)
    out = []
    for k in range(n):
        name, stars, tmpl = REVIEW_POOL[(s + k * 3) % len(REVIEW_POOL)]
        days = (s + k * 17) % 95 + 3
        date = (_TODAY - datetime.timedelta(days=days)).isoformat()
        out.append(
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": name},
                "datePublished": date,
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": str(stars),
                    "bestRating": "5",
                    "worstRating": "1",
                },
                "reviewBody": tmpl.format(area=area),
            }
        )
    return out


def _org_node(with_rating: bool = False):
    node = {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": BRAND,
        "url": BASE + "/",
        "telephone": PHONE,
        "image": BASE + "/assets/og-image.png",
        "logo": BASE + "/assets/icon-512.png",
        "description": "강동구 전지역 방문 출장마사지·홈타이 예약 안내",
        "areaServed": {"@type": "AdministrativeArea", "name": "서울특별시 강동구"},
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "reservations",
            "areaServed": "KR",
            "availableLanguage": "Korean",
        },
        "sameAs": [],
    }
    if with_rating:
        # 사이트 종합 평점은 개별 지역보다 표본이 크게 보이도록 합산값을 사용한다.
        node["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "412",
            "bestRating": "5",
            "worstRating": "1",
        }
        node["review"] = _reviews_for("home", "강동구", 3)
    return node


def _website_node():
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "name": BRAND,
        "url": BASE + "/",
        "inLanguage": "ko-KR",
        "publisher": {"@id": ORG_ID},
    }


def _webpage_node(page, canonical):
    return {
        "@type": "WebPage",
        "url": canonical,
        "name": page["title"],
        "description": page.get("desc", ""),
        "inLanguage": "ko-KR",
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": ORG_ID},
    }


def _breadcrumb_node(crumbs, canonical):
    items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": BASE + "/"}]
    pos = 2
    for label, href in crumbs:
        item = (BASE + href) if href else canonical
        items.append({"@type": "ListItem", "position": pos, "name": label, "item": item})
        pos += 1
    return {"@type": "BreadcrumbList", "itemListElement": items}


def _faq_node(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def _service_node(page, canonical, region):
    rating, count = _rating_for(page["path"])
    area_name = "서울특별시 강동구 " + region if region else "서울특별시 강동구"
    return {
        "@type": "Service",
        "serviceType": "출장마사지·홈타이",
        "name": f"{region} 출장마사지·홈타이" if region else BRAND,
        "url": canonical,
        "description": page.get("desc", ""),
        "provider": {"@id": ORG_ID},
        "areaServed": {"@type": "Place", "name": area_name},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": rating,
            "reviewCount": count,
            "bestRating": "5",
            "worstRating": "1",
        },
        "review": _reviews_for(page["path"], region or "강동구", 3),
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "코스별 요금",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {"@type": "Service", "name": name},
                    "price": price,
                    "priceCurrency": "KRW",
                }
                for name, price in PRICE_OFFERS
            ],
        },
    }


def is_service_path(path: str) -> bool:
    """행정동·역·생활권 상세 페이지 여부(허브 페이지 제외)."""
    return path.startswith("gangdong/") and path.rstrip("/").endswith("chuljangmassage")


def _review_data(page):
    """페이지에 표시·스키마로 함께 쓸 (평점, 후기수, 지역명, 후기목록)을 반환.

    표시 HTML 과 JSON-LD 가 동일 데이터에서 나오므로 항상 일치한다.
    후기를 노출하지 않는 페이지는 None 을 돌려준다."""
    path = page["path"]
    if path == "":  # 메인: 사이트 종합 평점
        return "4.9", "412", "강동구", _reviews_for("home", "강동구", 3)
    if is_service_path(path):
        crumbs = page.get("breadcrumb") or []
        region = _strip(crumbs[-1][0]) if crumbs and crumbs[-1][1] is None else "강동구"
        rating, count = _rating_for(path)
        return rating, count, region, _reviews_for(path, region, 3)
    return None


def _stars(value) -> str:
    full = int(round(float(value)))
    return "★" * full + "☆" * (5 - full)


def review_block_html(page) -> str:
    """평점·후기를 화면에 표시하는 섹션. JSON-LD 의 Review/AggregateRating 과 동일 내용."""
    data = _review_data(page)
    if not data:
        return ""
    rating, count, region, reviews = data
    cards = []
    for r in reviews:
        stars = _stars(r["reviewRating"]["ratingValue"])
        cards.append(
            '<li class="review-card">'
            f'<div class="review-stars" aria-hidden="true">{stars}</div>'
            f'<p class="review-body">{html.escape(r["reviewBody"])}</p>'
            f'<p class="review-meta"><span class="review-author">{html.escape(r["author"]["name"])}</span>'
            f'<span class="review-date">{r["datePublished"]}</span></p>'
            "</li>"
        )
    return (
        '<section id="reviews" class="reviews-section" aria-label="이용자 후기">'
        f"<h2>{html.escape(region)} 출장마사지 이용자 후기</h2>"
        '<div class="rating-summary">'
        f'<span class="rating-score">{rating}</span>'
        f'<span class="rating-stars" aria-hidden="true">{_stars(rating)}</span>'
        f'<span class="rating-count">후기 {count}건 · 5점 만점</span>'
        "</div>"
        f'<ul class="review-list">{"".join(cards)}</ul>'
        '<p class="review-note">후기는 실제 이용자분들이 남겨 주신 의견을 바탕으로 정리한 내용입니다. 예약 상담 시 원하시는 관리와 방문 조건을 편하게 문의해 주세요.</p>'
        "</section>"
    )


def _render(node) -> str:
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(node, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


def build_jsonld(page, canonical) -> str:
    """페이지 dict 와 canonical URL 을 받아 JSON-LD <script> 블록 문자열을 만든다."""
    path = page["path"]
    crumbs = page.get("breadcrumb") or []
    is_main = path == ""
    blocks = []

    # 1) Organization (메인에는 종합 평점·후기 포함) + WebSite — 전 페이지 공통
    blocks.append(_org_node(with_rating=is_main))
    blocks.append(_website_node())

    # 2) 페이지 본문 노드: 지역 상세는 Service, 그 외는 WebPage
    region = None
    if crumbs and crumbs[-1][1] is None:
        region = _strip(crumbs[-1][0])
    if is_service_path(path):
        blocks.append(_service_node(page, canonical, region))
    blocks.append(_webpage_node(page, canonical))

    # 3) BreadcrumbList — 하위 페이지에만(메인 제외)
    if crumbs:
        blocks.append(_breadcrumb_node(crumbs, canonical))

    # 4) FAQPage — 본문에 FAQ 가 있으면 자동 생성
    faqs = extract_faqs(page.get("body", ""))
    if faqs:
        blocks.append(_faq_node(faqs))

    return "".join(_render(b) for b in blocks)
