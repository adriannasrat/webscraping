import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils.price_utils import clean_price_text, price_to_float
from utils.ids import make_book_id

def rating_from_class(article_tag) -> str:
    """
    Rating class like: 'star-rating Three'
    Return 'Three', 'Four', etc. If not found: 'Unknown'
    """
    rating_tag = article_tag.select_one(".star-rating")
    if not rating_tag:
        return "Unknown"
    classes = rating_tag.get("class", [])
    for c in classes:
        if c.lower() != "star-rating":
            return c
    return "Unknown"

def scrape_books_for_category(category_url: str):
    """
    Scrape ALL pages for a category.
    Returns list of books with fields: id, title, price_gbp, rating, product_url
    """
    books = []
    next_url = category_url

    while next_url:
        resp = requests.get(next_url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for article in soup.select("article.product_pod"):
            a = article.select_one("h3 a")
            if not a:
                continue

            title = a.get("title", "").strip()
            product_href = a.get("href", "").strip()
            product_url = urljoin(next_url, product_href)

            price_text = article.select_one(".price_color")
            raw_price = price_text.get_text(strip=True) if price_text else ""
            cleaned = clean_price_text(raw_price)
            price_gbp = price_to_float(cleaned)

            rating = rating_from_class(article)

            book_id = make_book_id(title, price_gbp, product_url)

            books.append({
                "id": book_id,
                "title": title,
                "price_gbp": price_gbp,
                "rating": rating,
                "product_url": product_url
            })

        # Pagination
        next_a = soup.select_one("li.next a")
        if next_a and next_a.get("href"):
            next_url = urljoin(next_url, next_a["href"])
        else:
            next_url = None

    return books