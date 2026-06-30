# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
# 방문형 사이트(오프라인 사업장 주소 없음)이므로 LocalBusiness Schema는 사용하지 않고
# Organization · WebSite · WebPage · BreadcrumbList · FAQPage · Service(평점·후기) 를 사용한다.
# JSON-LD 스키마는 build.py 에서 페이지 데이터(본문 FAQ·breadcrumb 등)를 읽어 일괄 생성한다.
from .site import PHONE, PHONE_DISPLAY
from .pricing import PRICING

# 네이버 서치어드바이저 사이트 소유 확인용 메타 태그(메인 페이지에만 출력).
_NAVER = '<meta name="naver-site-verification" content="2b3409bd0feae08cda5bb324931224ca59559ace" />\n'

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 강동구 전지역</p>
    <h1>강동 출장마사지·강동구 홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 프리미엄 방문 관리.<br>자택·오피스텔·숙소 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/gangdong/">지역별 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>9개</strong><span>대표 행정동</span></li>
      <li><strong>12개</strong><span>역세권 안내</span></li>
      <li><strong>8개</strong><span>생활권·거점</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="why">
<h2>강동구에서 출장마사지를 찾는 이유</h2>
<p>강동 출장마사지를 찾는 분들은 대부분 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 강동구는 서울 동쪽 끝에 자리해 하남, 송파, 광진, 경기 남양주 생활권과 맞닿아 있습니다. 천호동과 성내동은 천호역·강동역·강동구청역을 중심으로 상권과 주거지가 섞여 있고, 고덕동과 상일동은 고덕비즈밸리·상일동역·고덕역을 중심으로 업무와 주거 수요가 함께 있습니다. 암사동은 암사역·암사역사공원역과 선사유적지 생활권을, 강일동은 강일역과 하남 인접 생활권을 함께 고려해야 합니다. 이 페이지는 강동구 전체 구조를 설명하는 허브 역할을 하며, 자세한 내용은 대표 행정동·지하철역·생활권 안내 페이지에서 확인하실 수 있습니다.</p>
</section>

<section id="areas">
<h2>대표 행정동별 방문 가능 지역 안내</h2>
<p>강동구 지역 안내는 강일동, 상일동, 명일동, 고덕동, 암사동, 천호동, 성내동, 길동, 둔촌동 아홉 개 대표 행정동을 중심으로 구성합니다. 상일1동·상일2동은 상일동으로, 명일1동·명일2동은 명일동으로, 고덕1동·고덕2동은 고덕동으로, 암사1동부터 암사3동은 암사동으로, 천호1동부터 천호3동은 천호동으로, 성내1동부터 성내3동은 성내동으로, 둔촌1동·둔촌2동은 둔촌동으로 통합해 안내합니다. 번호로 나뉜 행정동을 잘게 쪼개 비슷한 내용을 반복하는 것보다, 대표 동 단위로 묶어 생활권 특징과 방문 조건을 한 번에 설명하는 편이 이용자에게도 정확하기 때문입니다.</p>
<ul class="card-grid">
<li><a href="/gangdong/gangil-dong-chuljangmassage/">강일동 출장마사지<span>강일역·고덕강일 생활권</span></a></li>
<li><a href="/gangdong/sangil-dong-chuljangmassage/">상일동 출장마사지<span>상일동역·고덕 인접</span></a></li>
<li><a href="/gangdong/myeongil-dong-chuljangmassage/">명일동 출장마사지<span>명일역·굽은다리역</span></a></li>
<li><a href="/gangdong/godeok-dong-chuljangmassage/">고덕동 출장마사지<span>고덕역·고덕비즈밸리</span></a></li>
<li><a href="/gangdong/amsa-dong-chuljangmassage/">암사동 출장마사지<span>암사역·선사유적지</span></a></li>
<li><a href="/gangdong/cheonho-dong-chuljangmassage/">천호동 출장마사지<span>천호역·로데오거리</span></a></li>
<li><a href="/gangdong/seongnae-dong-chuljangmassage/">성내동 출장마사지<span>강동구청역 생활권</span></a></li>
<li><a href="/gangdong/gil-dong-chuljangmassage/">길동 출장마사지<span>길동역·길동사거리</span></a></li>
<li><a href="/gangdong/dunchon-dong-chuljangmassage/">둔촌동 출장마사지<span>둔촌동역·올림픽파크포레온</span></a></li>
</ul>
<p>강동구 전체 구조가 궁금하시면 <a href="/gangdong/">대표 행정동 전체 안내</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>천호역·강동역·고덕역·암사역 역세권 안내</h2>
<p>지하철역별 안내는 강동구를 지나는 5호선·8호선 주요 역세권을 기준으로 구성합니다. 각 역 페이지에서는 인근 생활권, 주변 대표 동, 예약 가능 시간, 방문 전 준비사항을 설명하며, 출구별 페이지나 역과 테마를 조합한 페이지는 만들지 않습니다. 천호역처럼 5호선과 8호선이 만나는 환승역도 노선별로 나누지 않고 한 페이지로만 운영합니다. 2024년 8월 개통한 8호선 별내선 암사역사공원역도 단독 역세권 페이지로 안내합니다.</p>
<ul class="card-grid">
<li><a href="/gangdong/cheonho-station-chuljangmassage/">천호역 출장마사지<span>5·8호선 환승</span></a></li>
<li><a href="/gangdong/gangdong-station-chuljangmassage/">강동역 출장마사지<span>5호선</span></a></li>
<li><a href="/gangdong/gil-dong-station-chuljangmassage/">길동역 출장마사지<span>5호선</span></a></li>
<li><a href="/gangdong/gubeundari-station-chuljangmassage/">굽은다리역 출장마사지<span>5호선</span></a></li>
<li><a href="/gangdong/myeongil-station-chuljangmassage/">명일역 출장마사지<span>5호선</span></a></li>
<li><a href="/gangdong/godeok-station-chuljangmassage/">고덕역 출장마사지<span>5호선</span></a></li>
<li><a href="/gangdong/sangildong-station-chuljangmassage/">상일동역 출장마사지<span>5호선</span></a></li>
<li><a href="/gangdong/gangil-station-chuljangmassage/">강일역 출장마사지<span>5호선</span></a></li>
<li><a href="/gangdong/dunchon-dong-station-chuljangmassage/">둔촌동역 출장마사지<span>9호선</span></a></li>
<li><a href="/gangdong/amsa-station-chuljangmassage/">암사역 출장마사지<span>8호선</span></a></li>
<li><a href="/gangdong/amsa-history-park-station-chuljangmassage/">암사역사공원역 출장마사지<span>8호선 별내선</span></a></li>
<li><a href="/gangdong/gangdong-gu-office-station-chuljangmassage/">강동구청역 출장마사지<span>8호선</span></a></li>
</ul>
</section>

