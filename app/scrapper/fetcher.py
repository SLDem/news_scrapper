import httpx
from bs4 import BeautifulSoup


async def fetch_page(url):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text


async def get_article_links():
    html = await fetch_page("https://www.ft.com/world")
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.select('a.js-teaser-heading-link'):
        href = a.get("href")
        if href and href.startswith("/content/"):
            links.append("https://www.ft.com" + href)
    return list(set(links))
