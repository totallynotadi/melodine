from abc import ABCMeta, abstractmethod

from typing_extensions import Self


class AlbumBase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_id(cls, resource_id: str) -> Self:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_url(cls, url: str):
        raise NotImplementedError()

    @property
    @abstractmethod
    def id(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def href(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def uri(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def type(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def year(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def total_tracks(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def artists(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def tracks(self):
        raise NotImplementedError()


class Test(AlbumBase):
    def __init__(self) -> None:
        super().__init__()
        pass

    @property
    def id(self):
        pass

    @property
    def artist(self):
        pass

    @property
    def href(self):
        pass

    @property
    def name(self):
        pass

    @property
    def tracks(self):
        pass

    @property
    def type(self):
        pass

    @property
    def uri(self):
        pass

    @property
    def total_tracks(self):
        pass

    @property
    def year(self):
        pass

    @property
    def artists(self):
        pass

    @classmethod
    def from_id(self):
        pass

    @classmethod
    def from_url(self):
        pass


test = Test()
