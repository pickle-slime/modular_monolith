from core.review_management.domain.entities.review_management import Review as ReviewEntity, ReviewEntityType
from core.review_management.domain.entity import EntityType

from typing import Generic, Optional, Iterable

MAX_REVIEWS = 100

class BaseEntityList(Generic[EntityType]):
    def __init__(self, entities: Iterable[EntityType]):
        self._entities = list(entities)

    def __len__(self):
        return len(self._entities)

    def __iter__(self):
        return iter(self._entities)

    def __getitem__(self, index):
        return self._entities[index]

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
