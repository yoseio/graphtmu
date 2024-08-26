from typing import List

from scrapy import Spider
from scrapy.http import Response

from scraper.loaders.kyouikujouhou import (
    get_link,
    load_syallabus,
    load_teacher,
)
from scraper.utils.kyouikujouhou import (
    LINK_PATTERN_1,
    LINK_PATTERN_2,
    START_URLS,
)


class KyouikujouhouSpider(Spider):
    name = "kyouikujouhou"
    start_urls = START_URLS

    def parse(self, response: Response, **kwargs):
        """
        @url http://www.kyouikujouhou.eas.tmu.ac.jp/syllabus/2024/YobiIchiran_0_1.html
        @returns items 0 0
        @returns requests 2927 2927
        """
        links = self._get_syllabus_links(response)
        yield from response.follow_all(links, self._parse_syllabus)

        links = self._get_teacher_links(response)
        yield from response.follow_all(links, self._parse_teacher)

    def _get_syllabus_links(self, response: Response) -> List[str]:
        targets = response.css("a").xpath("@onclick").getall()
        return list(filter(None, map(get_link(LINK_PATTERN_1), targets)))

    def _get_teacher_links(self, response: Response) -> List[str]:
        targets = response.css("a").xpath("@onclick").getall()
        return list(filter(None, map(get_link(LINK_PATTERN_2), targets)))

    def _parse_syllabus(self, response: Response):
        """
        @url http://www.kyouikujouhou.eas.tmu.ac.jp/syllabus/2024/A/2/2024_A4_I0075.html
        @returns items 1 1
        @returns requests 0 0
        """
        yield load_syallabus(response)

    def _parse_teacher(self, response: Response):
        """
        @url http://www.kyouikujouhou.eas.tmu.ac.jp/teacherprofile/D/D404_00482.html
        @returns items 1 1
        @returns requests 0 0
        """
        yield load_teacher(response)
