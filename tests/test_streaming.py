import pytest
import json
from unittest.mock import MagicMock, patch
from termux_ai.providers.groq import GroqProvider

def test_groq_streaming_success(capsys):
    provider = GroqProvider()
    config = {"groq_config": {"api_key": "test"}}
    
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_lines.return_value = [
        b'data: {"choices": [{"delta": {"content": "Hello"}}]}',
        b'data: {"choices": [{"delta": {"content": " world"}}]}',
        b'data: [DONE]'
    ]
    
    with patch('requests.post', return_value=mock_response):
        ret = provider.send_request(config, "hi", False)
        
    assert ret == 0
    captured = capsys.readouterr()
    assert "Hello world" in captured.out

def test_groq_streaming_error(capsys):
    provider = GroqProvider()
    config = {"groq_config": {"api_key": "test"}}
    
    # Mock response with error
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    
    with patch('requests.post', return_value=mock_response):
        ret = provider.send_request(config, "hi", False)
        
    assert ret == 1
    captured = capsys.readouterr()
    assert "Error 500" in captured.out
