from sqlalchemy import Column, String, Text, DateTime, Integer, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Article(Base):
    """
    Main model for saving articles.
    """
    __tablename__ = "articles"

    url = Column(String, primary_key=True, index=True)
    title = Column(String)
    subtitle = Column(String)
    tags = Column(JSON, nullable=True)
    image_url = Column(String)
    word_count = Column(Integer, nullable=True)
    reading_time = Column(String)
    related_articles = Column(JSON, nullable=True)
    content = Column(Text)
    author = Column(String, nullable=True)
    published_at = Column(DateTime)
    scraped_at = Column(DateTime)
