import logging
from pathlib import Path

from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy.http import Response
from scrapy.loader import ItemLoader

from models.raw.kyouikujouhou import (
    RawKyouikujouhouSyllabus,
    RawKyouikujouhouTeacher,
    授業基本情報,
    授業詳細情報,
    教員情報,
    教員詳細情報,
)
from scraper.utils import (
    get_keys,
    post,
    pre,
    split,
)
from scraper.utils.kyouikujouhou import (
    BASE_XPATH_SYLLABUS_KEY,
    BASE_XPATH_SYLLABUS_VAL,
    BASE_XPATH_TEACHER_KEY,
    BASE_XPATH_TEACHER_VAL,
    LINK_PATTERN_3,
    LINK_PATTERN_4,
    LINK_PATTERN_5,
    get_link,
)


class KyouikujouhouSyllabusLoader(ItemLoader):
    identifier_in = Identity()
    identifier_out = TakeFirst()

    # --------------------------------------------------------------------------
    #   基本情報
    # --------------------------------------------------------------------------

    科目種別_in = MapCompose(pre, post)
    科目種別_out = TakeFirst()

    授業番号_in = MapCompose(pre, post)
    授業番号_out = TakeFirst()

    学期_in = MapCompose(pre, post)
    学期_out = TakeFirst()

    曜日_in = MapCompose(pre, split(","), post)
    曜日_out = TakeFirst()

    科目_in = MapCompose(pre, post)
    科目_out = TakeFirst()

    時限_in = MapCompose(pre, split(","), post)
    時限_out = TakeFirst()

    担当教員_in = MapCompose(pre, post)
    担当教員_out = TakeFirst()

    単位数_in = MapCompose(pre, post)
    単位数_out = TakeFirst()

    科目ナンバリング_2018年度以降入学生対象_in = MapCompose(pre, post)
    科目ナンバリング_2018年度以降入学生対象_out = TakeFirst()

    # --------------------------------------------------------------------------
    #   担当教員一覧
    # --------------------------------------------------------------------------

    担当教員一覧_in = MapCompose(pre, post)
    担当教員一覧_out = Identity()

    # --------------------------------------------------------------------------
    #   詳細情報
    # --------------------------------------------------------------------------

    授業方針_テーマ_in = MapCompose(pre, post)
    授業方針_テーマ_out = TakeFirst()

    習得できる知識_能力や授業の目的_到達目標_in = MapCompose(pre, post)
    習得できる知識_能力や授業の目的_到達目標_out = TakeFirst()

    授業計画_内容授業方法_in = MapCompose(pre, post)
    授業計画_内容授業方法_out = TakeFirst()

    授業外学習_in = MapCompose(pre, post)
    授業外学習_out = TakeFirst()

    テキスト_参考書等_in = MapCompose(pre, post)
    テキスト_参考書等_out = TakeFirst()

    成績評価方法_in = MapCompose(pre, post)
    成績評価方法_out = TakeFirst()

    質問受付方法_オフィスアワー等_in = MapCompose(pre, post)
    質問受付方法_オフィスアワー等_out = TakeFirst()

    特記事項_他の授業科目との関連性_in = MapCompose(pre, post)
    特記事項_他の授業科目との関連性_out = TakeFirst()

    備考_in = MapCompose(pre, post)
    備考_out = TakeFirst()


def load_syallabus(response: Response) -> RawKyouikujouhouSyllabus:
    loader = KyouikujouhouSyllabusLoader(
        item=RawKyouikujouhouSyllabus(), response=response
    )
    loader.add_value("identifier", Path(response.url).stem)

    for key in get_keys(response.xpath(BASE_XPATH_SYLLABUS_KEY).getall()):
        if key not in (授業基本情報 + 授業詳細情報 + ["教員", "所属"]):
            logging.critical(f"unknown syllabus property: {key} ({response.url})")

    length = len(response.xpath(BASE_XPATH_SYLLABUS_VAL))
    offset = length - len(授業詳細情報)

    # 授業基本情報
    for i, field in enumerate(授業基本情報, 1):
        xpath = f"({BASE_XPATH_SYLLABUS_VAL})[{i}]"
        loader.add_xpath(field, xpath)

    # 担当教員一覧
    for i in reversed(range(offset - 1, len(授業基本情報), -2)):
        xpath = f"({BASE_XPATH_SYLLABUS_VAL})[{i}]"
        loader.add_xpath("担当教員一覧", xpath)

    # 授業詳細情報
    for i, field in enumerate(授業詳細情報, offset + 1):
        xpath = f"({BASE_XPATH_SYLLABUS_VAL})[{i}]"
        loader.add_xpath(field, xpath)

    return loader.load_item()


