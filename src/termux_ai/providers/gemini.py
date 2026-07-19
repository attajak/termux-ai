import json
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
                api_url,
                headers=headers,
                json=payload,
                proxies=proxies,
                timeout=timeout,
                stream=True,
            )

            if response.status_code != 200:
                if response.status_code == 429:
                    print("\n[Error 429] You have exceeded your Gemini API quota.")
                else:
                    print(f"\n[Error {response.status_code}]")
                    print(response.text)
                return 1

            full_response = ""
            full_json_str = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    full_json_str += decoded_line
            
            # Try to parse the entire response as a single JSON
            try:
                # Gemini streamGenerateContent returns a list of JSON objects, 
                # or a wrapped object. The debug output shows it's a list.
                data_list = json.loads(full_json_str)
                parsed_any = False
                for data in data_list:
                    if "candidates" in data and data["candidates"]:
                        cand = data["candidates"][0]
                        if "content" in cand and "parts" in cand["content"]:
                            text = cand["content"]["parts"][0]["text"]
                            print(text, end="", flush=True)
                            full_response += text
                            parsed_any = True
                print()
            except json.JSONDecodeError as e:
                if debug_mode:
                    print(f"\n[Debug] Stream parse error: {e}")
                print("\n[Error] Failed to decode JSON response from Gemini.")
                return 1

            if not parsed_any:
                print("\n[Error] No content found in Gemini response.")
                return 1

            if history is not None:
                from ..chat import add_to_history

                add_to_history("assistant", full_response)

            return 0
        except Exception as e:
            print(f"\n[Connection Error] {e}")
            return 1
