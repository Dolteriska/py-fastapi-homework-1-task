import datetime
from typing import Sequence, Optional
from fastapi_pagination import Page as BasePage
from pydantic import BaseModel, ConfigDict, Field, computed_field


class MovieBase(BaseModel):
    name: str
    date: datetime.date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str


class MovieListResponseSchema(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieDetailResponseSchema(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CustomMoviePagination(BasePage[MovieListResponseSchema]):
    movies: Sequence[MovieListResponseSchema] = Field(alias="items")
    total_pages: int = Field(alias="pages")
    total_items: int = Field(alias="total")

    @computed_field
    @property
    def next_page(self) -> Optional[str]:
        if self.page >= self.total_pages:
            return None
        return f"/theater/movies/?page={self.page + 1}&per_page={self.size}"

    @computed_field
    @property
    def prev_page(self) -> Optional[str]:
        if self.page <= 1:
            return None
        return f"/theater/movies/?page={self.page - 1}&per_page={self.size}"

    model_config = {
        "populate_by_name": True
    }
