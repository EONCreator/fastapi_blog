from typing import List

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from entities import Post
from datetime import date, datetime


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, title: str, content: str, chapter_id: int):
        new_post = Post(title=title,
                        content=content,
                        date=datetime.now().date(),
                        chapter_id=chapter_id)
        self.session.add(new_post)
        await self.session.commit()
        await self.session.refresh(new_post)
        return new_post

    async def get(self, post_id: int):
        result = await self.session.execute(select(Post).where(Post.id == post_id))
        return result.scalar_one_or_none()

    async def update(self, post_id: int, title: str, content: str):
        post = await self.get(post_id)
        if post:
            if title is not None:
                post.title = title
            if content is not None:
                post.content = content
            await self.session.commit()
            await self.session.refresh(post)
            return post
        return None

    async def delete(self, post_id: int):
        post = await self.get(post_id)
        if post:
            await self.session.delete(post)
            await self.session.commit()
            return True
        return False

    async def get_all(self, page: int = 1, size: int = 10) -> List[Post]:
        offset = (page - 1) * size
        result = await self.session.execute(select(Post).offset(offset).limit(size))
        return result.scalars().all()

    async def get_by_title(self, title: str):
        result = await self.session.execute(
            select(Post).where(Post.title == title)
        )
        return result.scalars().first()