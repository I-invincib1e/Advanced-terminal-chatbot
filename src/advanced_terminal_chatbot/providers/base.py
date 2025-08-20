"""Base provider class for all AI providers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseProvider(ABC):
    """Abstract base class for all AI providers."""

    @abstractmethod
    def get_models(self) -> List[str]:
        """Get a list of available models for the provider."""
        pass

    @abstractmethod
    def validate_api_key(self, api_key: str) -> bool:
        """Validate the API key for the provider."""
        pass

    @abstractmethod
    def send_message(self, message: str, model: str, history: List[Dict[str, str]]) -> str:
        """Send a message to the provider and get a response."""
        pass

    @abstractmethod
    def stream_response(self, message: str, model: str, history: List[Dict[str, str]]) -> Any:
        """Stream a response from the provider."""
        pass
