# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://www.barogo-gangdong.example.com"

BRAND = "바로GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("홈", "/", []),
    ("대표 행정동", "/gangdong/", [
        ("강동구 전체", "/gangdong/"),
        ("강일동", "/gangdong/gangil-dong-chuljangmassage/"),
        ("상일동", "/gangdong/sangil-dong-chuljangmassage/"),
        ("명일동", "/gangdong/myeongil-dong-chuljangmassage/"),
        ("고덕동", "/gangdong/godeok-dong-chuljangmassage/"),
        ("암사동", "/gangdong/amsa-dong-chuljangmassage/"),
        ("천호동", "/gangdong/cheonho-dong-chuljangmassage/"),
        ("성내동", "/gangdong/seongnae-dong-chuljangmassage/"),
        ("길동", "/gangdong/gil-dong-chuljangmassage/"),
        ("둔촌동", "/gangdong/dunchon-dong-chuljangmassage/"),
    ]),
    ("지하철역", "/gangdong/stations/", [
        ("역 전체", "/gangdong/stations/"),
        ("천호역", "/gangdong/cheonho-station-chuljangmassage/"),
        ("강동역", "/gangdong/gangdong-station-chuljangmassage/"),
        ("길동역", "/gangdong/gil-dong-station-chuljangmassage/"),
        ("굽은다리역", "/gangdong/gubeundari-station-chuljangmassage/"),
        ("명일역", "/gangdong/myeongil-station-chuljangmassage/"),
        ("고덕역", "/gangdong/godeok-station-chuljangmassage/"),
        ("상일동역", "/gangdong/sangildong-station-chuljangmassage/"),
        ("강일역", "/gangdong/gangil-station-chuljangmassage/"),
        ("둔촌동역", "/gangdong/dunchon-dong-station-chuljangmassage/"),
        ("암사역", "/gangdong/amsa-station-chuljangmassage/"),
        ("암사역사공원역", "/gangdong/amsa-history-park-station-chuljangmassage/"),
        ("강동구청역", "/gangdong/gangdong-gu-office-station-chuljangmassage/"),
    ]),
    ("생활권·거점", "/gangdong/areas/", [
        ("생활권 전체", "/gangdong/areas/"),
        ("천호 로데오거리", "/gangdong/cheonho-rodeo-area-chuljangmassage/"),
        ("고덕비즈밸리", "/gangdong/godeok-business-valley-chuljangmassage/"),
        ("암사 선사유적지 인근", "/gangdong/amsa-prehistoric-area-chuljangmassage/"),
        ("둔촌동 올림픽파크포레온", "/gangdong/dunchon-olympic-park-foreon-chuljangmassage/"),
        ("길동사거리 생활권", "/gangdong/gil-dong-area-chuljangmassage/"),
        ("명일동 주거권", "/gangdong/myeongil-area-chuljangmassage/"),
        ("상일·강일 생활권", "/gangdong/sangil-gangil-area-chuljangmassage/"),
        ("성내동·강동구청 생활권", "/gangdong/seongnae-gangdong-office-area-chuljangmassage/"),
    ]),
    ("예약안내", "/reservation/", [
        ("예약 방법", "/reservation/#how"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("방문 가능 장소", "/reservation/#place"),
        ("결제 안내", "/reservation/#payment"),
        ("변경·취소 안내", "/reservation/#change"),
        ("예약 전 체크사항", "/reservation/#check"),
    ]),
    ("이용안내", "/checklist/", [
        ("이용 전 확인사항", "/checklist/"),
        ("홈타이 이용 가이드", "/hometai-guide/"),
        ("처음 이용하시는 분", "/checklist/#first"),
        ("위생·안전 기준", "/checklist/#hygiene"),
        ("금지행위 안내", "/checklist/#prohibited"),
        ("운영자 소개", "/about/"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("개인정보처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
