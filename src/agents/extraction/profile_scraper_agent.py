# src/agents/extraction/profile_scraper_agent.py
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class ProfileScraperAgent:
    """An agent dedicated to scraping raw content from web pages."""

    def __init__(self):
        # Setup for Selenium (dynamic scraping)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless to avoid opening a browser window
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape_static(self, url: str) -> str:
        """Scrapes content from a static website using Requests and BeautifulSoup."""
        print(f"Agent [Scraper]: Performing static scrape on {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text(separator='\\n', strip=True)
        except requests.RequestException as e:
            print(f"Error during static scraping of {url}: {e}")
            return ""

    def scrape_dynamic(self, url: str) -> str:
        """Scrapes content from a dynamic website using Selenium."""
        print(f"Agent [Scraper]: Performing dynamic scrape on {url}")
        try:
            self.driver.get(url)
            # Wait for the page to load dynamically. Adjust time as needed.
            time.sleep(5)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            return soup.get_text(separator='\\n', strip=True)
        except Exception as e:
            print(f"Error during dynamic scraping of {url}: {e}")
            return ""

    def close(self):
        """Closes the Selenium WebDriver."""
        self.driver.quit()