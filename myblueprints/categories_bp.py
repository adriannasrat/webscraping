from flask import Blueprint, request, jsonify
from utils.json_store import read_json, write_json
from services.scrape_categories import scrape_categories

categories_bp = Blueprint("categories_bp", __name__)

CATEGORIES_PATH = "data/categories.json"

@categories_bp.get("/")
def get_categories():
    """
    GET /api/v1/categories
    - If categories.json exists: return it
    - If not scrape and create it
    """
    categories = read_json(CATEGORIES_PATH, default=None)
    if categories is None or not isinstance(categories, list) or len(categories) == 0:
        categories = scrape_categories()
        write_json(CATEGORIES_PATH, categories)
    return jsonify(categories), 200

@categories_bp.post("/")
def add_category():
    """
    POST /api/v1/categories
    Adds a category manually to the categories.json file.
    """
    payload = request.get_json(silent=True) or {}
    slug = str(payload.get("slug", "")).strip().lower()
    name = str(payload.get("name", "")).strip()
    url = str(payload.get("url", "")).strip()

    if not slug or not name or not url:
        return jsonify({"error": "slug, name and url are required"}), 400

    categories = read_json(CATEGORIES_PATH, default=[])
    if any(c.get("slug") == slug for c in categories):
        return jsonify({"error": "Category already exists", "slug": slug}), 409

    new_cat = {"slug": slug, "name": name, "url": url}
    categories.append(new_cat)
    write_json(CATEGORIES_PATH, categories)
    return jsonify(new_cat), 201

@categories_bp.put("/<slug>")
def update_category(slug: str):
    """
    PUT /api/v1/categories/<slug>
    Updates a category.
    """
    payload = request.get_json(silent=True) or {}
    categories = read_json(CATEGORIES_PATH, default=[])

    slug = slug.strip().lower()
    existing = next((c for c in categories if c.get("slug") == slug), None)
    if not existing:
        return jsonify({"error": "Category not found", "slug": slug}), 404

    # Update allowed fields
    if "name" in payload:
        existing["name"] = str(payload["name"]).strip()
    if "url" in payload:
        existing["url"] = str(payload["url"]).strip()

    write_json(CATEGORIES_PATH, categories)
    return jsonify(existing), 200

@categories_bp.delete("/<slug>")
def delete_category(slug: str):
    """
    DELETE /api/v1/categories/<slug>
    Deletes a category.
    """
    categories = read_json(CATEGORIES_PATH, default=[])
    slug = slug.strip().lower()

    existing = next((c for c in categories if c.get("slug") == slug), None)
    if not existing:
        return jsonify({"error": "Category not found", "slug": slug}), 404

    categories = [c for c in categories if c.get("slug") != slug]
    write_json(CATEGORIES_PATH, categories)
    return jsonify({"message": "Category deleted", "slug": slug}), 200