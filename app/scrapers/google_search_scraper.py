from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from .base_scraper import BaseScraper


class GoogleSearchScraper(BaseScraper):

    def __init__(self, num_results=100):
        super().__init__()
        self.num_results = num_results

    def scroll_and_parse(self):
        results = []
        seen_urls = set()
        paa_results = []
        paa_seen = set()

        while len(results) < self.num_results:
            time.sleep(0.5)  # Wait for the dynamic content to load.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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

            try:
                more_results_button = self.driver.find_element(By.CSS_SELECTOR, "div.GNJvt.ipz2Oe")
                self.driver.execute_script("arguments[0].click();", more_results_button)
                print("Clicked 'More results' button")
            
            except NoSuchElementException:
                    print("No 'More results' button found or end of results reached")
                    break

        return results, paa_results

    def scrape(self, search_term):
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
            results, paa_results = self.scroll_and_parse()
            return {'results': results, 'peopleAlsoAsked': paa_results}
        finally:
            self.close()  # Ensures that the driver is quit even if an exception occurs

    #testing git