from abc import abstractmethod
from typing import List, Optional, Union, Literal
import uuid

from core.shop_management.domain.entities.shop_management import Category as CategoryEntity, Brand as BrandEntity, ProductSize as ProductSizeEntity, ProductImage as ProductImageEntity
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity
from core.utils.domain.value_objects.common import ForeignUUID
from .....utils.domain.interfaces.i_repositories.base_repository import BaseRepository

class ICategoryRepository(BaseRepository):
    @abstractmethod
    def fetch_categories(self, limit: Optional[int] = None, order: Optional[str]=None) -> List[CategoryEntity]:
        pass

    @abstractmethod
    def fetch_category_by_slug(self, slug: str) -> CategoryEntity:
        pass

    @abstractmethod
    def fetch_categories_by_uuids(self, ids: List[int]) -> List[CategoryEntity]:
        pass

    @abstractmethod
    def fetch_by_uuid(self, pub_uuid: uuid.UUID) -> CategoryEntity:
        pass

class IBrandRepository(BaseRepository):
    @abstractmethod
    def fetch_brands(self, limit: Optional[int] = 0) -> List[BrandEntity]:
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
    def filter_products(
        self,
        price_min: float,
        price_max: float,
        sort_by: Literal['count_of_selled', 'price', '-time_updated'],
        category_pub: uuid.UUID | None = None,
        brand_pub: uuid.UUID | None = None,
    ) -> list[ProductEntity]:
        pass

    @abstractmethod
    def filter_by_category_slug(self, category_slug: str) -> list[ProductEntity]:
        pass

    @abstractmethod
    def fetch_by_slugs(self, category_slug: str, product_slug: str) -> ProductEntity:
        pass

    @abstractmethod
    def searching_products(self, name: str | None = None, category_inner: uuid.UUID | None = None) -> list[ProductEntity]:
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
        brand: str,
        limit: int = 1,
        select_related: Optional[str] = None
    ) -> list[ProductEntity]:
        pass

    @abstractmethod
    def fetch_first_sample(
        self,
        inner_uuid: uuid.UUID | None,
        public_uuid: uuid.UUID | None,
    ) -> ProductEntity:
        '''Fetches the Product entity with the first found size and image'''
        pass