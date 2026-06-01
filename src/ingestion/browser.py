# src/ingestion/browser.py

from contextlib import contextmanager
from playwright.sync_api import sync_playwright


@contextmanager
def get_page(headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        try:
            yield page
        finally:
            page.close()
            context.close()
            browser.close()