import json
import requests
import pytest
from termai.providers.gemini import GeminiProvider
from termai.providers.openai import OpenAIProvider

class DummyResponse:
    def __init__(self, status_code, json_data, text=None):
        self.status_code = status_code
        self._json = json_data
        self.text = text or json.dumps(json_data)
    def json(self):
        if self._json is None:
            raise json.JSONDecodeError("Expecting value", "", 0)
        return self._json

def test_gemini_success(monkeypatch, capsys):
    sample = {"candidates":[{"content":{"parts":[{"text":"hello gemini"}]}}]}
    
    def fake_post(url, json=None, headers=None, proxies=None, timeout=None):
        # Verify headers for Gemini
        assert headers["x-goog-api-key"] == "test_key"
        assert "key=" not in url
        assert timeout == 30
        return DummyResponse(200, sample)
    
    monkeypatch.setattr(requests, "post", fake_post)
    provider = GeminiProvider()
    config = {
        "request_timeout": 30,
        "gemini_config": {
            "api_key": "test_key",
            "model_name": "gemini-flash",
            "system_instruction": "be helpful"
        }
    }
    ret = provider.send_request(config, "hi", False)
    assert ret == 0
    captured = capsys.readouterr()
    assert "hello gemini" in captured.out

def test_openai_success(monkeypatch, capsys):
    sample = {"choices": [{"message": {"content": "hello openai"}}]}
    
    def fake_post(url, json=None, headers=None, proxies=None, timeout=None):
        assert headers["Authorization"] == "Bearer test_key_openai"
        assert timeout == 15
        return DummyResponse(200, sample)
    
    monkeypatch.setattr(requests, "post", fake_post)
    provider = OpenAIProvider()
    config = {
        "request_timeout": 15,
        "openai_config": {
            "api_key": "test_key_openai",
            "model_name": "gpt-4",
            "system_instruction": "be brief"
        }
    }
    ret = provider.send_request(config, "hi", False)
    assert ret == 0
    captured = capsys.readouterr()
    assert "hello openai" in captured.out

def test_json_decode_error(monkeypatch, capsys):
    def fake_post(url, **kwargs):
        return DummyResponse(200, None, text="Not a JSON")
    
    monkeypatch.setattr(requests, "post", fake_post)
    provider = GeminiProvider()
    config = {"gemini_config": {"api_key": "k"}}
    ret = provider.send_request(config, "hi", False)
    assert ret == 1
    captured = capsys.readouterr()
    assert "Failed to decode JSON" in captured.out

def test_api_error_429(monkeypatch, capsys):
    def fake_post(url, **kwargs):
        return DummyResponse(429, {"error": "quota exceeded"})
    
    monkeypatch.setattr(requests, "post", fake_post)
    provider = GeminiProvider()
    config = {"gemini_config": {"api_key": "k"}}
    ret = provider.send_request(config, "hi", False)
    assert ret == 1
    captured = capsys.readouterr()
    assert "exceeded your Gemini API quota" in captured.out
