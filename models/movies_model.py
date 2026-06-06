from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class GenreModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None


class MovieModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    price: float
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    location: Optional[str] = None
    published: bool
    genreId: Optional[int] = None
    genre: Optional[GenreModel] = None
    createdAt: Optional[str] = None
    rating: Optional[float] = None


class FindAllMoviesResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    movies: List[MovieModel]
    count: int = Field(ge=0)
    page: int
    pageSize: int
    pageCount: int