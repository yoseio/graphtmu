from dataclasses import field
from typing import List, Optional, Self

from pydantic import RootModel
from pydantic.dataclasses import dataclass


@dataclass
class RawKyouikujouhouSyllabus:
    """Syllabus data scraped from kyouikujouhou.eas.tmu.ac.jp

    http://www.kyouikujouhou.eas.tmu.ac.jp/syllabus/flame.html
    """

    identifier: Optional[str] = field(default=None)

    # 基本情報
    科目種別: Optional[str] = field(default=None)
    授業番号: Optional[str] = field(default=None)
    学期: Optional[str] = field(default=None)
    曜日: Optional[str] = field(default=None)
    科目: Optional[str] = field(default=None)
    時限: Optional[str] = field(default=None)
    担当教員: Optional[str] = field(default=None)
    単位数: Optional[str] = field(default=None)
    科目ナンバリング_2018年度以降入学生対象: Optional[str] = field(default=None)

    # 担当教員一覧
    担当教員一覧: Optional[List[str]] = field(default=None)

    # 詳細情報
    授業方針_テーマ: Optional[str] = field(default=None)
    習得できる知識_能力や授業の目的_到達目標: Optional[str] = field(default=None)
    授業計画_内容授業方法: Optional[str] = field(default=None)
    授業外学習: Optional[str] = field(default=None)
    テキスト_参考書等: Optional[str] = field(default=None)
    成績評価方法: Optional[str] = field(default=None)
    質問受付方法_オフィスアワー等: Optional[str] = field(default=None)
    特記事項_他の授業科目との関連性: Optional[str] = field(default=None)
    備考: Optional[str] = field(default=None)

    @classmethod
    def loads(cls, data: str | bytes | bytearray) -> Self:
        return RootModel[Self].model_validate_json(data).root


授業基本情報 = [
    "科目種別",
    "授業番号",
    "学期",
    "曜日",
    "科目",
    "時限",
    "担当教員",
    "単位数",
    "科目ナンバリング_2018年度以降入学生対象",
]

授業詳細情報 = [
    "授業方針_テーマ",
    "習得できる知識_能力や授業の目的_到達目標",
    "授業計画_内容授業方法",
    "授業外学習",
    "テキスト_参考書等",
    "成績評価方法",
    "質問受付方法_オフィスアワー等",
    "特記事項_他の授業科目との関連性",
    "備考",
]


@dataclass
class RawKyouikujouhouTeacher:
    """Teacher data scraped from kyouikujouhou.eas.tmu.ac.jp

    http://www.kyouikujouhou.eas.tmu.ac.jp/teacherprofile/flame.html
    """

    identifier: Optional[str] = field(default=None)

    # 教員情報
    教員名: Optional[str] = field(default=None)
    教員名カナ: Optional[str] = field(default=None)
    英字: Optional[str] = field(default=None)
    所属: Optional[str] = field(default=None)

    # 詳細情報
    学部_コース等: Optional[str] = field(default=None)
    研究科_専攻等: Optional[str] = field(default=None)
    職位: Optional[str] = field(default=None)
    専攻分野: Optional[str] = field(default=None)
    最終学歴_学位: Optional[str] = field(default=None)
    研究テーマ: Optional[str] = field(default=None)
    研究キーワード: Optional[str] = field(default=None)
    研究業績_著者_論文_その他それに準じる業績: Optional[str] = field(default=None)
    受賞: Optional[str] = field(default=None)
    主な学会活動: Optional[str] = field(default=None)
    社会等との関わり: Optional[str] = field(default=None)
    個人のURL: Optional[str] = field(default=None)
    担当科目: Optional[str] = field(default=None)
    オフィスアワー: Optional[str] = field(default=None)
    研究室: Optional[str] = field(default=None)
    内線番号: Optional[str] = field(default=None)
    メールアドレス: Optional[str] = field(default=None)
    研究室サイト等: Optional[str] = field(default=None)
    取組状況: Optional[str] = field(default=None)
    researchmap: Optional[str] = field(default=None)
    取組成果: Optional[str] = field(default=None)

    @classmethod
    def loads(cls, data: str | bytes | bytearray) -> Self:
        return RootModel[Self].model_validate_json(data).root


教員情報 = [
    "教員名",
    "教員名カナ",
    "英字",
    "所属",
]

教員詳細情報 = [
    "学部_コース等",  # hidden
    "研究科_専攻等",  # hidden
    "職位",
    "専攻分野",
    "最終学歴_学位",
    "研究テーマ",
    "研究キーワード",
    "研究業績_著者_論文_その他それに準じる業績",
    "受賞",
    "主な学会活動",
    "社会等との関わり",
    "個人のURL",
    "担当科目",
    "オフィスアワー",
    "研究室",
    "内線番号",
    "メールアドレス",
    "研究室サイト等",
    "取組状況",
    "researchmap",
    "取組成果",
]
