from ...domain.interfaces.i_repositories.i_shop_management import IBrandRepository, ICategoryRepository, IProductRepository
from ...domain.interfaces.i_acls import IBrandACL, ICategoryACL, IProductACL
from ..dtos.shop_management import CategoryDTO, ProductDTO
from core.shop_management.application.exceptions import ProductNotFoundError, SizeNotFoundError
from core.shop_management.application.acl_exceptions import ProductNotFoundACLError, SizeNotFoundACLError
from core.utils.domain.interfaces.hosts.url_mapping import URLHost

import uuid

class ProductACL(IProductACL):
    def __init__(self, product_repository: IProductRepository):
        self.product_rep = product_repository

    def fetch_sample_of_size(self, product_uuid: uuid.UUID, size_uuid: uuid.UUID | None = None) -> ProductDTO:
        try:
            return ProductDTO.from_entity(self.product_rep.fetch_sample_of_size(public_uuid=product_uuid, size_public_uuid=size_uuid))
        except ProductNotFoundError as e:
            raise ProductNotFoundACLError(e.raw_msg)
        except SizeNotFoundError as e:
            raise SizeNotFoundACLError(e.raw_msg)

class CategoryACL(ICategoryACL):
    def __init__(self, category_repository: ICategoryRepository):
        self.category_rep = category_repository

    def fetch_categories(self, limit: int | None = None, order: str | None = None, url_mapping_adapter: URLHost | None = None) -> list[CategoryDTO]:
        return [CategoryDTO.from_entity(entity, url_mapping_adapter=url_mapping_adapter) for entity in self.category_rep.fetch_categories(limit, order)]

class BrandACL(IBrandACL):
    def __init__(self, brand_repository: IBrandRepository):
        self.brand_rep = brand_repository
