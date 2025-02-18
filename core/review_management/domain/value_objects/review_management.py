from ....utils.domain.value_objects.common import BaseEntityCollection

from typing import Optional

MAX_REVIEWS = 100

class ReviewCollection(BaseEntityCollection):
    def __post_init__(self):
        self.validate_length(max_length=MAX_REVIEWS)

    def validate_length(self, max_length: Optional[int] = None) -> None:
        if max_length is not None and len(self._entities) > max_length:
            raise ValueError(f"{self.__class__.__name__} contains more than {max_length} entities.")