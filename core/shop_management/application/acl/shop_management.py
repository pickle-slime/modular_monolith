from ...domain.interfaces.i_repositories.i_shop_management import IBrandRepository, ICategoryRepository, IProductRepository
from ...domain.interfaces.i_acls import IBrandACL, ICategoryACL, IProductACL
from ..dtos.shop_management import CategoryDTO, ProductDTO, ProductSizeDTO

import uuid

class ProductACL(IProductACL):
    def __init__(self, product_repository: IProductRepository):
        self.product_rep = product_repository

    def fetch_first_sample(self, public_uuid: uuid.UUID | None) -> ProductDTO:
        return ProductDTO.from_entity(self.product_rep.fetch_first_sample(public_uuid=public_uuid))

class CategoryACL(ICategoryACL):
    def __init__(self, category_repository: ICategoryRepository):
        self.category_rep = category_repository

    def fetch_categories(self, limit: int = None, order: str = None) -> list[CategoryDTO]:
        return [CategoryDTO.from_entity(entity) for entity in self.category_rep.fetch_categories(limit, order)]

class BrandACL(IBrandACL):
    def __init__(self, brand_repository: IBrandRepository):
        self.brand_rep = brand_repository