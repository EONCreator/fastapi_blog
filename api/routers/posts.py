from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from repositories.post_repository import PostRepository

from api.view_models.posts import PostCreate, PostUpdate

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post("/")
async def create_post(post: PostCreate,
                      session: AsyncSession = Depends(get_async_session)):
    repo = PostRepository(session)

    validate_post_data(post)

    existing_post = await repo.get_by_title(post.title)
    if existing_post:
        raise HTTPException(status_code=400, detail="Post with this title already exists.")

    new_post = await repo.create(post.title, post.content, post.chapter_id)
    return new_post


@router.get("/{post_id}")
async def get_post(post_id: int,
                   session: AsyncSession = Depends(get_async_session)):
    repo = PostRepository(session)
    post = await repo.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}")
async def update_post(post_id: int,
                      post: PostUpdate,
                      session: AsyncSession = Depends(get_async_session)):
    repo = PostRepository(session)

    existing_post = await repo.get(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    validate_post_data(post)

    if post.title != existing_post.title:
        existing_with_same_title = await repo.get_by_title(post.title)
        if existing_with_same_title:
            raise HTTPException(status_code=400, detail="Post with this title already exists.")

    updated_post = await repo.update(post_id, post.title, post.content)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post


@router.delete("/{post_id}", response_model=dict)
async def delete_post(post_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    repo = PostRepository(session)
    result = await repo.delete(post_id)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}


@router.get("/")
async def get_posts(page: int = 1,
                    size: int = 10,
                    session: AsyncSession = Depends(get_async_session)):
    repo = PostRepository(session)
    posts = await repo.get_all(page, size)
    return posts


def validate_post_data(post):
    if not post.title or post.title.strip() == "":
        raise HTTPException(status_code=400, detail="Post title cannot be empty.")

    if not post.content or post.content.strip() == "":
        raise HTTPException(status_code=400, detail="Post content cannot be empty.")