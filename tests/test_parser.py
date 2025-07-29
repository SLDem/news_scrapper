import pytest

from app.scrapper.parser import parse_article


def test_parse_article_valid_html():
    """
    Test article parsing.
    """
    html = """
    <html>
      <head><meta property="og:image" content="https://img.jpg"></head>
      <body>
        <h1>Test Title</h1>
        <p class="article__standfirst">This is a subtitle</p>
        <article>
          <p>Paragraph 1</p>
          <p>Paragraph 2</p>
        </article>
        <a data-trackable="author-name">John Smith</a>
        <time datetime="2024-07-01T12:00:00Z"></time>
      </body>
    </html>
    """

    article = parse_article(html, "https://example.com/article")

    assert article["title"] == "Test Title"
    assert article["subtitle"] == "This is a subtitle"
    assert "Paragraph 1" in article["content"]
    assert article["author"] == "John Smith"
    assert article["image_url"] == "https://img.jpg"
    assert isinstance(article["word_count"], int)
    assert "min read" in article["reading_time"]
