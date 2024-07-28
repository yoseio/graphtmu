import re
import unicodedata
from typing import List, Optional

from toolz import curry
from w3lib._types import StrOrBytes
from w3lib.html import remove_tags, replace_tags
from w3lib.util import to_unicode

# ------------------------------------------------------------------------------
#   cat.1
# ------------------------------------------------------------------------------


def strip(text: StrOrBytes) -> str:
    return to_unicode(text).strip()


@curry
def split(sep: str, text: StrOrBytes) -> List[str]:
    return to_unicode(text).split(sep=sep)


@curry
def resplit(sep: str, text: StrOrBytes) -> List[str]:
    return re.split(sep, to_unicode(text))


def splitlines(text: StrOrBytes) -> List[str]:
    return to_unicode(text).splitlines()


def normalize(text: StrOrBytes) -> str:
    return unicodedata.normalize("NFKC", to_unicode(text))


def punctuation(text: StrOrBytes) -> bool:
    return unicodedata.category(to_unicode(text)).startswith("P")


def br(text: StrOrBytes) -> str:
    return replace_tags(remove_tags(text, keep=("br",)), "\n")


# ------------------------------------------------------------------------------
#   cat.2
# ------------------------------------------------------------------------------


def pre(text: StrOrBytes) -> str:
    return normalize(br(text))


def post(text: StrOrBytes) -> str:
    return strip(text)


# ------------------------------------------------------------------------------
#   cat.3
# ------------------------------------------------------------------------------


def identifier(text: StrOrBytes) -> Optional[str]:
    text = "".join(["_" if punctuation(c) else c for c in pre(text)])
    if text == "" or text is None or not text.isidentifier():
        return None
    return text


def get_keys(texts: List[StrOrBytes]) -> List[str]:
    return list(filter(None, map(identifier, texts)))
