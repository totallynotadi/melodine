from abc import ABCMeta, abstractmethod

from typing_extensions import Self


class TrackBase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_id(cls, id: str) -> Self:
        raise NotImplementedError()

    @property
    @abstractmethod
    def id(self):
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
    def explicit(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def duration(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def images(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def artists(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def album(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def url(self):
        raise NotImplementedError()

    @abstractmethod
    def get_recommendations(self):
        raise NotImplementedError()
