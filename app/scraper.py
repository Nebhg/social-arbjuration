from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

proxy = "http://pr.oxylabs.io:7777"

def set_chrome_options():
    """Sets Chrome options for Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--proxy-server={proxy}")
    return chrome_options

def scrape_website():
    """Scrapes the given URL and returns the IP address."""
    chrome_options = set_chrome_options()
    driver = webdriver.Remote(
        command_executor='http://172.23.0.2:4444', # Replace 'selenium-server' with the appropriate address of your Selenium hub
        options=chrome_options
    )
    try:
        url="https://stackoverflow.com/questions/67871777/why-am-i-getting-an-empty-body-tag-content-when-trying-to-use-web-scraping-using"
        driver.get(url)
        #Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, "html.parser")
        body_content = soup.find('body').get_text(strip=True)
        return {"HTML Content": body_content}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
    finally:
        driver.quit()
