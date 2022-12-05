from dataclasses import dataclass
import functools


class Image:
    """
    An object representing a Spotify image resource.

    Attributes
    ----------
    height : :class:`str`
        The height of the image.
    width : :class:`str`
        The width of the image.
    url : :class:`str`
        The URL of the image.
    """

    __slots__ = ("height", "width", "url")

    def __init__(self, *, height: str, width: str, url: str):
        self.height = height
        self.width = width
        self.url = url

    def __repr__(self):
        return f"<melo.Image: {self.url!r} (width: {self.width!r}, height: {self.height!r})>"

    def __eq__(self, other):
        return type(self) is type(other) and self.url == other.url


@dataclass
class SearchResults:
    """ A base dataclass of the YTMusicSearchResults and SpotifySearchResults classes. """

    def __add__(self, other: "SearchResults"):
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
    '''
    A base class to define basic dunder methods for all URI baed methods. It's purpose is to reduce boiler plate for models

    All melo models must inherit from this class to have basic dunder methods
    '''

    uri = repr(None)
    id = repr(None)

    def __hash__(self):
        return hash(self.uri)

    def __eq__(self, __o: object) -> bool:
        return (
            type(self) is type(__o) and self.uri == __o.uri
        )

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __bool__(self):
        return not not self.id

    def __str__(self) -> str:
        return self.uri


def singleton(cls):
    '''class definitions marked singleton remember created instances and return that one same instance each time its object is instantialted.

    i.e. only one instance of an object can exist at any given time.'''
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton
