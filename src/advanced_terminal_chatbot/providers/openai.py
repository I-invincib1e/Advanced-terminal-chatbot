"""OpenAI provider implementation."""

import requests
import json
import logging
from typing import List, Dict, Any, Optional, Generator
from .base import BaseProvider

logger = logging.getLogger(__name__)

class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation with enhanced error handling and optimization."""

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._models_cache: Optional[List[str]] = None
        self._common_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Advanced-Terminal-Chatbot/1.0.0"
        }

    def get_models(self) -> List[str]:
        """Get a list of available models for the provider with caching."""
        if self._models_cache is not None:
            return self._models_cache
            
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self._common_headers,
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            models = data.get('data', [])
            
            # Filter for GPT models and sort by preference
            gpt_models = [
                m.get('id') for m in models 
                if m.get('id') and any(keyword in m.get('id', '').lower() 
                                     for keyword in ['gpt', 'o1'])
            ]
            
            # Sort models by preference (newer models first)
            preferred_order = ['o1', 'gpt-4o', 'gpt-4', 'gpt-3.5']
            
            def sort_key(model_id: str) -> int:
                for i, preferred in enumerate(preferred_order):
                    if preferred in model_id.lower():
                        return i
                return len(preferred_order)
            
            gpt_models.sort(key=sort_key)
            self._models_cache = gpt_models
            return gpt_models
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch OpenAI models: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching OpenAI models: {e}")
            return []

    def validate_api_key(self) -> bool:
        """Validate the API key for the provider."""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self._common_headers,
                timeout=10
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenAI API key validation failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error validating OpenAI API key: {e}")
            return False

    def send_message(self, message: str, model: str, history: List[Dict[str, str]]) -> str:
        """Send a message to the provider and get a response."""
        try:
            if not message.strip():
                return "❌ Empty message provided"
            
            messages = history + [{"role": "user", "content": message}]
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self._common_headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and data['choices']:
                    content = data['choices'][0]['message']['content']
                    return content if content else "❌ Empty response from OpenAI"
                else:
                    return "❌ Invalid response format from OpenAI"
            elif response.status_code == 401:
                return "❌ Invalid OpenAI API key"
            elif response.status_code == 429:
                return "❌ OpenAI rate limit exceeded. Please try again later"
            elif response.status_code == 500:
                return "❌ OpenAI server error. Please try again later"
            else:
                error_msg = self._parse_error_response(response)
                return f"❌ OpenAI API error ({response.status_code}): {error_msg}"
                
        except requests.exceptions.Timeout:
            return "❌ OpenAI request timed out. Please try again"
        except requests.exceptions.RequestException as e:
            return f"❌ Network error communicating with OpenAI: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI send_message: {e}")
            return f"❌ Unexpected error: {str(e)}"

    def stream_response(self, message: str, model: str, history: List[Dict[str, str]]) -> Generator[str, None, None]:
        """Stream a response from the provider."""
        try:
            if not message.strip():
                yield "❌ Empty message provided"
                return
            
            messages = history + [{"role": "user", "content": message}]
            payload = {
                "model": model,
                "messages": messages,
                "stream": True,
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
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
                            if 'choices' in json_data and json_data['choices']:
                                delta = json_data['choices'][0].get('delta', {})
                                if 'content' in delta and delta['content']:
                                    yield delta['content']
                        except json.JSONDecodeError:
                            continue
            else:
                error_msg = self._parse_error_response(response)
                yield f"❌ OpenAI streaming error ({response.status_code}): {error_msg}"
                
        except requests.exceptions.Timeout:
            yield "❌ OpenAI streaming request timed out"
        except requests.exceptions.RequestException as e:
            yield f"❌ Network error during OpenAI streaming: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI stream_response: {e}")
            yield f"❌ Unexpected streaming error: {str(e)}"

    def _parse_error_response(self, response: requests.Response) -> str:
        """Parse error response from OpenAI API."""
        try:
            error_data = response.json()
            if 'error' in error_data:
                error_info = error_data['error']
                return error_info.get('message', 'Unknown error')
            return response.text[:200] + "..." if len(response.text) > 200 else response.text
        except json.JSONDecodeError:
            return response.text[:200] + "..." if len(response.text) > 200 else response.text
