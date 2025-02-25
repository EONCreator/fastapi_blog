from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from entities import Chapter
from typing import List


class ChapterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str) -> Chapter:
        new_chapter = Chapter(name=name)
        self.session.add(new_chapter)
        await self.session.commit()
        await self.session.refresh(new_chapter)
        return new_chapter

    async def get(self, chapter_id: int) -> Chapter:
        result = await self.session.execute(select(Chapter).where(Chapter.id == chapter_id))
        return result.scalars().first()

    async def update(self, chapter_id: int, name: str) -> Chapter:
        chapter = await self.get(chapter_id)
        if chapter:
            if name is not None:
                chapter.name = name
            await self.session.commit()
            await self.session.refresh(chapter)
        return chapter

    async def delete(self, chapter_id: int) -> None:
        chapter = await self.get(chapter_id)
        if chapter:
            await self.session.delete(chapter)
            await self.session.commit()

    async def get_all(self, page: int = 1, size: int = 10) -> List[Chapter]:
        offset = (page - 1) * size
        result = await self.session.execute(select(Chapter).offset(offset).limit(size))
        return result.scalars().all()

    async def get_by_name(self, name: str):
        result = await self.session.execute(
            select(Chapter).where(Chapter.name == name)
        )
        return result.scalars().first()