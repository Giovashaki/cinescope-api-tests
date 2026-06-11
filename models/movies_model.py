from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal


class GenreModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None


class MovieModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    price: float
    description: str
    imageUrl: Optional[str] = None
    location: Literal["MSK", "SPB"]
    published: bool
    genreId: int
    genre: Optional[GenreModel] = None
    createdAt: str
    rating: float = Field(ge=0, le=5)


class FindAllMoviesResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    movies: List[MovieModel]
    count: int = Field(ge=0)
    page: int
    pageSize: int
    pageCount: int