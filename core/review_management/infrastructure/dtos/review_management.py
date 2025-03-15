from core.utils.application.base_dto import BaseDTO
from core.review_management.domain.entities.review_management import Review as ReviewEntity

from pydantic import Field

class PaginatedReviewsDTO(BaseDTO["PaginatedReviewsDTO"]):
    reviews: list[ReviewEntity] | None = Field(default=None, title="Reviews")
    
    #pagination details
    current_page: int | None = Field(default=None, ge=0, title="Current Page", alias="currentPage")
    num_pages: int | None = Field(default=None, ge=0, title="Number of Pages", alias="numPages")
    has_previous: bool | None = Field(default=None, title="Has Previous", alias="hasPrevious")
    has_next: bool | None = Field(default=None, title="Has Next", alias="hasNext")
    total_count: int | None = Field(default=None, ge=0, title="Total Count", alias="totalCount")
