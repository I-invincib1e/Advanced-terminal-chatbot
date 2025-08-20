"""
Unit tests for provider modules.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from advanced_terminal_chatbot.providers.openai import OpenAIProvider
from advanced_terminal_chatbot.providers.anthropic import AnthropicProvider


class TestOpenAIProvider(unittest.TestCase):
    """Test cases for OpenAIProvider class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_openai_key"
        self.base_url = "https://api.openai.com/v1"
        self.provider = OpenAIProvider(self.api_key, self.base_url)

    def test_initialization(self):
        """Test OpenAIProvider initialization."""
        self.assertEqual(self.provider.api_key, self.api_key)
        self.assertEqual(self.provider.base_url, self.base_url)
        self.assertIsNotNone(self.provider._common_headers)
        self.assertIn("Authorization", self.provider._common_headers)

    def test_initialization_without_api_key(self):
        """Test OpenAIProvider initialization without API key."""
        with self.assertRaises(ValueError):
            OpenAIProvider("", self.base_url)

    @patch('advanced_terminal_chatbot.providers.openai.requests.get')
    def test_get_models_success(self, mock_get):
        """Test successful model fetching."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": "gpt-4o"},
                {"id": "gpt-3.5-turbo"},
                {"id": "text-davinci-003"}  # Should be filtered out
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        models = self.provider.get_models()
        
        self.assertIn("gpt-4o", models)
        self.assertIn("gpt-3.5-turbo", models)
        self.assertNotIn("text-davinci-003", models)

    @patch('advanced_terminal_chatbot.providers.openai.requests.get')
    def test_get_models_cached(self, mock_get):
        """Test model caching."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": "gpt-4o"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # First call
        models1 = self.provider.get_models()
        # Second call should use cache
        models2 = self.provider.get_models()
        
        self.assertEqual(models1, models2)
        mock_get.assert_called_once()  # Should only be called once due to caching

    @patch('advanced_terminal_chatbot.providers.openai.requests.get')
    def test_validate_api_key_success(self, mock_get):
        """Test successful API key validation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.provider.validate_api_key()
        self.assertTrue(result)

    @patch('advanced_terminal_chatbot.providers.openai.requests.get')
    def test_validate_api_key_failure(self, mock_get):
        """Test failed API key validation."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        result = self.provider.validate_api_key()
        self.assertFalse(result)

    @patch('advanced_terminal_chatbot.providers.openai.requests.post')
    def test_send_message_success(self, mock_post):
        """Test successful message sending."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello, how can I help?"}}]
        }
        mock_post.return_value = mock_response

        result = self.provider.send_message("Hello", "gpt-4o", [])
        self.assertEqual(result, "Hello, how can I help?")

    @patch('advanced_terminal_chatbot.providers.openai.requests.post')
    def test_send_message_empty_input(self, mock_post):
        """Test sending empty message."""
        result = self.provider.send_message("", "gpt-4o", [])
        self.assertIn("Empty message", result)
        mock_post.assert_not_called()

    @patch('advanced_terminal_chatbot.providers.openai.requests.post')
    def test_send_message_api_error(self, mock_post):
        """Test API error handling."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"message": "Invalid API key"}
        }
        mock_post.return_value = mock_response

        result = self.provider.send_message("Hello", "gpt-4o", [])
        self.assertIn("Invalid OpenAI API key", result)

    def test_stream_response_empty_input(self):
        """Test streaming with empty input."""
        result = list(self.provider.stream_response("", "gpt-4o", []))
        self.assertEqual(len(result), 1)
        self.assertIn("Empty message", result[0])


class TestAnthropicProvider(unittest.TestCase):
    """Test cases for AnthropicProvider class."""

    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_anthropic_key"
        self.base_url = "https://api.anthropic.com/v1"
        self.provider = AnthropicProvider(self.api_key, self.base_url)

    def test_initialization(self):
        """Test AnthropicProvider initialization."""
        self.assertEqual(self.provider.api_key, self.api_key)
        self.assertEqual(self.provider.base_url, self.base_url)
        self.assertIsNotNone(self.provider._common_headers)
        self.assertIn("x-api-key", self.provider._common_headers)

    def test_initialization_without_api_key(self):
        """Test AnthropicProvider initialization without API key."""
        with self.assertRaises(ValueError):
            AnthropicProvider("", self.base_url)

    def test_get_models(self):
        """Test getting available models."""
        models = self.provider.get_models()
        self.assertIsInstance(models, list)
        self.assertIn("claude-3-5-sonnet-20241022", models)

    @patch('advanced_terminal_chatbot.providers.anthropic.requests.post')
    def test_validate_api_key_success(self, mock_post):
        """Test successful API key validation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = self.provider.validate_api_key()
        self.assertTrue(result)

    @patch('advanced_terminal_chatbot.providers.anthropic.requests.post')
    def test_validate_api_key_failure(self, mock_post):
        """Test failed API key validation."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        result = self.provider.validate_api_key()
        self.assertFalse(result)

    @patch('advanced_terminal_chatbot.providers.anthropic.requests.post')
    def test_send_message_success(self, mock_post):
        """Test successful message sending."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{"text": "Hello! How can I assist you today?"}]
        }
        mock_post.return_value = mock_response

        result = self.provider.send_message("Hello", "claude-3-5-sonnet-20241022", [])
        self.assertEqual(result, "Hello! How can I assist you today?")

    @patch('advanced_terminal_chatbot.providers.anthropic.requests.post')
    def test_send_message_empty_input(self, mock_post):
        """Test sending empty message."""
        result = self.provider.send_message("", "claude-3-5-sonnet-20241022", [])
        self.assertIn("Empty message", result)
        mock_post.assert_not_called()

    def test_filter_history(self):
        """Test conversation history filtering."""
        history = [
            {"role": "system", "content": "You are helpful"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": ""},  # Empty content
            {"role": "user", "content": "How are you?"},
        ]
        
        filtered = self.provider._filter_history(history)
        
        # Should remove system messages and empty content
        # Should maintain proper alternation
        self.assertEqual(len(filtered), 3)
        self.assertEqual(filtered[0]["role"], "user")
        self.assertEqual(filtered[1]["role"], "assistant")
        self.assertEqual(filtered[2]["role"], "user")

    def test_parse_error_response(self):
        """Test error response parsing."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": {"message": "Rate limit exceeded"}
        }
        
        error_msg = self.provider._parse_error_response(mock_response)
        self.assertEqual(error_msg, "Rate limit exceeded")


if __name__ == '__main__':
    unittest.main()
