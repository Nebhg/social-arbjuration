from typing import List
from fastapi import FastAPI, HTTPException, Query

from app.scrapers.google_trends_scraper import GoogleTrendsScraper
app = FastAPI()


@app.get("/scrape")
def run_scraper(search_terms: List[str] = Query(...)):
    scraper = GoogleTrendsScraper()
    results = []
    try:
        for term in search_terms:
            print(term)
            res = scraper.scrape(term)
            results.append(res)
    except Exception as e:
        scraper.close()
        raise HTTPException(status_code=500, detail=str(e))
    scraper.close()
    return results