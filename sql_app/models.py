from sqlalchemy import Column, Integer, String

from .database import Base


class Anime(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    studio = Column(String)
    writer = Column(String)
    