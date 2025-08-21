"""Provider management for different AI services."""

from typing import List, Dict, Any, Optional
from .utils import ConfigManager
from .providers.base import BaseProvider
from .providers.openai import OpenAIProvider
from .providers.anthropic import AnthropicProvider

class ProviderManager:
    """Manages different AI providers and their models."""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.providers: Dict[str, BaseProvider] = {}
        self._initialize_providers()
        
        # Define default models for each provider
        self.default_models = {
            "openai": "gpt-4o",
            "anthropic": "claude-3-5-sonnet-20241022"
        }
        
        # Define commonly used models to filter the overwhelming list
        self.common_models = {
            "openai": [
                "gpt-4o",
                "gpt-4o-mini", 
                "gpt-4-turbo",
                "gpt-4",
                "gpt-3.5-turbo",
                "o1-preview",
                "o1-mini"
            ],
            "anthropic": [
                "claude-3-5-sonnet-20241022",
                "claude-3-5-haiku-20241022",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
        }

    def _initialize_providers(self):
        """Initialize available providers based on configuration."""
        if self.config.get_openai_api_key():
            self.providers["OpenAI"] = OpenAIProvider(
                api_key=self.config.get_openai_api_key(),
                base_url=self.config.get_openai_base_url()
            )
        if self.config.get_anthropic_api_key():
            self.providers["Anthropic"] = AnthropicProvider(
                api_key=self.config.get_anthropic_api_key(),
                base_url=self.config.get_anthropic_base_url()
            )

    def get_providers(self) -> List[str]:
        """Get list of available providers."""
        return list(self.providers.keys())

    def get_provider(self, name: str) -> Optional[BaseProvider]:
        """Get a provider instance by name."""
        return self.providers.get(name)

    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate API keys for all available providers."""
        validation_results = {}
        for name, provider in self.providers.items():
            validation_results[name] = provider.validate_api_key()
        return validation_results

    def select_provider_from_list(self, providers: List[str]) -> str:
        """Select a provider from a given list of providers."""
        if len(providers) == 1:
            provider = providers[0]
            print(f"✅ Using available provider: {provider}")
            return provider

        print("\n🤖 Available AI Providers:")
        for i, provider in enumerate(providers, 1):
            print(f"  {i}. {provider}")

        while True:
            try:
                choice = input(f"\n📝 Select provider (1-{len(providers)}): ").strip()
                if choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(providers):
                        selected_provider = providers[index]
                        print(f"✅ Selected: {selected_provider}")
                        return selected_provider
                    else:
                        print(f"❌ Please enter a number between 1 and {len(providers)}")
                else:
                    print("❌ Please enter a valid number")
            except (ValueError, KeyboardInterrupt):
                print("\n❌ Invalid selection. Please try again.")

    def fetch_api_models(self, provider_name: str, use_defaults: bool = True) -> List[str]:
        """Fetch models from the specified provider's API."""
        provider = self.get_provider(provider_name)
        if not provider:
            return []
            
        provider_key = provider_name.lower()
        
        if use_defaults and provider_key in self.common_models:
            # Return filtered common models instead of all available models
            all_models = provider.get_models()
            common_models = self.common_models[provider_key]
            
            # Filter to only include common models that are actually available
            available_common_models = [model for model in common_models if model in all_models]
            
            if available_common_models:
                return available_common_models
            else:
                # Fallback to all models if none of the common ones are available
                return all_models
        else:
            # Return all models when use_defaults is False
            return provider.get_models()
    
    def get_default_model(self, provider_name: str) -> Optional[str]:
        """Get the default model for a provider."""
        provider_key = provider_name.lower()
        return self.default_models.get(provider_key)
    
    def get_common_models(self, provider_name: str) -> List[str]:
        """Get the list of common models for a provider."""
        provider_key = provider_name.lower()
        return self.common_models.get(provider_key, [])

    def select_api_model(self, models: List[str]) -> str:
        """Select a model from API-fetched models."""
        print("🤖 API MODELS")
        print("─" * 50)

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
