import requests
from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    def send_request(self, config, user_input, debug_mode):
        openai_config = config.get("openai_config", {})
        api_key = openai_config.get("api_key")
        model_name = openai_config.get("model_name", "gpt-4o")
        system_instr = openai_config.get("system_instruction", "")
        temperature = openai_config.get("temperature", 0.7)
        max_tokens = openai_config.get("max_tokens", 1024)

        proxies, timeout = self._get_common_params(config)
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_instr},
                {"role": "user", "content": user_input},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        self._handle_debug(
            debug_mode,
            "OpenAI",
            model_name,
            f"| Temp: {temperature} | Timeout: {timeout}s",
        )

        try:
            response = requests.post(
                api_url, headers=headers, json=payload, proxies=proxies, timeout=timeout
            )

            if response.status_code != 200:
                if response.status_code == 429:
                    print("\n[Error 429] You have exceeded your OpenAI API quota.")
                else:
                    print(f"\n[Error {response.status_code}]")
                    print(response.text)
                return 1

            data = self._safe_json_decode(response, "OpenAI", debug_mode)
            if not data:
                return 1

            if "choices" in data and data["choices"]:
                message = data["choices"][0].get("message", {})
                content = message.get("content", "")
                if content:
                    print(f"{content.strip()}")
                else:
                    print("[No content returned]")
            else:
                print("[Error] Invalid response format from OpenAI")
                if debug_mode:
                    print(data)
            return 0
        except Exception as e:
            print(f"\n[Connection Error] {e}")
            return 1
