import logging
from fastapi import FastAPI
import uvicorn

from app.db.database import init_db
from app.api.routes import router
from app.scrapper.scheduler import start_scheduler, scrape_articles

app = FastAPI()
app.include_router(router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    await init_db()
    logger.info("Starting first scrape...")
    await scrape_articles(initial=True)
    logger.info("Starting scheduler...")
    start_scheduler()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
