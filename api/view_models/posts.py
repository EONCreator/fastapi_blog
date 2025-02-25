from pydantic import BaseModel, constr
from typing import Optional


class PostCreate(BaseModel):
    title: constr(min_length=1, max_length=255)
    content: constr(min_length=1, max_length=5000)
    chapter_id: int

    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    title: constr(min_length=1, max_length=255)
    content: constr(min_length=1, max_length=5000)

    class Config:
        orm_mode = True