# 바로GO — 강동 출장마사지·홈타이 안내 사이트

강동구 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
content/
  site.py           # 상호(바로GO)·전화·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (Organization/WebPage/FAQPage JSON-LD)
  areas.py          # 대표 행정동: 강동구 허브 + 대표 행정동 9개
  stations.py       # 지하철역별: 허브 + 5·8호선 12개 역
  districts.py      # 생활권·주요 거점: 허브 + 거점 8개
  info.py           # 예약안내·이용 전 확인사항·홈타이 가이드·고객센터·약관
  about.py          # 운영자 소개(E-E-A-T)
  pricing.py        # 공용 요금 블록
assets/             # CSS, 모바일 내비 JS, 파비콘/OG 이미지
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 메타 description은 **80자 이내**로 작성
- 대표 행정동은 9개만 (강일·상일·명일·고덕·암사·천호·성내·길동·둔촌) — 번호 행정동 페이지 없음
- 역은 역 1개당 페이지 1개 — 천호역 같은 환승역도 URL 하나, 출구별·노선별 페이지 없음
- **지역+역+테마 조합 페이지 없음** (도어웨이 방지)
- 방문형 사이트라 오프라인 주소 기반 LocalBusiness Schema는 사용하지 않음
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)

## 검색엔진 색인 / 빠른 인덱싱

빌드(`python3 build.py`) 시 색인 관련 파일이 자동 생성됩니다.

- `sitemap.xml` — `lastmod`·`changefreq`·`priority` 포함 (색인 대상 38개)
- `rss.xml` — RSS 2.0 피드 (전 페이지 `<head>`에 자동 발견 링크 포함)
- `robots.txt` — 전 봇 허용 + Googlebot·Yeti(네이버)·bingbot·Daum 명시 + sitemap 위치
- `{IndexNow키}.txt` — IndexNow 검증용 키 파일 (루트)
- `indexnow-urls.txt` — 통보용 URL 목록
- 메인페이지 `<head>`에 네이버 사이트 인증 메타태그

### 즉시 색인 통보 (IndexNow → 빙·네이버·얀덱스)

```bash
python3 build.py            # URL 목록 갱신
python3 tools/indexnow.py   # 모든 URL을 빙·네이버 등에 즉시 통보
# 글/페이지 추가 시 해당 URL만:
python3 tools/indexnow.py https://gangdong-swedish-massage1.pages.dev/새URL/
```

> IndexNow 키 파일(`{key}.txt`)이 실제 도메인에 배포된 뒤에 통보해야 검증을 통과합니다.

### 구글 (IndexNow 미참여)

- 기본: `sitemap.xml`을 **Google Search Console**에 제출 (가장 확실)
- 선택: `tools/google_indexing.py` — Indexing API로 즉시 통보 (서비스 계정 JSON 필요, 공식상 채용/방송 페이지용이라 일반 페이지 효과는 보장되지 않음)
- 참고: 구글·빙의 `sitemap ping` 엔드포인트는 2023년 폐지되어 더 이상 동작하지 않습니다.

### 네이버

- **네이버 서치어드바이저**에 사이트 등록 → 메인페이지의 인증 메타태그로 소유 확인
- `sitemap.xml`·`rss.xml` 제출, IndexNow로 즉시 통보 가능 (네이버 IndexNow 참여)

## 총 페이지 구성

- 메인 1
- 대표 행정동 허브 1 + 행정동 9
- 지하철역 허브 1 + 역 12
- 생활권·거점 허브 1 + 거점 8
- 예약안내 / 이용 전 확인사항 / 홈타이 이용 가이드 / 고객센터 / 개인정보처리방침 / 이용약관 / 운영자 소개
