from abc import ABC
from typing import TypeVar

Repository = TypeVar("Repository", bound='BaseRepository')

class BaseRepository(ABC):
    """A common base for all repository types."""
