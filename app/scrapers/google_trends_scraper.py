# In your app/scrapers/reddit_scraper.py
from .base_scraper import BaseScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time

class GoogleTrendsScraper(BaseScraper):
    def scrape(self, search_term):
        print("Entered func")
        try:
            # Navigate to Google Trends
            self.driver.get("https://trends.google.com/trends/")
            print("Url retrieved")
            time.sleep(2)  # Let the page load
            self.driver.save_screenshot('Test01.png')  # Save screenshot for debugging

            # Wait for the input box to be present and interactable
            search_box = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[jsname='YPqjbf']"))
            )
            print("wait for search box to be interactable")
            # Enter the search term and initiate the search
            time.sleep(1)  # Just to be safe
            search_box.click()  # Click the search box before typing
            search_box.clear()
            search_box.send_keys(search_term)
            self.driver.save_screenshot('Test02.png')  # Save screenshot for debugging
            search_box.send_keys(Keys.ENTER)

            self.driver.save_screenshot('Test03.png')
            # After search initiation, wait for cookie consent and click it
            WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cookieBarConsentButton"))
            )
            print("Cookie accepted")
            cookie_consent_button = self.driver.find_element(By.CSS_SELECTOR, ".cookieBarConsentButton")
            cookie_consent_button.click()
         
             # Navigate to the dropdown and click it to open
            dropdown = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".hierarchy-select"))
            )
            print("Wait for dropdown")
            dropdown.click()
            time.sleep(1)
            self.driver.save_screenshot('Test04.png')  # Save screenshot for debugging

            print("wait for options in dropdown")
            # Depending on the structure after clicking the dropdown, this selector might need to be adjusted.
            worldwide_option = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Worldwide']"))
            )
            # If "Worldwide" is not already selected, click it
            if worldwide_option:
                worldwide_option.click()
                self.driver.save_screenshot('Test05.png')  # Save screenshot for debugging
            
            # Navigate to the dropdown and click it to open
            time_frame_dropdown = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "md-select[aria-label^='Select time period']"))
            )
            print("wait for time frame dropdown")
            if time_frame_dropdown:
                time_frame_dropdown.click()
                self.driver.save_screenshot('Test06.png')

            # Wait for the "Past 30 days" option to become visible and clickable
            # The text "Past 30 days" should be adjusted based on the exact text used in the option within the dropdown
            past_30_days_option = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//md-option/div[normalize-space()='Past 30 days']"))
            )
            print("wait for options in time frame dropdown")
            self.driver.execute_script("arguments[0].click();", past_30_days_option)
            time.sleep(1)
            self.driver.save_screenshot('Test07.png')

            # Wait for the data to load after selecting the time frame
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='A tabular representation of the data in the chart.']"))
            )
            print("wait for tabular data to appear")
            time.sleep(3)  # Additional delay to ensure the data table is loaded

            self.driver.save_screenshot('Test08.png')  # Save screenshot for debugging

            # Refresh the page and wait for the data to load
            self.driver.refresh()
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='A tabular representation of the data in the chart.']"))
            )
            print("Page refreshed and data loaded")
            time.sleep(3)  # Additional delay to ensure the data table is loaded
            self.driver.save_screenshot('Test09.png')  # Save screenshot for debugging
            # Refresh the page and wait for the data to load
            self.driver.refresh()
            time.sleep(3)  # Ensure dynamic content loads
            self.driver.save_screenshot('Test10.png')


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
        



