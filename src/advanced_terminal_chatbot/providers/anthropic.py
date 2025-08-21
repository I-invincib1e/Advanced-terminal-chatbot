"""Anthropic provider implementation."""

import requests
import json
import logging
from typing import List, Dict, Any, Generator
from .base import BaseProvider

logger = logging.getLogger(__name__)

class AnthropicProvider(BaseProvider):
    """Anthropic provider implementation with enhanced error handling and optimization."""

    def __init__(self, api_key: str, base_url: str = "https://api.anthropic.com/v1"):
        if not api_key:
            raise ValueError("Anthropic API key is required")
            
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.anthropic_models = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022", 
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
        self._common_headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "User-Agent": "Advanced-Terminal-Chatbot/1.0.0"
        }

    def get_models(self) -> List[str]:
        """Get a list of available models for the provider."""
        return self.anthropic_models.copy()

    def validate_api_key(self) -> bool:
        """Validate the API key for the provider."""
        try:
            payload = {
                "model": "claude-3-haiku-20240307",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 10
            }
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self._common_headers,
                json=payload,
                timeout=15
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Anthropic API key validation failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error validating Anthropic API key: {e}")
            return False

    def send_message(self, message: str, model: str, history: List[Dict[str, str]]) -> str:
        """Send a message to the provider and get a response."""
        try:
            if not message.strip():
                return "❌ Empty message provided"
            
            # Filter out system messages and ensure proper alternation
            filtered_history = self._filter_history(history)
            messages = filtered_history + [{"role": "user", "content": message}]
            
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self._common_headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'content' in data and data['content']:
                    content = data['content'][0].get('text', '')
                    return content if content else "❌ Empty response from Anthropic"
                else:
                    return "❌ Invalid response format from Anthropic"
            elif response.status_code == 401:
                return "❌ Invalid Anthropic API key"
            elif response.status_code == 429:
                return "❌ Anthropic rate limit exceeded. Please try again later"
            elif response.status_code == 500:
                return "❌ Anthropic server error. Please try again later"
            else:
                error_msg = self._parse_error_response(response)
                return f"❌ Anthropic API error ({response.status_code}): {error_msg}"
                
        except requests.exceptions.Timeout:
            return "❌ Anthropic request timed out. Please try again"
        except requests.exceptions.RequestException as e:
            return f"❌ Network error communicating with Anthropic: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in Anthropic send_message: {e}")
            return f"❌ Unexpected error: {str(e)}"

    def stream_response(self, message: str, model: str, history: List[Dict[str, str]]) -> Generator[str, None, None]:
        """Stream a response from the provider."""
        try:
            if not message.strip():
                yield "❌ Empty message provided"
                return
            
            # Filter out system messages and ensure proper alternation
            filtered_history = self._filter_history(history)
            messages = filtered_history + [{"role": "user", "content": message}]
            
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.7,
                "stream": True
            }
            
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self._common_headers,
                json=payload,
                stream=True,
                timeout=60
            )
            
            if response.status_code == 200:
                for line in response.iter_lines(decode_unicode=True):
                    if line and line.startswith('data: '):
                        data = line[6:]
                        if data.strip() == '[DONE]':
                            break
                        try:
                            json_data = json.loads(data)
                            if json_data.get('type') == 'content_block_delta':
                                delta = json_data.get('delta', {})
                                if 'text' in delta and delta['text']:
                                    yield delta['text']
                        except json.JSONDecodeError:
                            continue
            else:
                error_msg = self._parse_error_response(response)
                yield f"❌ Anthropic streaming error ({response.status_code}): {error_msg}"
                
        except requests.exceptions.Timeout:
            yield "❌ Anthropic streaming request timed out"
        except requests.exceptions.RequestException as e:
            yield f"❌ Network error during Anthropic streaming: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in Anthropic stream_response: {e}")
            yield f"❌ Unexpected streaming error: {str(e)}"

    def _filter_history(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Filter conversation history to ensure proper alternation and remove system messages."""
        filtered = []
        last_role = None
        
        for msg in history:
            role = msg.get('role')
            content = msg.get('content', '').strip()
            
            # Skip empty messages or system messages
            if not content or role == 'system':
                continue
                
            # Ensure proper alternation (user -> assistant -> user -> ...)
            if role != last_role and role in ['user', 'assistant']:
                filtered.append({"role": role, "content": content})
                last_role = role
        
        return filtered

    def _parse_error_response(self, response: requests.Response) -> str:
        """Parse error response from Anthropic API."""
        try:
            error_data = response.json()
            if 'error' in error_data:
                error_info = error_data['error']
                return error_info.get('message', 'Unknown error')
            return response.text[:200] + "..." if len(response.text) > 200 else response.text
        except json.JSONDecodeError:
            return response.text[:200] + "..." if len(response.text) > 200 else response.text
