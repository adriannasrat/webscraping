import os
from datetime import datetime
from flask import Blueprint, request, jsonify

from utils.json_store import read_json, write_json, ensure_dir
from services.scrape_books import scrape_books_for_category
from services.exchange_rate import get_gbp_to_sek_rate

books_bp = Blueprint("books_bp", __name__)

BOOKS_DIR = "data/books"

def today_suffix() -> str:
    """Return yymmdd"""
    return datetime.now().strftime("%y%m%d")

def file_path_for(category: str) -> str:
    """data/books/<category>_<yymmdd>.json"""
    safe = category.strip().lower().replace(" ", "-")
    return os.path.join(BOOKS_DIR, f"{safe}_{today_suffix()}.json")

def load_categories():
    return read_json("data/categories.json", default=[])

def find_category_url(category_slug: str):
    categories = load_categories()
    category_slug = category_slug.strip().lower()
    cat = next((c for c in categories if c.get("slug") == category_slug), None)
    return cat.get("url") if cat else None

@books_bp.get("/<category>")
def get_books(category: str):
    """
    GET /api/v1/books/<category>
    Daily cache:
    - if today's file exists: return it
    - else scrape, save and return
    """
    ensure_dir(BOOKS_DIR)
    path = file_path_for(category)

    cached = read_json(path, default=None)
    if cached is not None:
        return jsonify({
            "category": category,
            "date": today_suffix(),
            "source": "cache",
            "count": len(cached),
            "books": cached
        }), 200

    category_url = find_category_url(category)
    if not category_url:
        return jsonify({
            "error": "Unknown category",
            "hint": "Call GET /api/v1/categories first to see available categories and their slugs"
        }), 404

    # Scrape books
    books = scrape_books_for_category(category_url)

    # Convert GBP -> SEK using scraped rate
    rate = get_gbp_to_sek_rate()
    for b in books:
        b["price_sek"] = round(float(b.get("price_gbp", 0.0)) * rate, 2)

    # Save daily file
    write_json(path, books)

    return jsonify({
        "category": category,
        "date": today_suffix(),
        "source": "scrape",
        "rate_gbp_to_sek": rate,
        "count": len(books),
        "books": books
    }), 200

@books_bp.post("/<category>")
def add_book(category: str):
    """
    POST /api/v1/books/<category>
    Adds a book.
    Body: {id, title, price_gbp, rating, product_url}
    """
    ensure_dir(BOOKS_DIR)
    path = file_path_for(category)
    books = read_json(path, default=[])

    payload = request.get_json(silent=True) or {}
    required = ["id", "title", "price_gbp", "rating", "product_url"]
    missing = [k for k in required if k not in payload]
    if missing:
        return jsonify({"error": "Missing fields", "missing": missing}), 400

    if any(b.get("id") == payload["id"] for b in books):
        return jsonify({"error": "Book already exists", "id": payload["id"]}), 409

    rate = get_gbp_to_sek_rate()
    payload["price_sek"] = round(float(payload.get("price_gbp", 0.0)) * rate, 2)

    books.append(payload)
    write_json(path, books)
    return jsonify(payload), 201

@books_bp.put("/<category>/<book_id>")
def update_book(category: str, book_id: str):
    """
    PUT /api/v1/books/<category>/<book_id>
    Updates a book.
    """
    ensure_dir(BOOKS_DIR)
    path = file_path_for(category)
    books = read_json(path, default=[])

    existing = next((b for b in books if b.get("id") == book_id), None)
    if not existing:
        return jsonify({"error": "Book not found", "id": book_id}), 404

    payload = request.get_json(silent=True) or {}

    for field in ["title", "price_gbp", "rating", "product_url"]:
        if field in payload:
            existing[field] = payload[field]

    # Always recompute SEK price if GBP price is updated
    rate = get_gbp_to_sek_rate()
    existing["price_sek"] = round(float(existing.get("price_gbp", 0.0)) * rate, 2)

    write_json(path, books)
    return jsonify(existing), 200

@books_bp.delete("/<category>/<book_id>")
def delete_book(category: str, book_id: str):
    """
    DELETE /api/v1/books/<category>/<book_id>
    Deletes a book 
    """
    ensure_dir(BOOKS_DIR)
    path = file_path_for(category)
    books = read_json(path, default=[])

    if not any(b.get("id") == book_id for b in books):
        return jsonify({"error": "Book not found", "id": book_id}), 404

    books = [b for b in books if b.get("id") != book_id]
    write_json(path, books)
    return jsonify({"message": "Book deleted", "id": book_id}), 200