from os import path
from typing import Optional

from w3lib._types import StrOrBytes
from w3lib.util import to_unicode

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

BASE_XPATH_TEACHER_KEY = '//td[@class="teacherprofile-head"]'
BASE_XPATH_TEACHER_VAL = '//td[@class="teacherprofile-normal"]'

BASE_XPATH_SYLLABUS_KEY = '//td[@class="syllabus-head"]'
BASE_XPATH_SYLLABUS_VAL = '//td[@class="syllabus-normal"]'

LINK_PATTERN_0 = "');"
LINK_PATTERN_1 = "return OpenInfo('"
LINK_PATTERN_2 = "return OpenInfoKyopro('"
LINK_PATTERN_3 = "return OpenInfoKyoproTJ('"
LINK_PATTERN_4 = "return OpenInfoKyoproRM('"
LINK_PATTERN_5 = "return OpenInfoKyoproTS('"


def get_link(pattern: str):
    def _get_link(text: StrOrBytes) -> Optional[str]:
        text = to_unicode(text)
        if text.startswith(pattern):
            return text[len(pattern) : -len(LINK_PATTERN_0)]
        return None

    return _get_link
