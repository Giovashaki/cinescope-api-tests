from sqlalchemy import Column, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MovieDBModel(Base):
    __tablename__ = "movies"

    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float)
    genre_id = Column(String)
    created_at = Column(DateTime)

    def __repr__(self):
        return f"<Movie(id='{self.id}', name='{self.name}')>"