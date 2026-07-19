import json
import requests
from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    def send_request(self, config, user_input, debug_mode, history=None):
        openai_config = config.get("active_config") or config.get("openai_config", {})
        api_key = openai_config.get("api_key")
        model_name = openai_config.get("model_name", "gpt-4o")
        system_instr = openai_config.get("system_instruction", "")
        temperature = openai_config.get("temperature", 0.7)
        max_tokens = openai_config.get("max_tokens", 1024)

        messages = [{"role": "system", "content": system_instr}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_input})

        proxies, timeout = self._get_common_params(config)
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": model_name,
            "messages": messages,
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
            payload["stream"] = True
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
                    print("\n[Error 429] You have exceeded your OpenAI API quota.")
                else:
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
                print("\n[Error] Failed to decode JSON response from OpenAI.")
                return 1

            if history is not None:
                from ..chat import add_to_history

                add_to_history("assistant", full_response)

            return 0
        except requests.exceptions.RequestException as e:
            print(f"\n[Connection Error] {e}")
            return 1
        except Exception as e:
            print(f"\n[Error] {e}")
            return 1
