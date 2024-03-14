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

            # Clear the search box, enter the search term
            
            time.sleep(1)  # Just to be safe
            search_box.click()  # Click the search box before typing
            search_box.clear()
            search_box.send_keys(search_term)
            self.driver.save_screenshot('after_input.png')  # Save screenshot for debugging
            search_box.send_keys(Keys.ENTER)


           # After clicking the search, wait for the results to be visible
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.line-chart"))
            )

            # Additional delay to ensure the data table is loaded in the background
            time.sleep(5)  # Wait for the dynamic content to load

            # Try to locate the hidden data table with the chart information
            try:
                table_data = self.driver.find_element(By.CSS_SELECTOR, 'div[aria-label="A tabular representation of the data in the chart."]')
                if table_data:
                    self.driver.save_screenshot('chart_data_loaded.png')  # Save screenshot for debugging
                    # Extract the table content using BeautifulSoup or directly with Selenium
                    # If using BeautifulSoup, uncomment the next line
                    soup = BeautifulSoup(table_data.get_attribute('innerHTML'), "html.parser")
                    data = soup.find_all('td')  # Your logic to extract data
                    return {"data": data}
            except Exception as e:
                print(f"Failed to find the data table: {e}")
           
            # # Now that the results are loaded, extract the HTML content of the page
            # page_source = self.driver.page_source
            # soup = BeautifulSoup(page_source, "html.parser")

            # # Find the data in the hidden table
            # table = soup.find('div', {'aria-label': 'A tabular representation of the data in the chart.'})
            # if table:
            #     table_data = table.find_all('td')
            #     extracted_data = [td.get_text() for td in table_data]
            #     return {"Extracted Data": extracted_data}
            # else:
            #     return {"Error": "Table with data not found."}

        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.save_screenshot('error.png')  # Save screenshot for debugging
            return {"error": str(e)}

        finally:
            self.close()





