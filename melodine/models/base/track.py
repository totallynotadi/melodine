from abc import ABCMeta


class TrackBase(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'id') and
            hasattr(subclass, 'name') and
            hasattr(subclass, 'href') and
            hasattr(subclass, 'uri') and
            hasattr(subclass, 'explicit') and
            hasattr(subclass, 'duration') and
            hasattr(subclass, 'images') and

            hasattr(subclass, 'artists') and
            hasattr(subclass, 'album') and
            hasattr(subclass, 'url') and

            hasattr(subclass, 'get_recommendations') and callable(
                subclass.get_recommendations)
        )

    # @property
    # @abstractmethod
    # def id(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def name(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def href(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def uri(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def explicit(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def duration(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def images(self):
    #     raise NotImplementedError

    # # @classmethod
    # # @abstractmethod
    # # def from_id(cls, id: str) -> "TrackBase":
    # #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def artists(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def album(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def url(self):
    #     raise NotImplementedError

    # @abstractmethod
    # def get_recommendations(self):
    #     raise NotImplementedError
