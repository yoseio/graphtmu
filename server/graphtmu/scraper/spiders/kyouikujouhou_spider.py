from os import path
from typing import List

from scrapy import Spider
from scrapy.http import Response

from graphtmu.scraper.loaders.kyouikujouhou import (
    LINK_PATTERN_1,
    LINK_PATTERN_2,
    get_link,
    load_syallabus,
    load_teacher,
)

BASE_URL = "http://www.kyouikujouhou.eas.tmu.ac.jp/"
START_URLS = [
    # シラバス
    path.join(BASE_URL, "syllabus/2024/YobiIchiran_0_1.html"),
    path.join(BASE_URL, "syllabus/2024/YobiIchiran_0_2.html"),
    path.join(BASE_URL, "syllabus/2024/YobiIchiran_0_3.html"),
    path.join(BASE_URL, "syllabus/2024/YobiIchiran_0_4.html"),
    path.join(BASE_URL, "syllabus/2024/YobiIchiran_0_5.html"),
    path.join(BASE_URL, "syllabus/2024/YobiIchiran_0_9.html"),
    # 教員
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_A.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_KA.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_SA.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_TA.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_NA.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_HA.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_MA.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_YA.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_RA.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_WA.html"),
    path.join(BASE_URL, "teacherprofile/KyoinIchiran_0_ELSE.html"),
]


class KyouikujouhouSpider(Spider):
    name = "kyouikujouhou"
    start_urls = START_URLS

    def parse(self, response: Response, **kwargs):
        links = self._get_syllabus_links(response)
        yield from response.follow_all(links, self._parse_syllabus)

        links = self._get_teacher_links(response)
        yield from response.follow_all(links, self._parse_teacher)

    def _get_syllabus_links(self, response: Response) -> List[str]:
        targets = response.css("a").xpath("@onclick").getall()
        return list(filter(None, map(get_link(LINK_PATTERN_1), targets)))

    def _parse_syllabus(self, response: Response):
        yield load_syallabus(response)

    def _get_teacher_links(self, response: Response) -> List[str]:
        targets = response.css("a").xpath("@onclick").getall()
        return list(filter(None, map(get_link(LINK_PATTERN_2), targets)))

    def _parse_teacher(self, response: Response):
        yield load_teacher(response)
