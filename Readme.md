Usage:

1. `git clone https://github.com/SLDem/news_scrapper.git`
2. `docker-compose up --build`
3. go to `http://localhost:8000/articles` to view the pulled articles
4. go to `http://localhost:8000/scrape-now` to manually start scraping
5. go to `http://localhost:8000/docs` to view the api docs
6. run `pytest` to start tests.

Normally the scrapper restarts every 60 minutes, you can change this value in **app/config.py**.

