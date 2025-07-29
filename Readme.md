Usage:

1. `git clone repo`
2. `docker-compose up --build`
3. go to `http://localhost:8000/articles` to view the pulled articles
4. go to `http://localhost:8000/scrape-now` to manually start scraping
5. go to `http://localhost:8000/docs` to view the api docs

Normally the scrapper restarts every 60 minutes, you can change this value in **app/config.py**.