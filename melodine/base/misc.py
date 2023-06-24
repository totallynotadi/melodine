from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResultsBase:
    """Base class for representing search results from a source."""

    def __add__(self, other: "SearchResultsBase"):
        self_items = self.__dict__.items()
        for attr, val in other.__dict__.items():
            if attr not in self_items:
                self.__setattr__(attr, val)
            else:
                self.__setattr__(attr, self.__getattribute__(attr).extend(val))
        return self

    def __bool__(self):
        return any(self.__dict__.values())

    def __repr__(self) -> str:
        return f"<melo.SearchResults: {id(self)}>"


class URIBase:
    """
    Base class for generic dataclass dunder methods defined for objects with a `uri` attribute.

    All melodine.must inherit from `URIBase`
    """

    uri = repr(None)
    id = repr(None)

    def __hash__(self):
        return hash(self.uri)

    def __eq__(self, __o: object) -> bool:
        return type(self) is type(__o) and self.uri == __o.uri  # type: ignore

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __bool__(self):
        return not not self.id

    def __str__(self) -> str:
        return self.uri
