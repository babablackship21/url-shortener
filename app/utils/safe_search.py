import requests
from fastapi import HTTPException
import logging

from config import GOOGLE_SAFE_BROWSING_API_URL, GOOGLE_SAFE_BROWSING_API_KEY

logger = logging.getLogger(__name__)

def check_url_safety(url: str) -> bool:
    """
    Checks if a given URL is safe using the Google Safe Browsing API.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is safe, False if a threat is found.

    Raises:
        HTTPException: HTTP 503 if the safety service fails or returns invalid data.
    """
    payload = {
        "client": {
            "clientId": "url-shortener-app",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(
            GOOGLE_SAFE_BROWSING_API_URL,
            params={"key": GOOGLE_SAFE_BROWSING_API_KEY},
            json=payload,
            timeout=(3.05, 10),
        )
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict):
            raise ValueError("Expected an object")
        matches = result.get("matches", [])
        if not isinstance(matches, list) or any(not isinstance(item, dict) for item in matches):
            raise ValueError("Expected a list of threat matches")
        return not bool(matches)
    except (requests.RequestException, ValueError) as exc:
        logger.warning("Safety service failed: %s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="URL safety service unavailable.") from None
