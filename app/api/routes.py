import json

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.models import Article
from app.db.database import async_session
from sqlalchemy.future import select

from app.scrapper.scheduler import scrape_articles

router = APIRouter()


async def get_session() -> AsyncSession:
    """
    Gets async session
    """
    async with async_session() as session:
        yield session


@router.get("/articles", response_model=List[dict])
async def get_articles(
    author: Optional[str] = None,
    limit: int = Query(10, le=100),
    session: AsyncSession = Depends(get_session)
):
    """
    Displays articles with optional params, such as author, limit of displayed articles.
    :param author: author to filter articles by.
    :param limit: limit articles number.
    :param session: async session to use.
    :return: json of articles.
    """
    query = select(Article)
    if author:
        query = query.where(Article.author == author)
    result = await session.execute(query.order_by(Article.published_at.desc()).limit(limit))
    articles = result.scalars().all()
    return [
        {
            "url": a.url,
            "title": a.title,
            "subtitle": a.subtitle,
            "tags": json.loads(a.tags) if a.tags else [],
            "image_url": a.image_url,
            "word_count": a.word_count,
            "reading_time": a.reading_time,
            "related_articles": json.loads(a.related_articles) if a.related_articles else [],
            "content": a.content,
            "author": a.author,
            "published_at": a.published_at,
            "scraped_at": a.scraped_at,
        }
        for a in articles
    ]


@router.get("/scrape-now")
async def trigger_scrape():
    """
    Start scraping articles.
    :return: message with start confirmation.
    """
    await scrape_articles(initial=True)
    return {"status": "Scraping triggered"}
