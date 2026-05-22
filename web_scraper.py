import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time

class WebScraper:
    """Async-ready web scraper with BeautifulSoup."""

    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; PythonBot/1.0)"
        })

    def scrape(self, url: str) -> Dict:
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        time.sleep(self.delay)
        return {
            "url": url,
            "title": soup.title.string if soup.title else "",
            "text": soup.get_text(separator=" ", strip=True),
            "links": [a.get("href") for a in soup.find_all("a", href=True)]
        }

    def scrape_many(self, urls: List[str]) -> List[Dict]:
        return [self.scrape(url) for url in urls]

