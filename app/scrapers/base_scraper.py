from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    proxy = "http://pr.oxylabs.io:7777"

    def __init__(self):
        self.driver = self._setup_driver()

    def _setup_driver(self):
        """Sets up the WebDriver with Chrome options."""
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        #chrome_options.add_argument(f"--proxy-server={self.proxy}")

        
        # Set up Chrome logging
        chrome_options.add_experimental_option("prefs", {"loggingPrefs": {"browser": "ALL"}})

        driver = webdriver.Remote(
            command_executor='http://172.18.0.2:4444',
            options=chrome_options
        )
        return driver

    @abstractmethod
    def scrape(self):
        """Abstract method for scraping logic to be implemented by subclasses."""
        pass

    def close(self):
        """Closes the WebDriver."""
        self.driver.quit()
