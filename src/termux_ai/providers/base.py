from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    def send_request(self, config, user_input, debug_mode, history=None):
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
            print(
                f"[Debug] Provider: {provider_name} | Model: {model_name} {extra_info}"
            )

    def _stream_response(self, response, provider_name, debug_mode):
        """Robustly processes and prints a streaming response with error handling."""
        full_response = ""
        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    # Logic here depends on the provider, so this method
                    # should be overridden or implemented to handle variations.
                    yield decoded_line
        except Exception as e:
            print(f"\n[Error] Streaming interrupted: {e}")
            return None
        return full_response
