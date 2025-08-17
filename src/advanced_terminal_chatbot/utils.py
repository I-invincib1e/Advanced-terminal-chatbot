"""
Utility functions and configuration management.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv


class ConfigManager:
    """Manages configuration and environment variables."""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.config: Dict[str, Any] = {}
        self._load_environment()
    
    def _load_environment(self) -> None:
        """Load environment variables from .env file if it exists."""
        env_path = Path(self.env_file)
        if env_path.exists():
            load_dotenv(env_path)
            print(f"✅ Loaded environment from {env_path}")
        else:
            print(f"⚠️  No {env_path} file found. Using system environment variables.")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value from environment variables."""
        return os.getenv(key, default)
    
    def get_openai_api_key(self) -> Optional[str]:
        """Get the OpenAI API key from environment variables."""
        return self.get("OPENAI_API_KEY")
    
    def get_anthropic_api_key(self) -> Optional[str]:
        """Get the Anthropic API key from environment variables."""
        return self.get("ANTHROPIC_API_KEY")
    
    def get_openai_base_url(self) -> str:
        """Get the OpenAI API base URL from environment variables."""
        return self.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    def get_anthropic_base_url(self) -> str:
        """Get the Anthropic API base URL from environment variables."""
        return self.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1")
    
    def get_default_model(self) -> Optional[str]:
        """Get the default model from environment variables."""
        return self.get("DEFAULT_MODEL")
    
    def get_default_provider(self) -> Optional[str]:
        """Get the default provider from environment variables."""
        return self.get("DEFAULT_PROVIDER")
    
    def validate_config(self) -> bool:
        """Validate that at least one API key is present."""
        openai_key = self.get_openai_api_key()
        anthropic_key = self.get_anthropic_api_key()

        if not openai_key and not anthropic_key:
            print("❌ No API keys found in environment variables.")
            print("   Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file or environment.")
            return False
        return True

    def get_available_providers(self) -> list:
        """Get list of available providers based on configured API keys."""
        providers = []
        if self.get_openai_api_key():
            providers.append("OpenAI")
        if self.get_anthropic_api_key():
            providers.append("Anthropic")
        return providers

    def get_primary_provider(self) -> Optional[str]:
        """Get the primary provider (first available one)."""
        providers = self.get_available_providers()
        return providers[0] if providers else None

    def require_api_keys(self) -> None:
        """Require at least one API key to be present, otherwise raise an error."""
        if not self.validate_config():
            raise ValueError(
                "No API keys configured. Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY "
                "in your .env file or environment variables."
            )


def create_env_sample() -> None:
    """Create a sample .env file if it doesn't exist."""
    env_sample_path = Path(".env.sample")
    if not env_sample_path.exists():
        sample_content = """# Advanced Terminal Chatbot Configuration
# Copy this file to .env and fill in your values

# Required: At least one API key must be set
# OpenAI API Key (get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API Key (get from https://console.anthropic.com/)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Custom API base URLs
# OPENAI_BASE_URL=https://api.openai.com/v1
# ANTHROPIC_BASE_URL=https://api.anthropic.com/v1

# Optional: Default provider to use
# DEFAULT_PROVIDER=OpenAI

# Optional: Default model to use
# DEFAULT_MODEL=gpt-4o

# Optional: Maximum tokens per response
# MAX_TOKENS=1000

# Optional: Temperature for responses (0.0 to 2.0)
# TEMPERATURE=0.7
"""
        env_sample_path.write_text(sample_content)
        print("✅ Created .env.sample file")
    else:
        print("ℹ️  .env.sample already exists")
