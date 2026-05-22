import requests
from typing import Optional, Dict, Any
import time

class APIClient:
    """Generic REST API client with auth, retry and rate limiting."""

    def __init__(self, base_url: str, api_key: Optional[str] = None,
                 max_retries: int = 3, rate_limit: float = 1.0):
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.rate_limit = rate_limit
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get(self, endpoint: str, params: Dict = {}) -> Any:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Dict = {}) -> Any:
        return self._request("POST", endpoint, json=data)

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip(/)}"
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                time.sleep(self.rate_limit)
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)

