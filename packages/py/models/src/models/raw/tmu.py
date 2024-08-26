from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class RawTmuTeacher:
    """Teacher data scraped from tmu.ac.jp

    https://www.tmu.ac.jp/stafflist.html
    """

    identifier: Optional[str] = field(default=None)

    教員名: Optional[str] = field(default=None)
    教員名カナ: Optional[str] = field(default=None)
    英字: Optional[str] = field(default=None)
    職位: Optional[str] = field(default=None)
    顔写真: Optional[str] = field(default=None)

    # 教員情報
    所属: Optional[List[List[str]]] = field(default=None)
    最終学歴_学位: Optional[str] = field(default=None)
    専門_研究分野: Optional[str] = field(default=None)
    研究テーマ: Optional[str] = field(default=None)
    研究キーワード: Optional[str] = field(default=None)
    研究イメージ: Optional[str] = field(default=None)
    研究紹介: Optional[str] = field(default=None)
    研究室: Optional[str] = field(default=None)
    オフィスアワー: Optional[str] = field(default=None)
    内線番号: Optional[str] = field(default=None)
    メールアドレス: Optional[str] = field(default=None)

    # 担当科目: Optional[str] = field(default=None)
    # 取組状況: Optional[str] = field(default=None)
    # Researchmap: Optional[str] = field(default=None)


教員情報 = [
    "所属",
    "最終学歴_学位",
    "専門_研究分野",
    "研究テーマ",
    "研究キーワード",
    "研究イメージ",
    "研究紹介",
    "研究室",
    "オフィスアワー",
    "内線番号",
    "メールアドレス",
]

教員詳細情報 = [
    "担当科目",
    "取組状況",
    "Researchmap",
]
