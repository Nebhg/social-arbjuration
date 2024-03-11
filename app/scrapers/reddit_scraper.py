# In your app/scrapers/reddit_scraper.py
from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class RedditScraper(BaseScraper):
    def scrape(self):
        try:
            url = "https://www.google.com/robots.txt"
            self.driver.get(url)
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            # Now that the page is loaded, you can use BeautifulSoup to parse it
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            body_content = soup.find('body').get_text(strip=True)
            return {"HTML Content": body_content}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": str(e)}
        finally:
            self.close()
