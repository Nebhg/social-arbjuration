from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class GenericUrlScraper(BaseScraper):

    def scrape(self, url):

        try:
            self.driver.get(url)
            print("Url retrieved")
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Waited for Body")
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            body = soup.find('body')

              # Return the body's HTML as a string
            print(body)
            return {"body": str(body)}
            
        except Exception as e:
            self.driver.save_screenshot('error.png')  # Save screenshot for debugging
            print(f"An error occurred: {e}")
            return {"error": str(e)}
        finally:
            self.close()
