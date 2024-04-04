from abc import ABCMeta, abstractmethod, abstractproperty


class AlbumBase(metaclass=ABCMeta):
    # @classmethod
    # def __subclasshook__(cls, subclass):
    #     return (
    #         hasattr(subclass, 'id') and
    #         hasattr(subclass, 'name') and
    #         hasattr(subclass, 'href') and
    #         hasattr(subclass, 'uri') and
    #         hasattr(subclass, 'duration') and
    #         not hasattr(subclass, 'explicit') and
    #         hasattr(subclass, 'images') and

    #         hasattr(subclass, 'artists') and
    #         hasattr(subclass, 'url') and

    #         hasattr(subclass, 'get_recommendations') and callable(
    #             subclass.get_recommendations)
    #     )

    @classmethod
    @abstractmethod
    def from_id(cls, resource_id: str): ...

    @classmethod
    @abstractmethod
    def from_url(cls, url: str): ...

    @property
    @abstractproperty
    def id(self) -> str: ...

    @property
    @abstractproperty
    def name(self): ...

    @property
    @abstractproperty
    def href(self): ...

    @property
    @abstractproperty
    def uri(self): ...

    @property
    @abstractproperty
    def type(self): ...

    # @property
    # @abstractproperty
    # def year(self):
    #     ...

    # @property
    # @abstractproperty
    # def total_tracks(self):
    #     ...

    @property
    @abstractproperty
    def artists(self): ...

    @property
    @abstractproperty
    def tracks(self): ...


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
    def artists(self):
        pass

    @classmethod
    def from_id(self):
        pass

    @classmethod
    def from_url(self):
        pass


test = Test()
