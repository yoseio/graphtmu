from dataclasses import asdict
from os import path
from typing import List, Optional

from dotenv import load_dotenv
from pandas import DataFrame
from pydantic import RootModel
from tqdm import tqdm

from graphtmu.extractor.llm import get_keywords
from graphtmu.models.teacher import (
    ContactPoint,
    DefinedTerm,
    Organization,
    Teacher,
    Thing,
)
from graphtmu.models.tmu import RawTmuTeacher
from graphtmu.utils.constants import DATA_PATH


class TeacherExtractor:
    @classmethod
    def extract(cls, raw: RawTmuTeacher) -> Teacher:
        return Teacher(
            identifier=cls._identifier(raw),
            name=cls._name(raw),
            affiliation=cls._affiliation(raw),
            alternateName=cls._alternateName(raw),
            description=cls._description(raw),
            email=cls._email(raw),
            jobTitle=cls._jobTitle(raw),
            knowsAbout=cls._knowsAbout(raw),
            workLocation=cls._workLocation(raw),
        )

    @classmethod
    def _identifier(cls, raw: RawTmuTeacher) -> str:
        return str(raw.identifier)

    @classmethod
    def _name(cls, raw: RawTmuTeacher) -> str:
        return str(raw.教員名)

    @classmethod
    def _affiliation(cls, raw: RawTmuTeacher) -> List[Organization]:
        def _affiliation_internal(data: List[str]) -> Optional[Organization]:
            if data == []:
                return None
            return Organization(
                identifier="_".join(data),
                name=data[-1],
                parentOrganization=_affiliation_internal(data[:-1]),
            )

        if raw.所属 is None:
            return []
        return list(filter(None, map(_affiliation_internal, raw.所属)))

    @classmethod
    def _alternateName(cls, raw: RawTmuTeacher) -> List[str]:
        return list(map(str, filter(None, [raw.教員名カナ, raw.英字])))

    @classmethod
    def _description(cls, raw: RawTmuTeacher) -> str:
        return str(raw.研究テーマ)

    @classmethod
    def _email(cls, raw: RawTmuTeacher) -> str:
        return str(raw.メールアドレス)

    @classmethod
    def _jobTitle(cls, raw: RawTmuTeacher) -> Optional[DefinedTerm]:
        if raw.職位 is None:
            return None
        return DefinedTerm(identifier=raw.職位, name=raw.職位)

    @classmethod
    def _knowsAbout(cls, raw: RawTmuTeacher) -> List[Thing]:
        text = "\n".join([
            str(raw.専門_研究分野),
            str(raw.研究テーマ),
            str(raw.研究キーワード),
        ])
        keywords = get_keywords(text).keywords
        return [Thing(identifier=keyword, name=keyword) for keyword in keywords]

    @classmethod
    def _workLocation(cls, raw: RawTmuTeacher) -> Optional[ContactPoint]:
        if raw.研究室 is None:
            return None
        return ContactPoint(
            identifier=raw.研究室,
            areaServed=raw.研究室,
            telephone=raw.内線番号,
        )


if __name__ == "__main__":
    load_dotenv()

    with open(path.join(DATA_PATH, "./raw/tmu/teacher.jsonl"), mode="r") as f:
        teachers = []
        for line in tqdm(f.readlines()):
            teachers.append(
                TeacherExtractor.extract(
                    RootModel[RawTmuTeacher].model_validate_json(line).root
                )
            )

    df = DataFrame(map(asdict, teachers))
    df.to_json(
        path.join(DATA_PATH, "./teacher.jsonl"),
        orient="records",
        force_ascii=False,
        lines=True,
    )
