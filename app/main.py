from fastapi import FastAPI, HTTPException, Query
from app.scraper import scrape_website

app = FastAPI()


@app.get("/scrape")
def run_scraper():
    try:
        results = scrape_website()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

