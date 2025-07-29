import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from app.db.database import init_db
from app.api.routes import router
from app.scrapper.scheduler import start_scheduler, scrape_articles


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes db, starts initial scrape and scheduler when app runs.
    """
    logger.info("Initializing database...")
    await init_db()
    logger.info("Starting first scrape...")
    await scrape_articles(initial=True)
    logger.info("Starting scheduler...")
    start_scheduler()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
