import requests
from typing import Optional

def get_ibm_iam_bearer(api_key: str, timeout: float = 15.0) -> str:
    """
    Exchange an IBM Cloud API key for an IAM access token and return the
    'Bearer <token>' string suitable for Authorization headers.

    Args:
        api_key: Your IBM Cloud API key (from IBM Cloud console).
        timeout: Request timeout in seconds.

    Returns:
        A string like 'Bearer eyJraWQiOi...'

    Raises:
        ValueError: If api_key is empty.
        requests.HTTPError: For non-2xx responses with details attached.
        requests.RequestException: For network/timeout issues.
        KeyError: If the token is missing in the response.
    """
    if not api_key or not api_key.strip():
        raise ValueError("IBM Cloud API key must be provided.")

    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key,
    }

    try:
        resp = requests.post(url, headers=headers, data=data, timeout=timeout)
    except requests.RequestException as e:
        # Network or timeout error
        raise

    if not resp.ok:
        # Attach response text for easier debugging
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        http_err = requests.HTTPError(
            f"IAM token request failed: {resp.status_code} {resp.reason} - {detail}"
        )
        http_err.response = resp  # preserve original response
        raise http_err

    payload = resp.json()
    access_token = payload.get("access_token")
    if not access_token:
        raise KeyError(
            f"access_token missing in IAM response: {payload}"
        )

    return f"Bearer {access_token}"
