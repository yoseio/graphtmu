from typing import List

from scrapy import Spider
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor

from graphtmu.scraper.loaders.tmu import load_teacher

START_URLS = ["https://www.tmu.ac.jp/stafflist.html"]


class TmuSpider(Spider):
    name = "tmu"
    start_urls = START_URLS

    def parse(self, response: Response, **kwargs):
        links = self._get_teacher_links(response)
        yield from response.follow_all(links, self._parse_teacher)

    def _get_teacher_links(self, response: Response) -> List[str]:
        extractor = LinkExtractor(restrict_xpaths=['id("researcherList")/div/a'])
        return list(map(lambda x: x.url, extractor.extract_links(response)))

    def _parse_teacher(self, response: Response):
        yield load_teacher(response)