class KyouikujouhouTeacherLoader(ItemLoader):
    identifier_in = Identity()
    identifier_out = TakeFirst()

    # --------------------------------------------------------------------------
    # 教員情報
    # --------------------------------------------------------------------------

    教員名_in = MapCompose(pre, post)
    教員名_out = TakeFirst()

    教員名カナ_in = MapCompose(pre, post)
    教員名カナ_out = TakeFirst()

    英字_in = MapCompose(pre, post)
    英字_out = TakeFirst()

    所属_in = MapCompose(pre, post)
    所属_out = Identity()

    # --------------------------------------------------------------------------
    # 詳細情報
    # --------------------------------------------------------------------------

    学部_コース等_in = MapCompose(pre, post)
    学部_コース等_out = TakeFirst()

    研究科_専攻等_in = MapCompose(pre, post)
    研究科_専攻等_out = TakeFirst()

    職位_in = MapCompose(pre, post)
    職位_out = TakeFirst()

    専攻分野_in = MapCompose(pre, post)
    専攻分野_out = TakeFirst()

    最終学歴_学位_in = MapCompose(pre, post)
    最終学歴_学位_out = TakeFirst()

    研究テーマ_in = MapCompose(pre, post)
    研究テーマ_out = TakeFirst()

    研究キーワード_in = MapCompose(pre, post)
    研究キーワード_out = TakeFirst()

    研究業績_著者_論文_その他それに準じる業績_in = MapCompose(pre, post)
    研究業績_著者_論文_その他それに準じる業績_out = TakeFirst()

    受賞_in = MapCompose(pre, post)
    受賞_out = TakeFirst()

    主な学会活動_in = MapCompose(pre, post)
    主な学会活動_out = TakeFirst()

    社会等との関わり_in = MapCompose(pre, post)
    社会等との関わり_out = TakeFirst()

    個人のURL_in = MapCompose(pre, post)
    個人のURL_out = TakeFirst()

    担当科目_in = MapCompose(pre, post)
    担当科目_out = TakeFirst()

    オフィスアワー_in = MapCompose(pre, post)
    オフィスアワー_out = TakeFirst()

    研究室_in = MapCompose(pre, post)
    研究室_out = TakeFirst()

    内線番号_in = MapCompose(pre, post)
    内線番号_out = TakeFirst()

    メールアドレス_in = MapCompose(pre, post)
    メールアドレス_out = TakeFirst()

    研究室サイト等_in = MapCompose(pre, post)
    研究室サイト等_out = TakeFirst()

    取組状況_in = MapCompose(get_link(LINK_PATTERN_3))
    取組状況_out = TakeFirst()

    researchmap_in = MapCompose(get_link(LINK_PATTERN_4))
    researchmap_out = TakeFirst()

    取組成果_in = MapCompose(get_link(LINK_PATTERN_5))
    取組成果_out = TakeFirst()


def load_teacher(response: Response) -> RawKyouikujouhouTeacher:
    loader = KyouikujouhouTeacherLoader(
        item=RawKyouikujouhouTeacher(), response=response
    )
    loader.add_value("identifier", Path(response.url).stem)

    keys = get_keys(response.xpath(BASE_XPATH_TEACHER_KEY).getall())
    vals = response.xpath(BASE_XPATH_TEACHER_VAL)

    if len(keys) != len(vals):
        logging.critical(
            f"length of keys ({len(keys)}) does not match length of values ({len(vals)})"
        )

    for i, key in enumerate(keys, 1):
        xpath = f"({BASE_XPATH_TEACHER_VAL})[{i}]"
        if key in ["取組状況", "researchmap", "取組成果"]:  # TODO: improve code
            xpath += "/a/@onclick"

        if key in (教員情報 + 教員詳細情報):
            loader.add_xpath(key, xpath)
        else:
            logging.critical(f"unknown teacher property: {key} ({response.url})")

    return loader.load_item()
