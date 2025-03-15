from ..entitites.notification_management import NewsLetter as NewsLetterEntity

from abc import ABC, abstractmethod
from typing import Iterator

class INewsLetterRepository(ABC):
    @abstractmethod
    def fetch_iterator(self) -> Iterator[NewsLetterEntity]:
        pass
    
    @abstractmethod
    def save(self, newsletter_entity: NewsLetterEntity) -> bool:
        pass