import hashlib

def make_book_id(title: str, price_gbp: float, product_url: str) -> str:
    """
    Deterministic id.
    """
    base = f"{title}|{price_gbp}|{product_url}".encode("utf-8")
    return hashlib.sha1(base).hexdigest()[:12]