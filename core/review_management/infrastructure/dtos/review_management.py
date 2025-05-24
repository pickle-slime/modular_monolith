from core.review_management.application.dtos.base_dto import BaseDTO

from pydantic import Field
from datetime import datetime
import uuid

class PaginatedReviewItemDTO(BaseDTO["PaginatedReviewItemDTO"]):
    pub_uuid: uuid.UUID | None = Field(default=None)

    text: str | None = Field(default=None, min_length=1, max_length=10000, title="Text")
    rating: int | None = Field(default=None, ge=0, le=5, title="Rating")
    datetime_created: datetime | None = Field(default=None, title="DateTime Created")

    username: str | None = Field(default=None, title="User", description="Contains owner's username")

class PaginatedReviewsDTO(BaseDTO["PaginatedReviewsDTO"]):
    reviews: list[PaginatedReviewItemDTO] | None = Field(default=None, title="Reviews")
    
    #pagination details
    current_page: int | None = Field(default=None, ge=0, title="Current Page")
    num_pages: int | None = Field(default=None, ge=0, title="Number of Pages")
    has_previous: bool | None = Field(default=None, title="Has Previous")
    has_next: bool | None = Field(default=None, title="Has Next")
    total_count: int | None = Field(default=None, ge=0, title="Total Count")

