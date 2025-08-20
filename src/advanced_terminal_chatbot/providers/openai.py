"""OpenAI provider implementation."""

import requests
import json
from typing import List, Dict, Any
from .base import BaseProvider

class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation."""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get_models(self) -> List[str]:
        """Get a list of available models for the provider."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                models = data.get('data', [])
                return [m.get('id') for m in models if 'gpt' in m.get('id', '').lower()]
            else:
                return []
        except:
            return []

    def validate_api_key(self) -> bool:
        """Validate the API key for the provider."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def send_message(self, message: str, model: str, history: List[Dict[str, str]]) -> str:
        """Send a message to the provider and get a response."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = history + [{"role": "user", "content": message}]
        payload = {
            "model": model,
            "messages": messages
        }
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return f"❌ OpenAI API error: {response.text}"

    def stream_response(self, message: str, model: str, history: List[Dict[str, str]]) -> Any:
        """Stream a response from the provider."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = history + [{"role": "user", "content": message}]
        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }
        response = requests.post(
            f"{self.base_url}/chat/completions",
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
                        if data == '[DONE]':
                            break
                        try:
                            json_data = json.loads(data)
                            if 'choices' in json_data and len(json_data['choices']) > 0:
                                delta = json_data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    yield delta['content']
                        except json.JSONDecodeError:
                            continue
        else:
            yield f"❌ OpenAI API error: {response.text}"
