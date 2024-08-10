from abc import ABCMeta, abstractmethod


class ArtistBase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_id(cls, resource_id: str): ...

    @classmethod
    @abstractmethod
    def from_url(cls, url: str): ...

    @property
    @abstractmethod
    def id(self): ...

    @property
    @abstractmethod
    def name(self): ...

    @property
    @abstractmethod
    def href(self): ...

    @property
    @abstractmethod
    def uri(self): ...

    # TODO: decide wether this property must be in every model
    # @property
    # @abstractmethod
    # def thumbnails(self): ...

    # TODO: decide wether this property must be in every model
    # @property
    # @abstractmethod
    # def followers(self): ...

    @property
    @abstractmethod
    def albums(self): ...

    @property
    @abstractmethod
    def tracks(self): ...

    @property
    @abstractmethod
    def related_artists(self): ...
