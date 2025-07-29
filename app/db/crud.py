import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Article


async def article_exists(session: AsyncSession, url: str) -> bool:
    result = await session.execute(select(Article).filter_by(url=url))
    return result.scalar_one_or_none() is not None


async def save_article(session: AsyncSession, data: dict):
    """
    Save article to database.
    :param session: async session to use.
    :param data: article data.
    """
    article = Article(
        url=data["url"],
        title=data["title"],
        content=data["content"],
        author=data.get("author"),
        published_at=data["published_at"],
        scraped_at=data["scraped_at"],
        subtitle=data["subtitle"],
        tags=json.dumps(data.get("tags", [])),
        image_url=data["image_url"],
        word_count=data["word_count"],
        reading_time=data["reading_time"],
        related_articles=json.dumps(data.get("related_articles", []))
    )
    session.add(article)
    await session.commit()
