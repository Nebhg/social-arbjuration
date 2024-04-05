from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from .base_scraper import BaseScraper

class GoogleSearchScraper(BaseScraper):
    def close(self):
        # Close the browser window
        self.driver.quit()

    def scroll_and_parse(self, num_scrolls=10):
        results = []
        seen_urls = set()
        paa_results = []
        paa_seen = set()

        for _ in range(num_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the dynamic content to load.
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Parse search results
            search_results = soup.find_all("div", class_="g")
            for result in search_results:
                link_element = result.find("a", href=True)
                if link_element:
                    link = link_element['href']
                    if link not in seen_urls:
                        seen_urls.add(link)
                        title_element = result.find("h3")
                        snippet_element = result.find("div", class_="VwiC3b")
                        rating_element = result.select_one("div.fG8Fp.uo4vr span:-soup-contains('Rating:')")
                        review_element = result.select_one("div.fG8Fp.uo4vr > span:nth-of-type(3)")

                        result_data = {
                            "title": title_element.text.strip() if title_element else None,
                            "link": link,
                            "snippet": snippet_element.text.strip() if snippet_element else None,
                            "rating": rating_element.text if rating_element else None,
                            "reviews": review_element.text if review_element else None
                        }
                        results.append(result_data)

            # Parse "People Also Ask" section
            paa_elements = soup.select("div.related-question-pair")
            for element in paa_elements:
                question = element.get_text().strip()
                if question not in paa_seen:
                    paa_results.append(question)
                    paa_seen.add(question)

        return results, paa_results

    def scrape(self, search_term, num_scrolls=5):
        try:
            search_url = f"https://www.google.com/search?q={search_term}"
            self.driver.get(search_url)
            self.driver.save_screenshot("Test01.png")
            # Accept cookies if the button is present
            try:
                consent_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='L2AGLb']"))
                )
                consent_button.click()
            except (NoSuchElementException, TimeoutException):
                print("No cookie consent button found or not found in time.")

            # Your scraping logic...
            results, paa_results = self.scroll_and_parse(num_scrolls)
            return {'results': results, 'peopleAlsoAsked': paa_results}
        finally:
            self.close()  # Ensures that the driver is quit even if an exception occurs