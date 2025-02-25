from sqlalchemy import String, Integer, ForeignKey, Column, Date
from sqlalchemy.orm import relationship
from database.database import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    date = Column(Date)

    chapter_id = Column(Integer, ForeignKey('chapters.id'))
    chapter = relationship("Chapter", back_populates="posts")