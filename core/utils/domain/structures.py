from core.utils.domain.entity import EntityType
from typing import Iterable, Generic

class BaseEntityList(Generic[EntityType]):
    def __init__(self, entities: Iterable[EntityType]):
        self._entities = list(entities)

    def __len__(self):
        return len(self._entities)

    def __iter__(self):
        return iter(self._entities)

    def __getitem__(self, index):
        return self._entities[index]
