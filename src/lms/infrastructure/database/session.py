from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/lms"

engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

SYNC_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/lms"
sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)

Base = declarative_base()
