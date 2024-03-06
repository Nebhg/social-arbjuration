from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

proxy = "http://customer-AkaThePistachio:Kobe2601202o@pr.oxylabs.io:7777"

def set_chrome_options():
    """Sets Chrome options for Selenium."""
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--proxy-server={proxy}")
    return chrome_options

def scrape_website():
    """Scrapes the given URL and returns the IP address."""
    chrome_options = set_chrome_options()
    driver = webdriver.Remote(
        command_executor='http://selenium-server:4444/wd/hub', # Replace 'selenium-server' with the appropriate address of your Selenium hub
        options=chrome_options
    )
    try:
        driver.get("https://httpbin.org/ip")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'token-string'))
        )
        ip_element = driver.find_element(By.CLASS_NAME, 'token-string')
        ip_address = ip_element.text.strip('"')
        return {"IP Address": ip_address}
    except Exception as e:
        driver.save_screenshot('error.png')  # Save a screenshot on error
        print(f"An error occurred: {e}")
        return {"error": str(e)}
    finally:
        driver.quit()
