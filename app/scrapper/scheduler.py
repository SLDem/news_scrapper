from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from app.db.database import async_session
from app.db.crud import save_article, article_exists
import logging
import app.config as config

from app.scrapper.fetcher import get_article_links, fetch_page
from app.scrapper.parser import parse_article

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def scrape_articles(initial=False):
    """
    Start scraping articles from web.
    :param initial: is it the initial scrape.
    """
    logger.info("Starting article scrape")
    try:
        urls = await get_article_links()
        for url in urls:
            async with async_session() as session:
                if await article_exists(session, url):
                    continue

                try:
                    html = await fetch_page(url)
                    article = parse_article(html, url)

                    if not article:
                        continue

                    article["scraped_at"] = datetime.utcnow()
                    await save_article(session, article)
                    logger.info(f"Saved article: {article['title']}")
                except Exception as e:
                    logger.warning(f"Failed to scrape {url}: {e}")

    except Exception as e:
        logger.error(f"Scraper failed: {e}")


def start_scheduler():
    """
    Start job scheduler for articles.
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scrape_articles, 'interval', minutes=config.SCRAPE_INTERVAL)
    scheduler.start()
    logger.info("Scheduler started")
