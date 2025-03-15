from typing import Iterable, Generic, TypeVar

T = TypeVar('T')

class BaseEntityList(Iterable[T], Generic[T]):
    def __init__(self, entities: Iterable):
        self._entities = list(entities)

    def __len__(self):
        return len(self._entities)

    def __iter__(self):
        return iter(self._entities)

    def __getitem__(self, index):
        return self._entities[index]