<section id="living">
<h2>고덕·상일·강일 생활권과 천호·성내 생활권 차이</h2>
<p>같은 강동구라도 생활권에 따라 방문 조건이 달라집니다. 천호·성내 생활권은 천호역과 강동구청역을 낀 상권형 지역이라 늦은 시간 숙소·오피스텔 방문 문의가 많고, 고덕·상일·강일 생활권은 업무지구와 신축 단지가 섞인 주거형 지역이라 자택 방문과 차량 이동 기준이 더 중요합니다. 생활권·거점 안내에서는 천호 로데오거리, 고덕비즈밸리, 암사 선사유적지 인근, 둔촌동 올림픽파크포레온처럼 검색 의도가 뚜렷한 거점을 따로 정리했습니다.</p>
<ul class="card-grid">
<li><a href="/gangdong/cheonho-rodeo-area-chuljangmassage/">천호 로데오거리 출장마사지<span>천호동 번화가</span></a></li>
<li><a href="/gangdong/godeok-business-valley-chuljangmassage/">고덕비즈밸리 출장마사지<span>업무지구</span></a></li>
<li><a href="/gangdong/amsa-prehistoric-area-chuljangmassage/">암사 선사유적지 인근 출장마사지<span>암사동 한강변</span></a></li>
<li><a href="/gangdong/dunchon-olympic-park-foreon-chuljangmassage/">올림픽파크포레온 출장마사지<span>둔촌동 대단지</span></a></li>
<li><a href="/gangdong/gil-dong-area-chuljangmassage/">길동사거리 생활권 출장마사지<span>길동 중심상권</span></a></li>
<li><a href="/gangdong/myeongil-area-chuljangmassage/">명일동 주거권 출장마사지<span>학원가·주거지</span></a></li>
<li><a href="/gangdong/sangil-gangil-area-chuljangmassage/">상일·강일 생활권 출장마사지<span>고덕강일 신도시</span></a></li>
<li><a href="/gangdong/seongnae-gangdong-office-area-chuljangmassage/">성내동·강동구청 생활권 출장마사지<span>강동구청 인근</span></a></li>
</ul>
</section>

<section id="check">
<h2>강동 홈타이 예약 전 확인사항</h2>
<p>강동 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비 여부, 결제 방식, 취소 기준, 서비스 범위를 미리 확인하시는 것이 좋습니다. 강동구는 면적이 아주 넓은 편은 아니지만 천호·성내 생활권과 고덕·상일·강일 생활권의 이동 기준이 다릅니다. 특히 강일동, 고덕동, 상일동 일부는 차량 이동 시간이 달라질 수 있으므로 예약 가능 시간과 추가 이동비 여부를 명확하게 확인해 주세요. 자세한 준비사항은 <a href="/checklist/">이용 전 확인사항</a>과 <a href="/reservation/">예약안내</a>에 정리되어 있습니다.</p>
</section>

