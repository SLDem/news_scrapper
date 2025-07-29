from datetime import datetime

from bs4 import BeautifulSoup


def parse_article(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    if soup.find("div", class_="article-barrier"):
        raise ValueError("Paywalled article")

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    subtitle_tag = soup.find("p", class_="article__standfirst")  # example class
    subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else None

    content_blocks = soup.select("article p")
    content = "\n".join(p.get_text() for p in content_blocks)

    author_tag = soup.find("a", attrs={"data-trackable": "author-name"})
    author = author_tag.get_text(strip=True) if author_tag else None

    published_at_tag = soup.find("time")
    published_at = None
    if published_at_tag and published_at_tag.has_attr("datetime"):
        try:
            published_at = datetime.fromisoformat(
                published_at_tag["datetime"].replace("Z", "+00:00")).astimezone().replace(tzinfo=None)
        except Exception:
            pass

    tags = []
    tags_container = soup.find("ul", class_="article-tags")
    if tags_container:
        tag_links = tags_container.find_all("a")
        tags = [tag.get_text(strip=True) for tag in tag_links]

    image_url = None
    image_tag = soup.find("meta", property="og:image")
    if image_tag and image_tag.has_attr("content"):
        image_url = image_tag["content"]

    word_count = len(content.split())

    reading_time = None
    reading_time_tag = soup.find("span", class_="reading-time")
    if reading_time_tag:
        reading_time = reading_time_tag.get_text(strip=True)
    else:
        minutes = max(1, word_count // 200)
        reading_time = f"{minutes} min read"

    related_articles = []
    related_section = soup.find("section", class_="related-articles")
    if related_section:
        links = related_section.find_all("a", href=True)
        related_articles = [link["href"] for link in links if link["href"].startswith("http")]

    return {
        "url": url,
        "title": title,
        "subtitle": subtitle,
        "content": content,
        "author": author,
        "published_at": published_at,
        "tags": tags,
        "image_url": image_url,
        "word_count": word_count,
        "reading_time": reading_time,
        "related_articles": related_articles,
    }
