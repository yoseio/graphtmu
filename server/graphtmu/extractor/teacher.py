from typing import List, Optional

from graphtmu.extractor.llm import get_keywords
from graphtmu.models.teacher import ContactPoint, DefinedTerm, Organization, Teacher
from graphtmu.models.tmu import RawTmuTeacher


class TeacherExtractor:
    @classmethod
    def extract(cls, raw: RawTmuTeacher) -> Teacher:
        return Teacher(
            affiliation=cls._affiliation(raw),
            alternateName=cls._alternateName(raw),
            description=cls._description(raw),
            email=cls._email(raw),
            identifier=cls._identifier(raw),
            jobTitle=cls._jobTitle(raw),
            knowsAbout=cls._knowsAbout(raw),
            name=cls._name(raw),
            workLocation=cls._workLocation(raw),
        )

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
    def _identifier(cls, raw: RawTmuTeacher) -> str:
        return str(raw.identifier)

    @classmethod
    def _jobTitle(cls, raw: RawTmuTeacher) -> Optional[DefinedTerm]:
        if raw.職位 is None:
            return None
        return DefinedTerm(identifier=raw.職位, name=raw.職位)

    @classmethod
    def _knowsAbout(cls, raw: RawTmuTeacher) -> List[str]:
        text = "\n".join([str(raw.専門_研究分野), str(raw.研究キーワード)])
        return get_keywords(text).keywords

    @classmethod
    def _name(cls, raw: RawTmuTeacher) -> str:
        return str(raw.教員名)

    @classmethod
    def _workLocation(cls, raw: RawTmuTeacher) -> Optional[ContactPoint]:
        if raw.研究室 is None:
            return None
        return ContactPoint(
            areaServed=raw.研究室, identifier=raw.研究室, telephone=raw.内線番号
        )


if __name__ == "__main__":
    from dataclasses import asdict

    from dotenv import load_dotenv
    from pandas import DataFrame
    from pydantic import RootModel

    load_dotenv()

    with open("data/raw/tmu/teacher.jsonl", mode="r") as f:
        df = DataFrame([
            asdict(
                TeacherExtractor.extract(
                    RootModel[RawTmuTeacher].model_validate_json(line).root
                )
            )
            for line in f.readlines()
        ])

    df.to_json("data/teacher.jsonl", orient="records", force_ascii=False, lines=True)
