import re

def clean_price_text(raw: str) -> str:
    """
    Cleans characters in price strings, e.g. 'Â£45.17' -> '£45.17'
    Keeps digits, dot, comma, and currency symbols when possible.
    """
    if raw is None:
        return ""
    # Remove common encoding artifact "Â"
    cleaned = raw.replace("Â", "")
    # Strip everything except digits, dot, comma, and currency symbols
    cleaned = re.sub(r"[^0-9\.,£$€]", "", cleaned)
    return cleaned.strip()

def price_to_float(cleaned: str) -> float:
    """Converts '£45.17' or '45.17' into float 45.17."""
    if not cleaned:
        return 0.0
    # Remove currency signs
    numeric = re.sub(r"[£$€]", "", cleaned)
    # Replace comma with dot if comma is used as decimal separator
    numeric = numeric.replace(",", ".")
    try:
        return float(numeric)
    except ValueError:
        return 0.0