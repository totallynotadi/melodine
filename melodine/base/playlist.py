from abc import ABCMeta


class PlaylistBase(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'id') and
            hasattr(subclass, 'name') and
            hasattr(subclass, 'href') and
            hasattr(subclass, 'uri') and
            hasattr(subclass, 'owner') and
            hasattr(subclass, 'description') and
            hasattr(subclass, 'images') and

            hasattr(subclass, 'total_tracks') and
            hasattr(subclass, 'tracks')
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
    # def owner(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def description(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def total_tracks(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def tracks(self):
    #     raise NotImplementedError
