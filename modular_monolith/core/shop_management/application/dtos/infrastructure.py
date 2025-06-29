from core.shop_management.application.dtos.base_dto import BaseInfDTO
from core.shop_management.domain.aggregates.shop_management import Product as ProductEntity

class PaginatedProductsInfDTO(BaseInfDTO[ProductEntity]):
    products: list[ProductEntity]
    has_previous: bool
    has_next: bool
    previous_page_number: int
    next_page_number: int
    current_page: int
    page_range: list[int]
