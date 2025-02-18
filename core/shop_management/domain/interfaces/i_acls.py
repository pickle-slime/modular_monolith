from ...application.dtos.shop_management import CategoryDTO

from abc import ABC, abstractmethod

class IProductACL(ABC):
    pass

class ICategoryACL(ABC):
    @abstractmethod
    def fetch_categories(self, limit: int = None, order: str = None) -> list[CategoryDTO]:
        pass

class IBrandACL(ABC):
    pass