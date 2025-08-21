"""
Unit tests for provider manager module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from advanced_terminal_chatbot.provider import ProviderManager
from advanced_terminal_chatbot.utils import ConfigManager


class TestProviderManager(unittest.TestCase):
    """Test cases for ProviderManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_config = Mock(spec=ConfigManager)
        self.mock_config.get_openai_api_key.return_value = "test_openai_key"
        self.mock_config.get_anthropic_api_key.return_value = "test_anthropic_key"
        self.mock_config.get_openai_base_url.return_value = "https://api.openai.com/v1"
        self.mock_config.get_anthropic_base_url.return_value = "https://api.anthropic.com/v1"
        
        self.provider_manager = ProviderManager(self.mock_config)

    def test_initialization(self):
        """Test ProviderManager initialization."""
        self.assertEqual(len(self.provider_manager.providers), 2)
        self.assertIn("OpenAI", self.provider_manager.providers)
        self.assertIn("Anthropic", self.provider_manager.providers)

    def test_initialization_openai_only(self):
        """Test initialization with only OpenAI key."""
        config = Mock(spec=ConfigManager)
        config.get_openai_api_key.return_value = "test_key"
        config.get_anthropic_api_key.return_value = None
        config.get_openai_base_url.return_value = "https://api.openai.com/v1"
        config.get_anthropic_base_url.return_value = "https://api.anthropic.com/v1"
        
        pm = ProviderManager(config)
        self.assertEqual(len(pm.providers), 1)
        self.assertIn("OpenAI", pm.providers)
        self.assertNotIn("Anthropic", pm.providers)

    def test_get_providers(self):
        """Test getting list of providers."""
        providers = self.provider_manager.get_providers()
        self.assertIsInstance(providers, list)
        self.assertIn("OpenAI", providers)
        self.assertIn("Anthropic", providers)

    def test_get_provider_existing(self):
        """Test getting existing provider."""
        provider = self.provider_manager.get_provider("OpenAI")
        self.assertIsNotNone(provider)

    def test_get_provider_non_existing(self):
        """Test getting non-existing provider."""
        provider = self.provider_manager.get_provider("NonExistent")
        self.assertIsNone(provider)

    @patch('advanced_terminal_chatbot.providers.openai.OpenAIProvider.validate_api_key')
    @patch('advanced_terminal_chatbot.providers.anthropic.AnthropicProvider.validate_api_key')
    def test_validate_api_keys(self, mock_anthropic_validate, mock_openai_validate):
        """Test API key validation."""
        mock_openai_validate.return_value = True
        mock_anthropic_validate.return_value = False
        
        results = self.provider_manager.validate_api_keys()
        
        self.assertTrue(results["OpenAI"])
        self.assertFalse(results["Anthropic"])

    @patch('advanced_terminal_chatbot.providers.openai.OpenAIProvider.get_models')
    def test_fetch_api_models_with_defaults(self, mock_get_models):
        """Test fetching API models with common models filter."""
        mock_get_models.return_value = ["gpt-4o", "gpt-3.5-turbo", "text-davinci-003"]
        
        models = self.provider_manager.fetch_api_models("OpenAI", use_defaults=True)
        
        # Should return common models that are available
        self.assertIn("gpt-4o", models)
        self.assertIn("gpt-3.5-turbo", models)

    @patch('advanced_terminal_chatbot.providers.openai.OpenAIProvider.get_models')
    def test_fetch_api_models_all(self, mock_get_models):
        """Test fetching all API models."""
        expected_models = ["gpt-4o", "gpt-3.5-turbo", "text-davinci-003"]
        mock_get_models.return_value = expected_models
        
        models = self.provider_manager.fetch_api_models("OpenAI", use_defaults=False)
        
        self.assertEqual(models, expected_models)

    def test_get_default_model(self):
        """Test getting default model for provider."""
        default_model = self.provider_manager.get_default_model("OpenAI")
        self.assertEqual(default_model, "gpt-4o")
        
        default_model = self.provider_manager.get_default_model("Anthropic")
        self.assertEqual(default_model, "claude-3-5-sonnet-20241022")

    def test_get_default_model_invalid_provider(self):
        """Test getting default model for invalid provider."""
        default_model = self.provider_manager.get_default_model("InvalidProvider")
        self.assertIsNone(default_model)

    def test_get_common_models(self):
        """Test getting common models for provider."""
        common_models = self.provider_manager.get_common_models("OpenAI")
        self.assertIsInstance(common_models, list)
        self.assertIn("gpt-4o", common_models)

    def test_get_common_models_invalid_provider(self):
        """Test getting common models for invalid provider."""
        common_models = self.provider_manager.get_common_models("InvalidProvider")
        self.assertEqual(common_models, [])

    @patch('builtins.input')
    def test_select_provider_from_list_single(self, mock_input):
        """Test selecting provider from list with single option."""
        providers = ["OpenAI"]
        
        selected = self.provider_manager.select_provider_from_list(providers)
        
        self.assertEqual(selected, "OpenAI")
        mock_input.assert_not_called()  # Should auto-select

    @patch('builtins.input')
    def test_select_provider_from_list_multiple(self, mock_input):
        """Test selecting provider from list with multiple options."""
        mock_input.return_value = "1"
        providers = ["OpenAI", "Anthropic"]
        
        selected = self.provider_manager.select_provider_from_list(providers)
        
        self.assertEqual(selected, "OpenAI")
        mock_input.assert_called_once()

    @patch('builtins.input')
    def test_select_api_model(self, mock_input):
        """Test selecting API model."""
        mock_input.return_value = "2"
        models = ["gpt-4o", "gpt-3.5-turbo", "claude-3-5-sonnet-20241022"]
        
        selected = self.provider_manager.select_api_model(models)
        
        self.assertEqual(selected, "gpt-3.5-turbo")

    @patch('builtins.input')
    def test_select_api_model_invalid_input(self, mock_input):
        """Test selecting API model with invalid input then valid."""
        mock_input.side_effect = ["invalid", "0", "1"]
        models = ["gpt-4o", "gpt-3.5-turbo"]
        
        selected = self.provider_manager.select_api_model(models)
        
        self.assertEqual(selected, "gpt-4o")
        self.assertEqual(mock_input.call_count, 3)


if __name__ == '__main__':
    unittest.main()
