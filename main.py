from fastapi import FastAPI, HTTPException, Query

from app.scrapers.google_trends_scraper import GoogleTrendsScraper
app = FastAPI()


@app.get("/scrape")
def run_scraper(search_term: str = Query(...)):
    scraper = GoogleTrendsScraper()
    try:
        results = scraper.scrape(search_term)
        return results
    except Exception as e:
        scraper.close()
        raise HTTPException(status_code=500, detail=str(e))
