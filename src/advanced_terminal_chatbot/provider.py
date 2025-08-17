"""
Provider management for different AI services.
"""

import requests
from typing import List, Dict, Any, Optional
from .utils import ConfigManager


class ProviderManager:
    """Manages different AI providers and their models."""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        
        # OpenAI models
        self.openai_models = [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo"
        ]
        
        # Anthropic models
        self.anthropic_models = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
        
        # Provider models mapping
        self.provider_models = {
            "OpenAI": self.openai_models,
            "Anthropic": self.anthropic_models
        }
    
    def get_providers(self) -> List[str]:
        """Get list of available providers based on configured API keys."""
        return self.config.get_available_providers()
    
    def get_provider_models(self, provider: str) -> List[str]:
        """Get models for a specific provider."""
        return self.provider_models.get(provider, [])
    
    def fetch_openai_models(self) -> List[Dict[str, Any]]:
        """Fetch available models from OpenAI API."""
        api_key = self.config.get_openai_api_key()
        if not api_key:
            raise ValueError("OpenAI API key not configured")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.config.get_openai_base_url()}/models", 
                headers=headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('data', [])
                
                if models:
                    # Filter for chat models and limit to first 10
                    chat_models = [m for m in models if 'gpt' in m.get('id', '').lower()]
                    limited_models = chat_models[:10]
                    return limited_models
                else:
                    return []
            else:
                raise requests.HTTPError(
                    f"Failed to fetch OpenAI models. Status: {response.status_code}"
                )
                
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error fetching OpenAI models: {e}")
    
    def fetch_anthropic_models(self) -> List[Dict[str, Any]]:
        """Fetch available models from Anthropic API."""
        api_key = self.config.get_anthropic_api_key()
        if not api_key:
            raise ValueError("Anthropic API key not configured")
        
        # Anthropic doesn't have a models endpoint, so we return our predefined list
        return [{"id": model, "name": model} for model in self.anthropic_models]
    
    def validate_model(self, model: str, provider: str) -> bool:
        """Validate if a model exists for the specified provider."""
        if provider == "OpenAI":
            return model in self.openai_models
        elif provider == "Anthropic":
            return model in self.anthropic_models
        return False
    
    def get_model_provider(self, model: str) -> Optional[str]:
        """Get the provider for a specific model."""
        if model in self.openai_models:
            return "OpenAI"
        elif model in self.anthropic_models:
            return "Anthropic"
        return None
    
    def display_providers(self) -> None:
        """Display available providers with model counts."""
        print("🏢 PROVIDER SELECTION")
        print("─" * 50)
        
        available_providers = self.get_providers()
        if not available_providers:
            print("❌ No API keys configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")
            return
        
        for i, provider in enumerate(available_providers, 1):
            model_count = len(self.get_provider_models(provider))
            print(f"  {i}. {provider} ({model_count} models available)")
        
        print("─" * 50)
    
    def select_provider(self) -> str:
        """Interactive provider selection."""
        available_providers = self.get_providers()
        if not available_providers:
            raise ValueError("No providers available. Please configure API keys.")
        
        if len(available_providers) == 1:
            provider = available_providers[0]
            print(f"✅ Using available provider: {provider}")
            return provider
        
        print("\n🤖 Available AI Providers:")
        for i, provider in enumerate(available_providers, 1):
            print(f"  {i}. {provider}")
        
        while True:
            try:
                choice = input(f"\n📝 Select provider (1-{len(available_providers)}): ").strip()
                if choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(available_providers):
                        selected_provider = available_providers[index]
                        print(f"✅ Selected: {selected_provider}")
                        return selected_provider
                    else:
                        print(f"❌ Please enter a number between 1 and {len(available_providers)}")
                else:
                    print("❌ Please enter a valid number")
            except (ValueError, KeyboardInterrupt):
                print("\n❌ Invalid selection. Please try again.")
    
    def select_provider_model(self, provider: str) -> str:
        """Select a model from a specific provider."""
        print(f"🤖 {provider.upper()} MODELS")
        print("─" * 50)
        
        models = self.get_provider_models(provider)
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
        
        print("─" * 50)
        
        while True:
            try:
                choice = input(f"🎯 Select model (1-{len(models)}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(models):
                    selected_model = models[choice_num - 1]
                    print(f"✅ Selected model: {selected_model}")
                    print()
                    return selected_model
                else:
                    print(f"❌ Please enter a number between 1 and {len(models)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
    
    def fetch_api_models(self, provider: str) -> List[Dict[str, Any]]:
        """Fetch models from the specified provider's API."""
        if provider == "OpenAI":
            return self.fetch_openai_models()
        elif provider == "Anthropic":
            return self.fetch_anthropic_models()
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def select_api_model(self, models: List[Dict[str, Any]]) -> str:
        """Select a model from API-fetched models."""
        print("🤖 API MODELS")
        print("─" * 50)
        
        for i, model in enumerate(models, 1):
            model_id = model.get('id', 'Unknown')
            model_name = model.get('name', model_id)
            print(f"  {i}. {model_name}")
        
        print("─" * 50)
        
        while True:
            try:
                choice = input(f"🎯 Select model (1-{len(models)}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(models):
                    selected_model = models[choice_num - 1]
                    model_id = selected_model.get('id')
                    print(f"✅ Selected model: {model_id}")
                    print()
                    return model_id
                else:
                    print(f"❌ Please enter a number between 1 and {len(models)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
