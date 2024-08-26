import itertools
from typing import List

from itemadapter.adapter import ItemAdapter
from toolz.curried import filter, map, pipe

from scraper.utils import replace, split, splitlines


class AffiliationsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("所属"):
            affiliations: List[str] = adapter.get("所属")  # type: ignore
            adapter["所属"] = pipe(
                affiliations,
                map(replace("東京都立大学", "")),
                map(splitlines),
                itertools.chain.from_iterable,
                filter(lambda x: x != ""),
                map(split(" ")),
                map(lambda x: ["東京都立大学"] + x),
                list,
            )

        return item
