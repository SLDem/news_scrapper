import pytest
from app.db.crud import save_article, article_exists
from datetime import datetime


@pytest.mark.asyncio
async def test_save_and_check_article(db_session):
    """
    Test saving articles.
    :param db_session: database session to use.
    """
    url = "https://ft.com/test-article"
    data = {
        "url": url,
        "title": "Test Article",
        "subtitle": "Test Subtitle",
        "content": "This is a test.",
        "author": "Test Author",
        "published_at": datetime.utcnow(),
        "scraped_at": datetime.utcnow(),
        "tags": ["Politics", "UK"],
        "image_url": "https://image.jpg",
        "word_count": 42,
        "reading_time": "1 min read",
        "related_articles": ["https://related.com"]
    }

    exists_before = await article_exists(db_session, url)
    assert not exists_before

    await save_article(db_session, data)

    exists_after = await article_exists(db_session, url)
    assert exists_after
