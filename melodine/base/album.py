from abc import ABCMeta, abstractmethod


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
    def from_id(cls, id: str):
        ...

    @classmethod
    @abstractmethod
    def from_url(cls, url: str):
        ...

    @property
    @abstractmethod
    def id(self):
        ...

    @property
    @abstractmethod
    def name(self):
        ...

    @property
    @abstractmethod
    def href(self):
        ...

    @property
    @abstractmethod
    def uri(self):
        ...

    @property
    @abstractmethod
    def type(self):
        ...

    # @property
    # @abstractmethod
    # def year(self):
    #     ...

    # @property
    # @abstractmethod
    # def total_tracks(self):
    #     ...

    @property
    @abstractmethod
    def artist(self):
        ...

    @property
    @abstractmethod
    def tracks(self):
        ...


# class Test(AlbumBase):
#     def __init__(self) -> None:
#         super().__init__()
#         pass

#     def id(self):
#         pass

#     def artist(self):
#         pass

#     def href(self):
#         pass

#     def name(self):
#         pass

#     def tracks(self):
#         pass

#     def type(self):
#         pass

#     def uri(self):
#         pass


# test = Test()
