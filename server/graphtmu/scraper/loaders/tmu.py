import logging
from pathlib import Path

from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy.http import Response
from scrapy.loader import ItemLoader

from graphtmu.models.raw.tmu import RawTmuTeacher, 教員情報
from graphtmu.scraper.utils import identifier, post, pre, splitlines
from graphtmu.scraper.utils.tmu import XPATH_TEACHER_PROFILE


class TmuTeacherLoader(ItemLoader):
    identifier_in = Identity()
    identifier_out = TakeFirst()

    教員名_in = MapCompose(pre, splitlines, post)
    教員名_out = TakeFirst()

    教員名カナ_in = MapCompose(pre, post)
    教員名カナ_out = TakeFirst()

    英字_in = MapCompose(pre, post)
    英字_out = TakeFirst()

    職位_in = MapCompose(pre, post)
    職位_out = TakeFirst()

    顔写真_in = MapCompose(pre, post)
    顔写真_out = TakeFirst()

    # --------------------------------------------------------------------------
    # 教員情報
    # --------------------------------------------------------------------------

    所属_in = MapCompose(pre, post)
    所属_out = Identity()

    最終学歴_学位_in = MapCompose(pre, post)
    最終学歴_学位_out = TakeFirst()

    専門_研究分野_in = MapCompose(pre, post)
    専門_研究分野_out = TakeFirst()

    研究テーマ_in = MapCompose(pre, post)
    研究テーマ_out = TakeFirst()

    研究キーワード_in = MapCompose(pre, post)
    研究キーワード_out = TakeFirst()

    研究イメージ_in = MapCompose(pre, post)
    研究イメージ_out = TakeFirst()

    研究紹介_in = MapCompose(pre, post)
    研究紹介_out = TakeFirst()

    研究室_in = MapCompose(pre, post)
    研究室_out = TakeFirst()

    オフィスアワー_in = MapCompose(pre, post)
    オフィスアワー_out = TakeFirst()

    内線番号_in = MapCompose(pre, post)
    内線番号_out = TakeFirst()

    メールアドレス_in = MapCompose(pre, post)
    メールアドレス_out = TakeFirst()

    # --------------------------------------------------------------------------
    # 教員詳細情報
    # --------------------------------------------------------------------------


def load_teacher(response: Response) -> RawTmuTeacher:
    loader = TmuTeacherLoader(item=RawTmuTeacher(), response=response)
    loader.add_value("identifier", Path(response.url).stem)

    loader.add_xpath("教員名", 'id("researcherHeader")/h3[@class="name"]')
    loader.add_xpath("教員名カナ", 'id("researcherHeader")//span[@class="kana"]')
    loader.add_xpath("英字", 'id("researcherHeader")/div[@class="bgName en-pt"]')
    loader.add_xpath("職位", 'id("researcherHeader")/div[@class="position"]')
    # loader.add_value(
    #     "顔写真", f"assets/cache/images/researcher/face/{identifier}_face.jpg"
    # )

    # 教員情報
    for prop in response.xpath(XPATH_TEACHER_PROFILE):  # type: ignore
        key = identifier(prop.xpath("h5").get())  # type: ignore
        if key in ["研究イメージ"]:
            val = prop.xpath("*/img/@src").get()
            loader.add_value(key, val)
        if key in 教員情報:
            val = prop.xpath('descendant-or-self::p[@class="text"]').get()
            loader.add_value(key, val)
        else:
            logging.critical(f"unknown teacher property: {key} ({response.url})")

    # 教員詳細情報
    # keys = get_keys(response, XPATH_TEACHER_DETAIL_KEY)
    # vals = response.xpath(XPATH_TEACHER_DETAIL_VAL)
    # if len(keys) != len(vals):
    #     logging.critical(
    #         f"length of keys ({len(keys)}) does not match length of values ({len(vals)})"
    #     )
    # for i, key in enumerate(keys, 1):
    #     xpath = f"({XPATH_TEACHER_DETAIL_VAL})[{i}]"
    #     if key in ["取組状況", "Researchmap"]:  # TODO: improve code
    #         xpath += "/a/@onclick"
    #     if key in 教員詳細情報:
    #         loader.add_xpath(key, xpath)
    #     else:
    #         logging.critical(f"unknown teacher property: {key} ({response.url})")

    return loader.load_item()
