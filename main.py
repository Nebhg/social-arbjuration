from fastapi import FastAPI, HTTPException, Query

from app.scrapers.reddit_scraper import RedditScraper
app = FastAPI()


@app.get("/scrape")
def run_scraper():
    scraper = RedditScraper()
    try:
        results = scraper.scrape()
        return results
    except Exception as e:
        # If an error occurs, make sure to close the scraper before raising an HTTPException
        scraper.close()
        raise HTTPException(status_code=500, detail=str(e))
