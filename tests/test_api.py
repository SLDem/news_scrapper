from datetime import datetime
import pytest


@pytest.mark.asyncio
async def test_get_articles_after_scraping(client, db_session):
    """
    Test article endpoint with data.
    :param client: http client.
    :param db_session: database session to use.
    """
    article_data = {
        "url": "https://ft.com/test-data-check",
        "title": "Test Data Exists",
        "subtitle": "Subtitle here",
        "content": "Full content text.",
        "author": "Jane Scraper",
        "published_at": datetime.utcnow(),
        "scraped_at": datetime.utcnow(),
        "tags": ["News"],
        "image_url": "https://img.test.jpg",
        "word_count": 100,
        "reading_time": "1 min read",
        "related_articles": ["https://ft.com/related1"]
    }

    from app.db.crud import save_article
    await save_article(db_session, article_data)

    response = await client.get("/articles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    first = data[0]
    assert first["url"] == article_data["url"]
    assert first["title"] == article_data["title"]
    assert first["word_count"] == 100
    assert "Test Data Exists" in first["title"]


@pytest.mark.asyncio
async def test_get_articles_empty(client):
    """
    Tests articles endpoint for empty response.
    :param client: http client.
    """
    response = await client.get("/articles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_scrape_now(client):
    """
    Tests scrape now endpoint.
    :param client: http client.
    """
    response = await client.get("/scrape-now")
    assert response.status_code == 200
