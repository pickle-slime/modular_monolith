from ...application.dtos.shop_management import CategoryDTO, ProductDTO
from core.utils.domain.interfaces.hosts.url_mapping import URLHost

from abc import ABC, abstractmethod
import uuid

class IProductACL(ABC):
    @abstractmethod
    def fetch_sample_of_size(self, product_uuid: uuid.UUID, size_uuid: uuid.UUID | None = None) -> ProductDTO:
        pass

class ICategoryACL(ABC):
    @abstractmethod
    def fetch_categories(self, limit: int | None = None, order: str | None = None, url_mapping_adapter: URLHost | None = None) -> list[CategoryDTO]:
        pass

class IBrandACL(ABC):
    pass
