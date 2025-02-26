from ...application.dtos.shop_management import CategoryDTO, ProductDTO

from abc import ABC, abstractmethod
import uuid

class IProductACL(ABC):
    @abstractmethod
    def fetch_product_by_uuid(self, public_uuid: uuid.UUID | None, load_sizes: bool, load_images: bool) -> ProductDTO:
        pass

class ICategoryACL(ABC):
    @abstractmethod
    def fetch_categories(self, limit: int = None, order: str = None) -> list[CategoryDTO]:
        pass

class IBrandACL(ABC):
    pass