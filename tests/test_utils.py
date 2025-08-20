"""
Unit tests for utility modules.
"""

import unittest
from unittest.mock import Mock, patch, mock_open
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from advanced_terminal_chatbot.utils import ConfigManager, create_env_sample


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = ConfigManager(load_env=False)  # Don't load actual env

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key',
        'DEFAULT_MODEL': 'gpt-4o',
        'DEFAULT_PROVIDER': 'OpenAI',
        'MAX_TOKENS': '2000',
        'TEMPERATURE': '0.8'
    })
    def test_environment_variable_access(self):
        """Test accessing environment variables."""
        self.assertEqual(self.config.get_openai_api_key(), 'test_openai_key')
        self.assertEqual(self.config.get_anthropic_api_key(), 'test_anthropic_key')
        self.assertEqual(self.config.get_default_model(), 'gpt-4o')
        self.assertEqual(self.config.get_default_provider(), 'OpenAI')
        self.assertEqual(self.config.get('MAX_TOKENS'), '2000')
        self.assertEqual(self.config.get('TEMPERATURE'), '0.8')

    def test_default_values(self):
        """Test default values when environment variables are not set."""
        self.assertEqual(self.config.get_openai_base_url(), "https://api.openai.com/v1")
        self.assertEqual(self.config.get_anthropic_base_url(), "https://api.anthropic.com/v1")
        self.assertIsNone(self.config.get_default_model())
        self.assertIsNone(self.config.get_default_provider())

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_validate_config_with_openai_key(self):
        """Test config validation with OpenAI key."""
        self.assertTrue(self.config.validate_config())

    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    def test_validate_config_with_anthropic_key(self):
        """Test config validation with Anthropic key."""
        self.assertTrue(self.config.validate_config())

    @patch.dict(os.environ, {}, clear=True)
    def test_validate_config_without_keys(self):
        """Test config validation without any keys."""
        self.assertFalse(self.config.validate_config())

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'openai_key', 'ANTHROPIC_API_KEY': 'anthropic_key'})
    def test_get_available_providers(self):
        """Test getting available providers."""
        providers = self.config.get_available_providers()
        self.assertIn('OpenAI', providers)
        self.assertIn('Anthropic', providers)

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_primary_provider(self):
        """Test getting primary provider."""
        provider = self.config.get_primary_provider()
        self.assertEqual(provider, 'OpenAI')

    @patch.dict(os.environ, {}, clear=True)
    def test_require_api_keys_without_keys(self):
        """Test requiring API keys when none are present."""
        with self.assertRaises(ValueError):
            self.config.require_api_keys()

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_require_api_keys_with_key(self):
        """Test requiring API keys when one is present."""
        # Should not raise an exception
        self.config.require_api_keys()

    @patch('advanced_terminal_chatbot.utils.load_dotenv')
    @patch('pathlib.Path.exists')
    def test_load_environment_file_exists(self, mock_exists, mock_load_dotenv):
        """Test loading environment when .env file exists."""
        mock_exists.return_value = True
        
        config = ConfigManager()
        
        mock_load_dotenv.assert_called_once()

    @patch('advanced_terminal_chatbot.utils.load_dotenv')
    @patch('pathlib.Path.exists')
    def test_load_environment_file_not_exists(self, mock_exists, mock_load_dotenv):
        """Test loading environment when .env file doesn't exist."""
        mock_exists.return_value = False
        
        config = ConfigManager()
        
        mock_load_dotenv.assert_not_called()


class TestCreateEnvSample(unittest.TestCase):
    """Test cases for create_env_sample function."""

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.write_text')
    def test_create_env_sample_new_file(self, mock_write_text, mock_exists):
        """Test creating new .env.sample file."""
        mock_exists.return_value = False
        
        create_env_sample()
        
        mock_write_text.assert_called_once()
        args, _ = mock_write_text.call_args
        content = args[0]
        
        # Check that the content contains expected sections
        self.assertIn('OPENAI_API_KEY', content)
        self.assertIn('ANTHROPIC_API_KEY', content)
        self.assertIn('DEFAULT_PROVIDER', content)
        self.assertIn('MAX_TOKENS', content)

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.write_text')
    def test_create_env_sample_existing_file(self, mock_write_text, mock_exists):
        """Test handling existing .env.sample file."""
        mock_exists.return_value = True
        
        create_env_sample()
        
        mock_write_text.assert_not_called()


if __name__ == '__main__':
    unittest.main()
