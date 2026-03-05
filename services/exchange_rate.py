import os
import re
import requests
from bs4 import BeautifulSoup

def get_gbp_to_sek_rate() -> float:
    """
    Scrapes GBP->SEK rate from page.
    If anything goes wrong, returns fallback rate from env or 13.0.
    """
    url = os.getenv("EXCHANGE_URL", "").strip()

    # Default fallback rate if env var is not set or empty
    fallback_rate = float(os.getenv("GBP_SEK_FALLBACK", "13.0"))

    if not url:
        return fallback_rate

    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        text = soup.get_text(" ", strip=True)
        # Find something that looks like 12.34 or 12,34
        m = re.search(r"(\d{1,2}[.,]\d{1,4})", text)
        if not m:
            return fallback_rate

        rate_str = m.group(1).replace(",", ".")
        return float(rate_str)
    except Exception:
        return fallback_rate