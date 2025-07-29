from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/ft_news")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def init_db():
    """
    Initializes database.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)