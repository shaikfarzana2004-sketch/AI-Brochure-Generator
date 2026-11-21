from urllib.parse import urljoin, urlparse, urldefrag

KEYWORDS = {
    "About": ("about", "company", "who-we-are", "our-story"),
    "Services": ("service", "solution", "what-we-do"),
    "Products": ("product", "platform", "offering"),
    "Contact": ("contact", "reach-us", "get-in-touch"),
    "Mission and Vision": ("mission", "vision", "values")
}


def extract_internal_links(url, soup):
    base = urlparse(url)
    found = []

    for a in soup.find_all("a", href=True):
        absolute = urldefrag(urljoin(url, a["href"]))[0]
        parsed = urlparse(absolute)

        if (
            parsed.scheme in ("http", "https")
            and parsed.netloc.lower() == base.netloc.lower()
        ):
            if absolute not in found:
                found.append(absolute)

    return found


def classify_url(url):
    path = urlparse(url).path.lower()

    for category, words in KEYWORDS.items():
        if any(word in path for word in words):
            return category

    return None