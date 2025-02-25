from sqlalchemy import String, Integer, ForeignKey, Column, Date
from sqlalchemy.orm import relationship
from database.database import Base


class Chapter(Base):
    __tablename__ = 'chapters'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    posts = relationship("Post", back_populates="chapter", cascade="all, delete-orphan")