<section id="guide">
<h2>강동 출장마사지 사이트 이용 가이드</h2>
<p>메인 페이지는 강동구 전체 안내를 담당하고, 대표 행정동 페이지는 강일동·상일동·명일동·고덕동·암사동·천호동·성내동·길동·둔촌동 검색을, 역세권 페이지는 천호역·강동역·고덕역·암사역·암사역사공원역처럼 실제 검색 수요가 생기는 키워드를 담당합니다. 홈타이가 처음이라면 <a href="/hometai-guide/">홈타이 이용 가이드</a>를, 운영 주체와 콘텐츠 기준이 궁금하시면 <a href="/about/">운영자 소개</a>를 확인해 주세요. 과장된 표현 대신 이용 가능 지역, 예약 절차, 취소 기준, 개인정보 처리 기준을 분명하게 안내하는 것을 원칙으로 합니다.</p>
</section>

<section id="topics">
<h2>강동 출장마사지·홈타이 인기 검색 주제</h2>
<p>자주 찾으시는 주제별로 가장 알맞은 안내 페이지를 모았습니다. 원하시는 상황과 가까운 항목을 선택하시면 방문 조건과 예약 방법을 바로 확인하실 수 있습니다. 별도의 조합 페이지를 만들지 않고, 실제 안내가 담긴 지역·이용 안내 페이지로 바로 연결합니다.</p>
<ul class="topic-list">
<li><a href="/reservation/">강동구 24시간 출장마사지 예약 방법</a></li>
<li><a href="/gangdong/cheonho-station-chuljangmassage/">천호역 심야 홈타이 방문 안내</a></li>
<li><a href="/gangdong/godeok-dong-chuljangmassage/">고덕동 자택 방문 마사지</a></li>
<li><a href="/gangdong/gangil-dong-chuljangmassage/">강일동 신축단지 홈타이</a></li>
<li><a href="/gangdong/dunchon-olympic-park-foreon-chuljangmassage/">올림픽파크포레온 출장마사지</a></li>
<li><a href="/gangdong/amsa-history-park-station-chuljangmassage/">암사역사공원역 8호선 별내선 출장마사지</a></li>
<li><a href="/gangdong/gangdong-gu-office-station-chuljangmassage/">강동구청역 직장인 퇴근 후 마사지</a></li>
<li><a href="/gangdong/cheonho-rodeo-area-chuljangmassage/">천호 로데오거리 숙소 홈타이</a></li>
<li><a href="/hometai-guide/#price">출장마사지 요금·코스 안내</a></li>
<li><a href="/hometai-guide/">강동 홈타이 처음 이용 가이드</a></li>
<li><a href="/checklist/">방문 전 확인사항·위생 기준</a></li>
<li><a href="/about/">운영자 소개·운영 원칙</a></li>
</ul>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>강동구 전지역 방문이 가능한가요?</h3>
<p>예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 대표 행정동 안내 페이지에서 강일동, 상일동, 명일동, 고덕동, 암사동, 천호동, 성내동, 길동, 둔촌동 기준으로 확인할 수 있습니다.</p>
</div>
<div class="faq-item">
<h3>천호역이나 고덕역 근처도 가능한가요?</h3>
<p>주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 환승역도 노선별로 페이지를 나누지 않고 역마다 한 페이지로 운영하며, 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다.</p>
</div>
<div class="faq-item">
<h3>천호1동과 천호2동은 왜 따로 없나요?</h3>
<p>번호가 붙은 행정동은 천호동, 성내동, 암사동, 고덕동, 명일동, 상일동, 둔촌동 대표 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다.</p>
</div>
<div class="faq-item">
<h3>강동 홈타이는 출장마사지와 다른가요?</h3>
<p>홈타이는 자택·숙소·사무실 인근으로 방문해 받는 방문형 관리를 가리키는 말로, 출장마사지와 같은 방식입니다. 예약 가능 여부를 먼저 확인한 뒤 이용하시면 됩니다.</p>
</div>
<div class="faq-item">
<h3>당일 예약도 가능한가요?</h3>
<p>가능할 수 있지만 저녁 시간대와 주말은 문의가 많을 수 있어 사전 예약을 권장합니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>강동구 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "강동 출장마사지｜강동구 홈타이 지역별 예약 안내",
    "desc": "강동 출장마사지·홈타이 예약 전 행정동, 역세권, 이용 기준을 정리했습니다.",
    "h1": "강동 출장마사지·강동구 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _NAVER,
    "breadcrumb": [],
    "hero": _HERO,
}
