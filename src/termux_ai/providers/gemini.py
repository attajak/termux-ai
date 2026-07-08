import requests
from .base import BaseProvider


class GeminiProvider(BaseProvider):
    def send_request(self, config, user_input, debug_mode, history=None):
        gemini_config = config.get("active_config") or config.get("gemini_config", {})
        api_key = gemini_config.get("api_key")
        model_name = gemini_config.get("model_name", "gemini-2.5-flash")
        system_instr = gemini_config.get("system_instruction", "")
        gen_config = gemini_config.get("generation_config", {})

        # Gemini history format differs (contents list), for simplicity map only user/assistant
        contents = [{"parts": [{"text": system_instr}]}]
        if history:
            for item in history:
                role = "user" if item["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": item["content"]}]})
        contents.append({"role": "user", "parts": [{"text": user_input}]})

        proxies, timeout = self._get_common_params(config)
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:streamGenerateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}

        payload = {
            "contents": contents,
            "generationConfig": gen_config,
        }

        self._handle_debug(
            debug_mode,
            "Gemini",
            model_name,
            f"| Temp: {gen_config.get('temperature')} | Timeout: {timeout}s",
        )

        try:
            response = requests.post(
                api_url, headers=headers, json=payload, proxies=proxies, timeout=timeout, stream=True
            )

            if response.status_code != 200:
                if response.status_code == 429:
                    print("\n[Error 429] You have exceeded your Gemini API quota.")
                else:
                    print(f"\n[Error {response.status_code}]")
                    print(response.text)
                return 1

            full_response = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('{'):
                        try:
                            json_str = decoded_line.lstrip(', ')
                            data = json.loads(json_str)
                            if "candidates" in data and data["candidates"]:
                                cand = data["candidates"][0]
                                if "content" in cand and "parts" in cand["content"]:
                                    text = cand["content"]["parts"][0]["text"]
                                    print(text, end='', flush=True)
                                    full_response += text
                        except (json.JSONDecodeError, KeyError):
                            continue
            print()
            
            if history is not None:
                from ..chat import add_to_history
                add_to_history("assistant", full_response)
                
            return 0
        except Exception as e:
            print(f"\n[Connection Error] {e}")
            return 1
