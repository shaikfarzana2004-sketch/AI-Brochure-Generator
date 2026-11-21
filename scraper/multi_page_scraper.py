
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from scraper.website_scraper import fetch_page, HEADERS
from scraper.page_navigator import (
    extract_internal_links,
    classify_url
)


def scrape_website(url, max_pages=8):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.netloc:
        raise ValueError("Please enter a valid website URL.")

    # Scrape homepage and find its logo
    home = fetch_page(url, include_logo=True)

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    links = extract_internal_links(url, soup)

    selected = []
    seen_categories = set()

    for link in links:

        category = classify_url(link)

        if category and category not in seen_categories:

            selected.append((link, category))
            seen_categories.add(category)

        if len(selected) >= max_pages - 1:
            break

    # Preserve homepage logo data
    pages = [
        {
            "url": home["url"],
            "title": home["title"],
            "category": "Home",
            "content": home["content"],
            "logo_data": home.get("logo_data", "")
        }
    ]

    # Scrape selected internal pages
    for link, category in selected:

        try:

            time.sleep(0.7)

            page = fetch_page(link)

            if len(page["content"]) > 80:

                page["category"] = category
                pages.append(page)

        except (requests.RequestException, ValueError):
            continue

    return pages
