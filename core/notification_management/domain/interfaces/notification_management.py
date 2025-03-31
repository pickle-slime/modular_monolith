from ..entities.notification_management import NewsLetter as NewsLetterEntity

from abc import ABC, abstractmethod
from typing import Iterator
import uuid

class INewsLetterRepository(ABC):
    @abstractmethod
    def fetch_iterator(self) -> Iterator[NewsLetterEntity]:
        pass
    
    @abstractmethod
    def create(self, email: str, user_public_uuid: uuid.UUID | None = None) -> NewsLetterEntity | None:
        pass
