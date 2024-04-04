from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from .base_scraper import BaseScraper

class GoogleSearchScraper(BaseScraper):
    def scrape(self, search_term, num_results=100):
        results = []
        paa_results = []
        seen_urls = set()  # To keep track of URLs we have already seen
        paa_seen = set()  # To keep track of PAA questions we have already seen

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
            except TimeoutException:
                print("Cookie consent button was not found in time")

            time.sleep(2)  # Small delay to mimic human interaction
            
            while len(results) < num_results:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")

                for result in search_results:
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    link = link_element.get_attribute("href")

                    if link in seen_urls:
                        continue
                    seen_urls.add(link)

                    result_data = {}
                    
                    title_element = result.find_element(By.CSS_SELECTOR, "h3.LC20lb")
                    if title_element and title_element.text.strip():
                        result_data["title"] = title_element.text.strip()

                    result_data["link"] = link  # Assuming link is always present

                    snippet_elements = result.find_elements(By.CSS_SELECTOR, "div.VwiC3b")
                    if snippet_elements:
                        result_data["snippet"] = snippet_elements[0].text
                    
                    rating_elements = result.find_elements(By.CSS_SELECTOR, "div.fG8Fp.uo4vr span")
                    for elem in rating_elements:
                        if 'Rating:' in elem.text:
                            result_data["rating"] = elem.text
                            break

                    reviews_elements = result.find_elements(By.CSS_SELECTOR, "div.fG8Fp.uo4vr > span:nth-of-type(3)")
                    if reviews_elements:
                        result_data["reviews"] = reviews_elements[0].text

                    if result_data:  # Only append if there's data to add
                        results.append(result_data)

                    if len(results) >= num_results:
                        break

                try:
                    more_results_button = self.driver.find_element(By.CSS_SELECTOR, "div.GNJvt.ipz2Oe")
                    self.driver.execute_script("arguments[0].click();", more_results_button)
                    print("Clicked 'More results' button")
                except NoSuchElementException:
                    print("No 'More results' button found or end of results reached")
                    break

                paa_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.related-question-pair"))
                )
                for element in paa_elements:
                    question = element.find_element(By.CSS_SELECTOR, "div").text
                    if question not in paa_seen:
                        paa_results.append(question)
                        paa_seen.add(question)

                if len(results) >= num_results:
                    print(f"Reached the desired number of results: {len(results)}")
                    break

            results = results[:num_results]
            
        except Exception as e:
            print(f"An error occurred: {e}")
            results = {"error": str(e)}
        finally:
            self.close()
            
        return {'results': results, 'peopleAlsoAsked': paa_results}
