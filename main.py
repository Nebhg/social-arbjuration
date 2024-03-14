from fastapi import FastAPI, HTTPException, Query

from app.scrapers.reddit_scraper import RedditScraper
app = FastAPI()


@app.get("/scrape")
def run_scraper(search_term: str = Query(...)):
    scraper = RedditScraper()
    try:
        results = scraper.scrape(search_term)
        return results
    except Exception as e:
        scraper.close()
        raise HTTPException(status_code=500, detail=str(e))
