import json
import requests
from .base import BaseProvider


class MistralProvider(BaseProvider):
    def send_request(self, config, user_input, debug_mode, history=None):
        mistral_config = config.get("active_config") or config.get("mistral_config", {})
        api_key = mistral_config.get("api_key")
        model_name = mistral_config.get("model_name", "mistral-small-latest")
        system_instr = mistral_config.get("system_instruction", "")

        messages = [{"role": "system", "content": system_instr}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_input})

        proxies, timeout = self._get_common_params(config)
        api_url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": mistral_config.get("temperature", 0.7),
            "stream": True,
        }

        self._handle_debug(debug_mode, "Mistral", model_name)

        try:
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                proxies=proxies,
                timeout=timeout,
                stream=True,
            )

            if response.status_code != 200:
                print(f"\n[Error {response.status_code}]")
                print(response.text)
                return 1

            full_response = ""
            parsed_any = False
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data: "):
                        data_str = decoded_line[6:]
                        if data_str == "[DONE]":
                            parsed_any = True
                            break
                        try:
                            data = json.loads(data_str)
                            content = data["choices"][0]["delta"].get("content")
                            if content:
                                print(content, end="", flush=True)
                                full_response += content
                                parsed_any = True
                        except (json.JSONDecodeError, KeyError, Exception) as e:
                            if debug_mode:
                                print(f"\n[Debug] Stream parse error: {e}")
                            continue
            print()  # Newline after streaming complete

            if not parsed_any:
                print("\n[Error] Failed to decode JSON response from Mistral.")
                return 1

            if history is not None:
                from ..chat import add_to_history

                add_to_history("assistant", full_response)

            return 0
        except Exception as e:
            print(f"\n[Connection Error] {e}")
            return 1
