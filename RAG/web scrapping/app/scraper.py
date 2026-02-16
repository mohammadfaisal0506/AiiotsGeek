# Scrapes a page. Uses Playwright for JS-heavy pages, trafilatura fallback for readability.
import requests
import trafilatura
from bs4 import BeautifulSoup
from .utils import logger

def fetch_html(url: str, use_playwright: bool = True) -> str:
    html = None
    if use_playwright:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=30000)
                page.wait_for_load_state("networkidle", timeout=30000)
                html = page.content()
                browser.close()
        except Exception as e:
            logger.warning(f"Playwright fetch failed: {e}. Falling back.")
            html = None

    if html:
        return html

    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        return r.text
    except Exception as e:
        logger.warning(f"Requests fetch failed: {e}. Trying trafilatura via URL.")
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return downloaded
        raise
import re

def sanitize_url(url: str) -> str:
    url = url.strip()

    # Remove accidental double schemes like https://https://
    url = re.sub(r'^(https?:\/\/)+', r'https://', url)

    # Add https:// if missing
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    return url
