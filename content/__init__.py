# 전체 페이지 목록 집계
from . import main, areas, stations, districts, info, about

PAGES = (
    [main.PAGE]
    + areas.PAGES
    + stations.PAGES
    + districts.PAGES
    + info.PAGES
    + [about.PAGE]
)
