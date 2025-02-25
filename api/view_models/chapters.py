from pydantic import BaseModel, constr


class ChapterModel(BaseModel):
    name: constr(min_length=1)

    class Config:
        orm_mode = True
