
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from base64 import b64encode

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CompanyBrochureBot/1.0)"
}

MAX_LOGO_SIZE = 2 * 1024 * 1024


def find_logo_candidates(soup, page_url):
    """Find possible company logo image URLs."""

    candidates = []

    for img in soup.find_all("img"):

        src = (
            img.get("src")
            or img.get("data-src")
            or img.get("data-lazy-src")
        )

        if not src and img.get("srcset"):
            src = img.get("srcset").split(",")[0].strip().split()[0]

        if not src:
            continue

        logo_text = " ".join([
            str(img.get("alt", "")),
            str(img.get("class", "")),
            str(img.get("id", ""))
        ]).lower()

        score = 0

        if "logo" in logo_text:
            score += 100

        if "brand" in logo_text:
            score += 40

        if img.find_parent("header"):
            score += 30

        if img.find_parent("nav"):
            score += 15

        absolute_url = urljoin(page_url, src)

        if urlparse(absolute_url).scheme in ("http", "https"):
            candidates.append((score, absolute_url))

    # Add website favicon as a fallback candidate
    for link in soup.find_all("link", rel=True):

        rel_value = " ".join(link.get("rel", [])).lower()

        if "icon" in rel_value and link.get("href"):

            icon_url = urljoin(page_url, link["href"])

            if urlparse(icon_url).scheme in ("http", "https"):
                candidates.append((5, icon_url))

    # Highest scoring candidates first; remove duplicates
    candidates.sort(key=lambda item: item[0], reverse=True)

    result = []
    seen = set()

    for score, image_url in candidates:

        if image_url not in seen:
            result.append(image_url)
            seen.add(image_url)

    return result[:6]


def download_logo_as_data_url(image_url):
    """Download a public image and convert it to a Base64 data URL."""

    try:

        with requests.get(
            image_url,
            headers=HEADERS,
            timeout=15,
            stream=True
        ) as response:

            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type", ""
            ).split(";")[0].strip().lower()

            if not content_type.startswith("image/"):
                return ""

            content_length = response.headers.get("Content-Length")

            if content_length:
                if int(content_length) > MAX_LOGO_SIZE:
                    return ""

            image_bytes = bytearray()

            for chunk in response.iter_content(chunk_size=65536):

                if not chunk:
                    continue

                image_bytes.extend(chunk)

                if len(image_bytes) > MAX_LOGO_SIZE:
                    return ""

            if not image_bytes:
                return ""

            encoded_image = b64encode(image_bytes).decode("ascii")

            return (
                f"data:{content_type};base64,{encoded_image}"
            )

    except (requests.RequestException, ValueError):
        return ""


def extract_company_logo(soup, page_url):
    """Find and download the best available company logo."""

    candidates = find_logo_candidates(soup, page_url)

    for image_url in candidates:

        logo_data = download_logo_as_data_url(image_url)

        if logo_data:
            return logo_data

    return ""


def fetch_page(url, timeout=20, include_logo=False):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=timeout
    )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

    if "text/html" not in content_type:
        raise ValueError("The URL did not return an HTML page.")

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract logo before removing header and navigation elements
    logo_data = ""

    if include_logo:
        logo_data = extract_company_logo(soup, url)

    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "nav",
        "footer",
        "header"
    ]):
        tag.decompose()

    title = (
        soup.title.get_text(" ", strip=True)
        if soup.title
        else urlparse(url).netloc
    )

    main = (
        soup.find("main")
        or soup.find("article")
        or soup.body
        or soup
    )

    text = " ".join(main.stripped_strings)
    text = " ".join(text.split())

    return {
        "url": url,
        "title": title,
        "content": text[:12000],
        "logo_data": logo_data
    }
