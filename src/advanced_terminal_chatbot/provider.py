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

    def fetch_api_models(self, provider_name: str) -> List[str]:
        """Fetch models from the specified provider's API."""
        provider = self.get_provider(provider_name)
        if provider:
            return provider.get_models()
        return []

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
