from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from .base_scraper import BaseScraper

class GoogleSearchScraper(BaseScraper):
    def scrape(self, search_term):
        results = []
        try:
            search_url = f"https://www.google.com/search?q={search_term}"
            self.driver.get(search_url)
            print("Search URL retrieved")
            
            # Accept cookies
            try:
                consent_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='L2AGLb']"))
                )
                consent_button.click()
                print("Cookie consent accepted")
            except NoSuchElementException:
                print("No cookie consent button found")
            
            time.sleep(2)  # Small delay to mimic human interaction
            
            # Scroll to the end of the page to ensure all results are loaded
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Allow time for the next results to load
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Retrieve and parse the search results
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")

            for result in search_results:
                try:
                    title_element = result.find_element(By.CSS_SELECTOR, "h3")
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    snippet_element = result.find_element(By.CSS_SELECTOR, "span")
                    title = title_element.text if title_element else "No title"
                    link = link_element.get_attribute("href") if link_element else "No link"
                    snippet = snippet_element.text if snippet_element else "No snippet"
                    results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })
                except Exception as e:
                    print(f"Error parsing result: {e}")

            print(f"Found {len(results)} results")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            results = {"error": str(e)}
        finally:
            self.close()
            
        return {'results': results}
