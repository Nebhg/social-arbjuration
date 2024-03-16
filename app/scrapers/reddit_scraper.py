# In your app/scrapers/reddit_scraper.py
from .base_scraper import BaseScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time

class RedditScraper(BaseScraper):
    def scrape(self, search_term):
        try:
            # Navigate to Google Trends
            self.driver.get("https://trends.google.com/trends/")
            time.sleep(2)  # Let the page load
            self.driver.save_screenshot('after_init_load.png')  # Save screenshot for debugging

            # Wait for the input box to be present and interactable
            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[jsname='YPqjbf']"))
            )

            # Enter the search term and initiate the search
            time.sleep(1)  # Just to be safe
            search_box.click()  # Click the search box before typing
            search_box.clear()
            search_box.send_keys(search_term)
            # Save screenshot for debugging
            self.driver.save_screenshot('after_input.png')
            search_box.send_keys(Keys.ENTER)

            # After search initiation, wait for cookie consent and click it
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cookieBarConsentButton"))
            )
            cookie_consent_button = self.driver.find_element(By.CSS_SELECTOR, ".cookieBarConsentButton")
            cookie_consent_button.click()
            self.driver.save_screenshot('before_accept.png')  # Save screenshot for debugging

            # Refresh the page and wait for the data to load
            self.driver.refresh()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='A tabular representation of the data in the chart.']"))
            )
            time.sleep(3)  # Additional delay to ensure the data table is loaded
            self.driver.save_screenshot('chart_data_loaded.png')  # Save screenshot for debugging

            # Extract the data from the hidden table
            table_data = self.driver.find_element(By.CSS_SELECTOR, 'div[aria-label="A tabular representation of the data in the chart."] table')
            soup = BeautifulSoup(table_data.get_attribute('outerHTML'), "html.parser")
            rows = soup.find_all('tr')
            data = []
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if cols:
                    data_point = {
                        "date": cols[0].get_text(),
                        "value": cols[1].get_text()
                    }
                    data.append(data_point)

            return {"data": data}

        except Exception as e:
            self.driver.save_screenshot('error.png')  # Save screenshot for debugging
            print(f"An error occurred: {e}")
            return {"error": str(e)}

        finally:
            self.close()




