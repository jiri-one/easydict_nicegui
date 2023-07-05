from abc import ABC, abstractmethod
from difflib import SequenceMatcher
from typing import Iterator, Callable
from dataclasses import dataclass, field
from bisect import insort
from operator import attrgetter


@dataclass
class Result:
    eng: str
    cze: str
    notes: str = None
    special: str = None
    author: str = None
    matchratio: float = None


@dataclass
class ResultList:
    word: str = None
    lang: str = None
    fulltext: bool = None
    on_change: Callable = None
    items: list[Result] = field(default_factory=list)

    def add(self, item: Result):
        insort(self.items, item, key=attrgetter("matchratio"))


class DBBackend(ABC):
    @abstractmethod
    def search_in_db(
        self, word, lang, fulltext: bool = None
    ) -> Iterator[Result] | None:
        """The only mandatory method that provides a database search and that must return a result iterator of Results or None."""

    def search_sorted(self, word, lang, fulltext: bool = None) -> ResultList | None:
        results_from_db = self.search_in_db(word, lang, fulltext)
        if not results_from_db:
            return None
        results = ResultList(word, lang, fulltext)
        for result in results_from_db:
            result.matchratio = SequenceMatcher(
                None, getattr(result, lang), word
            ).ratio()
            results.add(result)
        return results
