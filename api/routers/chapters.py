from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.chapter_repository import ChapterRepository

from database.database import get_async_session
from api.view_models.chapters import ChapterModel

router = APIRouter(
    prefix="/chapters",
    tags=["Chapters"],
)


@router.post("/")
async def create_chapter(chapter: ChapterModel,
                         session: AsyncSession = Depends(get_async_session)):
    repo = ChapterRepository(session)

    validate_chapter_data(chapter)

    chapter = await repo.create(chapter.name)
    return chapter


@router.get("/{chapter_id}")
async def get_chapter(chapter_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    repo = ChapterRepository(session)
    chapter = await repo.get(chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.put("/{chapter_id}")
async def update_chapter(chapter_id: int, chapter: ChapterModel,
                         session: AsyncSession = Depends(get_async_session)):
    repo = ChapterRepository(session)

    existing_chapter = await repo.get(chapter_id)
    if not existing_chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    validate_chapter_data(chapter)

    if chapter.name != existing_chapter.name:
        existing_with_same_name = await repo.get_by_name(chapter.name)
        if existing_with_same_name:
            raise HTTPException(status_code=400, detail="Chapter with this name already exists.")

    chapter = await repo.update(chapter_id, chapter.name)
    return chapter


@router.delete("/{chapter_id}", response_model=dict)
async def delete_chapter(chapter_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    repo = ChapterRepository(session)

    chapter = await repo.get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    await repo.delete(chapter_id)
    return {"detail": "Chapter deleted"}


@router.get("/")
async def get_chapters(page: int = 1,
                       size: int = 10,
                       session: AsyncSession = Depends(get_async_session)):
    repo = ChapterRepository(session)
    chapters = await repo.get_all(page, size)
    return chapters


def validate_chapter_data(chapter):
    if not chapter.name or chapter.name.strip() == "":
        raise HTTPException(status_code=400, detail="Chapter name cannot be empty.")