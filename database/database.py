import os
from dotenv import load_dotenv

import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_session, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def create_database_if_not_exists():
    print("Creating database...")
    conn = await asyncpg.connect(user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)
    try:
        databases = await conn.fetch("SELECT datname FROM pg_database;")
        if DATABASE_NAME not in [db['datname'] for db in databases]:
            await conn.execute(f"CREATE DATABASE {DATABASE_NAME}")
    finally:
        await conn.close()


async def init_models():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
    async with async_session() as session:
        yield session