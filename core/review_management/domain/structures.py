from core.utils.domain.structures import BaseEntityList
from core.review_management.domain.entities.review_management import Review as ReviewEntity, ReviewEntityType

from typing import Generic, Optional, Iterable

MAX_REVIEWS = 100

class ReviewCollection(Generic[ReviewEntityType], BaseEntityList[ReviewEntity]):
    def __init__(self, entities: Iterable[ReviewEntity]):
        super().__init__(entities)
        self.validate_length(max_length=MAX_REVIEWS)

    def validate_length(self, max_length: Optional[int] = None) -> None:
        if max_length is not None and len(self._entities) > max_length:
            raise ValueError(f"{self.__class__.__name__} contains more than {max_length} entities.")
        
    def append(self, review: ReviewEntity) -> 'ReviewCollection':
        self._entities.append(review)
        return self
