import requests
from .base import BaseProvider

class GeminiProvider(BaseProvider):
    def send_request(self, config, user_input, debug_mode):
        gemini_config = config.get("gemini_config", {})
        api_key = gemini_config.get("api_key")
        model_name = gemini_config.get("model_name", "gemini-2.5-flash")
        system_instr = gemini_config.get("system_instruction", "")
        gen_config = gemini_config.get("generation_config", {})
        proxy = config.get("proxy", "")
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": user_input}]}],
            "systemInstruction": {"parts": [{"text": system_instr}]},
            "generationConfig": gen_config
        }
        if debug_mode: print(f"[Debug] Provider: Gemini | Model: {model_name} | Temp: {gen_config.get('temperature')} | Proxy: {proxy if proxy else 'None'}")
        try:
            proxies = {"http": proxy, "https": proxy} if proxy else None
            response = requests.post(api_url, json=payload, proxies=proxies)
            if debug_mode:
                print(f"[Debug] Status: {response.status_code}")
            if response.status_code != 200:
                if response.status_code == 429:
                    print("\n[Error 429] You have exceeded your Gemini API quota.")
                    print("Please check your usage and billing details at aistudio.google.com.")
                else:
                    print(f"\n[Error {response.status_code}]")
                    print(response.text)
                return 1
            data = response.json()
            if "promptFeedback" in data and "blockReason" in data["promptFeedback"]:
                print(f"[Blocked] Reason: {data['promptFeedback']['blockReason']}")
                return 0
            if "candidates" in data and data["candidates"]:
                cand = data["candidates"][0]
                if "content" in cand and "parts" in cand["content"] and cand["content"]["parts"]:
                    print(f"{cand['content']['parts'][0]['text'].strip()}")
                else:
                    print("[No content returned]")
                    if debug_mode: print(data)
            else:
                print("[Error] Invalid response format from Gemini")
                if debug_mode: print(data)
            return 0
        except Exception as e:
            print(f"\n[Connection Error] {e}")
            return 1
