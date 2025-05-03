from abc import abstractmethod
from typing import Optional, Literal
import uuid

from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity
from core.utils.domain.interfaces.i_repositories.base_repository import BaseRepository

class ICategoryRepository(BaseRepository):
    @abstractmethod
    def fetch_categories(self, limit: Optional[int] = None, order: Optional[str]=None) -> list[CategoryEntity]:
        pass

    @abstractmethod
    def fetch_category_by_slug(self, slug: str) -> CategoryEntity | None:
        pass

    @abstractmethod
    def fetch_categories_by_uuids(self, uuids: list[str]) -> list[CategoryEntity]:
        pass

    @abstractmethod
    def fetch_by_uuid(self, pub_uuid: uuid.UUID) -> CategoryEntity:
        pass

class IBrandRepository(BaseRepository):
    @abstractmethod
    def fetch_brands(self, limit: Optional[int] = 0) -> list[BrandEntity]:
        pass

    @abstractmethod
    def fetch_by_uuid(self, pub_uuid: uuid.UUID) -> BrandEntity:
        pass

class IProductRepository(BaseRepository):
    @abstractmethod
    def fetch_product_by_uuid(
        self,
        inner_uuid: uuid.UUID | None,
        public_uuid: uuid.UUID | None,
    ) -> ProductEntity:
        pass

    @abstractmethod
    def all(self) -> list[ProductEntity]:
        pass

    @abstractmethod
    def filter_products(
            self,
            price_min: float,
            price_max: float,
            sort_by: Literal['count_of_selled', 'price', '-time_updated'],
            category_pubs: list[uuid.UUID] | None = None,
            brand_pubs: list[uuid.UUID] | None = None,
        ) -> list[ProductEntity]:
        pass

    @abstractmethod
    def filter_by_category_slug(self, category_slug: str | None) -> list[ProductEntity]:
        pass

    @abstractmethod
    def fetch_by_slugs(self, category_slug: str, product_slug: str) -> ProductEntity:
        pass

    @abstractmethod
    def searching_products(self, query: str | None = None, category_pub: uuid.UUID | None = None) -> list[ProductEntity]:
        pass

    @abstractmethod
    def fetch_hot_deals(self, days: int) -> list[ProductEntity]:
        pass

    @abstractmethod
    def fetch_top_selling(self, amount: int, indent: int = 0) -> list[ProductEntity]:
        pass

    @abstractmethod 
    def fetch_related_products(
        self,
        brand: uuid.UUID,
        limit: int = 1,
        select_related: Optional[str] = None
    ) -> list[ProductEntity]:
        pass

    @abstractmethod
    def fetch_sample_of_size(
        self,
        public_uuid: uuid.UUID | None,
        size_public_uuid: uuid.UUID | None,
    ) -> ProductEntity:
        '''Fetches the Product entity with the first found size and image'''
        pass
