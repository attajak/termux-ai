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
        proxy = config.get("proxy", "")
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_instr},
                {"role": "user", "content": user_input}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if debug_mode: print(f"[Debug] Provider: OpenAI | Model: {model_name} | Temp: {temperature} | Proxy: {proxy if proxy else 'None'}")
        try:
            proxies = {"http": proxy, "https": proxy} if proxy else None
            response = requests.post(api_url, headers=headers, json=payload, proxies=proxies)
            if debug_mode:
                print(f"[Debug] Status: {response.status_code}")
            if response.status_code != 200:
                if response.status_code == 429:
                    print("\n[Error 429] You have exceeded your OpenAI API quota.")
                    print("Please check your usage and billing details at platform.openai.com.")
                else:
                    print(f"\n[Error {response.status_code}]")
                    print(response.text)
                return 1
            data = response.json()
            if "choices" in data and data["choices"]:
                message = data["choices"][0].get("message", {})
                content = message.get("content", "")
                if content:
                    print(f"{content.strip()}")
                else:
                    print("[No content returned]")
                    if debug_mode: print(data)
            else:
                print("[Error] Invalid response format from OpenAI")
                if debug_mode: print(data)
            return 0
        except Exception as e:
            print(f"\n[Connection Error] {e}")
            return 1
