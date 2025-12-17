"""
Web Fetcher Module
Handles browser automation using Selenium WebDriver to fetch web pages.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_driver():
    """
    Initialize and configure a Chrome WebDriver instance.
    
    Returns:
        WebDriver: Configured Chrome WebDriver with headless disabled for visibility
    """
    options = Options()
    # options.add_argument("--headless")  # Commented out to see browser window
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    # Set timeout to prevent hanging on slow sites
    driver.set_page_load_timeout(10)
    return driver

def fetch_page(driver, url, wait=2):
    """
    Fetch a web page using Selenium WebDriver.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        url (str): URL to fetch
        wait (int): Wait time in seconds after page loads
        
    Returns:
        tuple: (page_source HTML string, error message if any)
    """
    try:
        driver.get(url)
        time.sleep(wait)  # Wait for JavaScript to execute
        return driver.page_source, None
    except Exception as e:
        # Return error message if page fails to load
        return None, str(e)