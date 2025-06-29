from abc import abstractmethod

from .base_repository import BaseRepository

class ISessionRepository(BaseRepository):
    @abstractmethod
    def get(self, key: str, default=None):
        """Retrieve a value from the session."""
        pass

    @abstractmethod
    def set(self, key: str, value: any):
        """Set a value in the session."""
        pass

    @abstractmethod
    def delete(self, key: str):
        """Delete a value from the session."""
        pass

    @abstractmethod
    def clear(self):
        """Clear the entire session."""
        pass
