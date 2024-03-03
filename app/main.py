from fastapi import FastAPI, HTTPException, Query
from scraper import scrape_website

app = FastAPI()


@app.get("/scrape")
def run_scraper(url: str = Query(..., description="The URL to scrape")):
    try:
        results = scrape_website(url)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"Hello": "Worladad11"}