from abc import ABC, abstractmethod

import requests


class BaseLookup(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def requires_api_key(self):
        pass

    @property
    @abstractmethod
    def api_key_name(self):
        pass

    @abstractmethod
    def lookup(self, phone_number, api_key=None):
        """
        Perform the lookup.
        Returns: {"success": bool, "data": dict/OrderedDict, "error": str|None}
        """
        pass

    def _make_request(self, url, params=None, headers=None, timeout=10):
        """Shared HTTP GET with standardized error handling."""
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            return {"success": True, "data": response.json(), "error": None}
        except requests.exceptions.ConnectionError:
            return {"success": False, "data": None, "error": "Connection failed. Check your internet."}
        except requests.exceptions.Timeout:
            return {"success": False, "data": None, "error": "Request timed out."}
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else 0
            messages = {
                401: "Invalid API key.",
                403: "Access denied. Check API key permissions.",
                429: "Rate limit exceeded. Try again later.",
            }
            msg = messages.get(status, f"HTTP error {status}")
            return {"success": False, "data": None, "error": msg}
        except requests.exceptions.RequestException as e:
            return {"success": False, "data": None, "error": str(e)}
        except ValueError:
            return {"success": False, "data": None, "error": "Invalid JSON response from API."}
