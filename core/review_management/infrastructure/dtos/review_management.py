from core.utils.application.base_dto import DTO
from core.review_management.domain.entities.review_management import Review as ReviewEntity

from pydantic import BaseModel, Field
from typing import Generic

class PaginatedReviewsDTO(BaseModel, Generic[DTO]):
    reviews: list[ReviewEntity] = Field(default=[])
    
    #pagination details
    current_page: int = Field(default=0)
    num_pages: int = Field(default=0)
    has_previous: bool = Field(default=False)
    has_next: bool = Field(default=False)
    total_count: int = Field(default=0)
