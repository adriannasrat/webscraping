import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

def scrape_categories():
    """
    Scrapes categories from URL.
    Returns list of dicts: {slug, name, url}
    """
    resp = requests.get(BASE_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # We grab links that include "/category/books/"
    links = soup.select("div.side_categories ul li ul li a")

    categories = []
    for a in links:
        name = a.get_text(strip=True)
        href = a.get("href", "").strip()
        if not href:
            continue

        full_url = urljoin(BASE_URL, href)

        # slug example: travel_2 -> travel
        slug = (
            name.lower()
            .replace("&", "and")
            .replace("/", "-")
            .replace(" ", "-")
        )

        categories.append({
            "slug": slug,
            "name": name,
            "url": full_url
        })

    return categories