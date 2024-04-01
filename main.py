from fastapi import FastAPI, HTTPException, Query
from asyncio import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List
from app.scrapers.google_trends_scraper import GoogleTrendsScraper
from app.scrapers.generic_url_scraper import GenericUrlScraper
import logging
import debugpy
import redis 
from rejson import Client, Path
import json

debugpy.listen(5678)
app = FastAPI()
r = redis.Redis(host="redis", port=6379)
# Initialize the RedisJSON client
rj = Client(host='redis', port=6379, decode_responses=True)

@app.get("/hits")
def read_root():
    r.incr("hits")
    return {"number of hits": r.get("hits")}

@app.get("/scrapeBody")
def run_url_scraper(url: str):
    scraper = GenericUrlScraper()
    try:
        results = scraper.scrape(url)
        rj.jsonset(url, Path.rootPath(), results)
        
        return results
    except Exception as e:
        scraper.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scrape")
def run_scraper(search_term: str = Query(...)):
    scraper = GoogleTrendsScraper()
    try:
        results = scraper.scrape(search_term)
        return results
    except Exception as e:
        scraper.close()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/batch-scrape")
async def run_batch_scraper(search_terms: List[str] = Query(...)):
    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Map each search term to a future
        future_to_search_term = {executor.submit(run_scraper, term): term for term in search_terms}

        for future in as_completed(future_to_search_term):
            term = future_to_search_term[future]
            try:
                data = future.result()  # Retrieve the result from the future
                results.append({term: data})
            except Exception as exc:
                results.append({term: f"Scraping failed with exception: {str(exc)}"})

    return results


    
