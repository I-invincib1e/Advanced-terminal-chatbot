"""Anthropic provider implementation."""

import requests
import json
from typing import List, Dict, Any
from .base import BaseProvider

class AnthropicProvider(BaseProvider):
    """Anthropic provider implementation."""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.anthropic_models = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]

    def get_models(self) -> List[str]:
        """Get a list of available models for the provider."""
        return self.anthropic_models

    def validate_api_key(self) -> bool:
        """Validate the API key for the provider."""
        try:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "claude-3-haiku-20240307",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def send_message(self, message: str, model: str, history: List[Dict[str, str]]) -> str:
        """Send a message to the provider and get a response."""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        messages = history + [{"role": "user", "content": message}]
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 1024
        }
        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data['content'][0]['text']
        else:
            return f"❌ Anthropic API error: {response.text}"

    def stream_response(self, message: str, model: str, history: List[Dict[str, str]]) -> Any:
        """Stream a response from the provider."""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        messages = history + [{"role": "user", "content": message}]
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 1024,
            "stream": True
        }
        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]
                        try:
                            json_data = json.loads(data)
                            if json_data.get('type') == 'content_block_delta' and 'delta' in json_data:
                                delta = json_data['delta']
                                if 'text' in delta:
                                    yield delta['text']
                        except json.JSONDecodeError:
                            continue
        else:
            yield f"❌ Anthropic API error: {response.text}"
