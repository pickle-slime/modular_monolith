from abc import ABC
from typing import TypeVar

Host = TypeVar("Host", bound='BaseHost')

class BaseHost(ABC):
    """A common base for all host types."""