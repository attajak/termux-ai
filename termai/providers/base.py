import requests
import json
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def send_request(self, config, user_input, debug_mode):
        """Send a request to the AI model."""
        pass

    def _get_common_params(self, config):
        """Extract common parameters like proxy and timeout."""
        proxy = config.get("proxy", "")
        timeout = config.get("request_timeout", 30)
        proxies = {"http": proxy, "https": proxy} if proxy else None
        return proxies, timeout

    def _handle_debug(self, debug_mode, provider_name, model_name, extra_info=""):
        """Centralized debug logging."""
        if debug_mode:
            print(f"[Debug] Provider: {provider_name} | Model: {model_name} {extra_info}")

    def _safe_json_decode(self, response, provider_name, debug_mode):
        """Safely decode JSON response with error handling."""
        try:
            return response.json()
        except json.JSONDecodeError:
            print(f"\n[Error] Failed to decode JSON response from {provider_name}.")
            if debug_mode:
                print(f"[Debug] Status Code: {response.status_code}")
                print(f"[Debug] Raw Response: {response.text}")
            return None
