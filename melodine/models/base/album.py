from abc import ABCMeta


class AlbumBase(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'id') and
            hasattr(subclass, 'name') and
            hasattr(subclass, 'href') and
            hasattr(subclass, 'uri') and
            hasattr(subclass, 'duration') and
            not hasattr(subclass, 'explicit') and
            hasattr(subclass, 'images') and

            hasattr(subclass, 'artists') and
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
    # def type(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def year(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def total_tracks(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def tracks(self):
    #     raise NotImplementedError
