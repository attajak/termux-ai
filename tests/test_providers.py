import json
import requests
from termai.providers.gemini import GeminiProvider

class DummyResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data
        self.text = json.dumps(json_data)
    def json(self):
        return self._json

def test_gemini_success(monkeypatch, capsys):
    sample = {"candidates":[{"content":{"parts":[{"text":"hello"}]}}]}
    def fake_post(url, json=None, proxies=None):
        return DummyResponse(200, sample)
    monkeypatch.setattr(requests, "post", fake_post)
    provider = GeminiProvider()
    ret = provider.send_request({"gemini_config":{"api_key":"k","model_name":"m","system_instruction":""}}, "hi", False)
    assert ret == 0
    captured = capsys.readouterr()
    assert "hello" in captured.out
