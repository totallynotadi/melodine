from abc import ABC, abstractmethod


class ArtistBase(ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'id') and
            hasattr(subclass, 'name') and
            hasattr(subclass, 'href') and
            hasattr(subclass, 'uri') and
            hasattr(subclass, 'images') and

            hasattr(subclass, 'from_id') and callable(subclass.from_id) and

            hasattr(subclass, 'artists') and
            hasattr(subclass, 'album') and
            hasattr(subclass, 'url') and 

            hasattr(subclass, 'get_recommendations') and callable(subclass.get_recommendations)
            or
            NotImplemented
        )
        
    @property
    @abstractmethod
    def id(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def href(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def uri(self):
        raise NotImplementedError
    
    @property
    @abstractmethod
    def images(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def followers(self):
        raise NotImplementedError
    
    @property
    @abstractmethod
    def albums(self):
        raise NotImplementedError
    
    @property
    @abstractmethod
    def tracks(self):
        raise NotImplementedError
    
    @property
    @abstractmethod
    def related_artists(self):
        raise NotImplementedError    
