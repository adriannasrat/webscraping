from flask import Flask, jsonify
from myblueprints.categories_bp import categories_bp
from myblueprints.books_bp import books_bp

app = Flask(__name__)

@app.get("/")
def home():
    """Start endpoint: visar info + endpoints."""
    return jsonify({
        "message": "Webscrape Books API (BooksToScrape) - v1",
        "endpoints": {
            "GET /api/v1/categories": "Scrape/load categories (cached in data/categories.json)",
            "POST /api/v1/categories": "Add a category manually",
            "PUT /api/v1/categories/<slug>": "Update a category",
            "DELETE /api/v1/categories/<slug>": "Delete a category",

            "GET /api/v1/books/<category>": "Get books for category (scrape/load from cache file data/books_<category>.json)",
            "POST /api/v1/books/<category>": "Add a book to cache file",
            "PUT /api/v1/books/<category>/<book_id>": "Update a book in cache file",
            "DELETE /api/v1/books/<category>/<book_id>": "Delete a book from cache file"
        }
    }), 200

# Register blueprints for categories and books
app.register_blueprint(categories_bp, url_prefix="/api/v1/categories")
app.register_blueprint(books_bp, url_prefix="/api/v1/books")

if __name__ == "__main__":
    app.run(debug=True)