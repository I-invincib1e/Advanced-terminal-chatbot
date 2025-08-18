"""
Unit tests for the chat module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import requests

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from advanced_terminal_chatbot.utils import ConfigManager
from advanced_terminal_chatbot.chat import ChatSession


class TestChatSession(unittest.TestCase):
    """Test cases for ChatSession class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock config
        self.mock_config = Mock(spec=ConfigManager)
        self.mock_config.get_openai_base_url.return_value = "https://api.openai.com/v1"
        self.mock_config.get_anthropic_base_url.return_value = "https://api.anthropic.com/v1"
        self.mock_config.get_openai_api_key.return_value = "test_openai_key"
        self.mock_config.get_anthropic_api_key.return_value = "test_anthropic_key"
        
        # Mock the get method to return appropriate values for different keys
        def mock_get(key, default=None):
            if key == "MAX_TOKENS":
                return "1000"
            elif key == "TEMPERATURE":
                return "0.7"
            else:
                return default
        
        self.mock_config.get.side_effect = mock_get
        
        # Create a chat session for OpenAI
        self.openai_chat_session = ChatSession(
            self.mock_config, 
            "gpt-4o", 
            "OpenAI"
        )
        
        # Create a chat session for Anthropic
        self.anthropic_chat_session = ChatSession(
            self.mock_config, 
            "claude-3-5-sonnet-20241022", 
            "Anthropic"
        )
    
    def test_openai_initialization(self):
        """Test ChatSession initialization for OpenAI."""
        self.assertEqual(self.openai_chat_session.model, "gpt-4o")
        self.assertEqual(self.openai_chat_session.provider, "OpenAI")
        self.assertEqual(self.openai_chat_session.api_base, "https://api.openai.com/v1")
        self.assertEqual(self.openai_chat_session.api_key, "test_openai_key")
        self.assertEqual(len(self.openai_chat_session.conversation_history), 0)
    
    def test_anthropic_initialization(self):
        """Test ChatSession initialization for Anthropic."""
        self.assertEqual(self.anthropic_chat_session.model, "claude-3-5-sonnet-20241022")
        self.assertEqual(self.anthropic_chat_session.provider, "Anthropic")
        self.assertEqual(self.anthropic_chat_session.api_base, "https://api.anthropic.com/v1")
        self.assertEqual(self.anthropic_chat_session.api_key, "test_anthropic_key")
        self.assertEqual(len(self.anthropic_chat_session.conversation_history), 0)
    
    def test_add_message(self):
        """Test adding messages to conversation history."""
        self.openai_chat_session.add_message("user", "Hello")
        self.openai_chat_session.add_message("assistant", "Hi there!")
        
        self.assertEqual(len(self.openai_chat_session.conversation_history), 2)
        self.assertEqual(self.openai_chat_session.conversation_history[0]["role"], "user")
        self.assertEqual(self.openai_chat_session.conversation_history[0]["content"], "Hello")
        self.assertEqual(self.openai_chat_session.conversation_history[1]["role"], "assistant")
        self.assertEqual(self.openai_chat_session.conversation_history[1]["content"], "Hi there!")
    
    def test_clear_history(self):
        """Test clearing conversation history."""
        self.openai_chat_session.add_message("user", "Hello")
        self.openai_chat_session.add_message("assistant", "Hi there!")
        
        self.assertEqual(len(self.openai_chat_session.conversation_history), 2)
        
        self.openai_chat_session.clear_history()
        self.assertEqual(len(self.openai_chat_session.conversation_history), 0)
    
    def test_get_history(self):
        """Test getting conversation history copy."""
        self.openai_chat_session.add_message("user", "Hello")
        history = self.openai_chat_session.get_history()
        
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["content"], "Hello")
        
        # Verify it's a copy, not a reference
        history.append({"role": "test", "content": "test"})
        self.assertEqual(len(self.openai_chat_session.conversation_history), 1)
    
    @patch('requests.post')
    def test_openai_send_message_success(self, mock_post):
        """Test successful message sending to OpenAI."""
        # Mock successful OpenAI response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Hello! How can I help you?'}}]
        }
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result = self.openai_chat_session.send_message("Hello")
        
        self.assertEqual(result, "Hello! How can I help you?")
        self.assertEqual(len(self.openai_chat_session.conversation_history), 2)
        self.assertEqual(self.openai_chat_session.conversation_history[0]["role"], "user")
        self.assertEqual(self.openai_chat_session.conversation_history[1]["role"], "assistant")
    
    @patch('requests.post')
    def test_anthropic_send_message_success(self, mock_post):
        """Test successful message sending to Anthropic."""
        # Mock successful Anthropic response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'content': [{'text': 'Hello! How can I help you?'}]
        }
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result = self.anthropic_chat_session.send_message("Hello")
        
        self.assertEqual(result, "Hello! How can I help you?")
        self.assertEqual(len(self.anthropic_chat_session.conversation_history), 2)
        self.assertEqual(self.anthropic_chat_session.conversation_history[0]["role"], "user")
        self.assertEqual(self.anthropic_chat_session.conversation_history[1]["role"], "assistant")
    
    @patch('requests.post')
    def test_openai_authentication_error(self, mock_post):
        """Test OpenAI authentication error handling."""
        # Mock authentication error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result = self.openai_chat_session.send_message("Hello")
        
        self.assertIn("Authentication failed for OpenAI", result)
        self.assertEqual(len(self.openai_chat_session.conversation_history), 0)  # Should be removed
    
    @patch('requests.post')
    def test_anthropic_rate_limit_error(self, mock_post):
        """Test Anthropic rate limit error handling."""
        # Mock rate limit error response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result = self.anthropic_chat_session.send_message("Hello")
        
        self.assertIn("Rate limit exceeded for Anthropic", result)
        self.assertEqual(len(self.anthropic_chat_session.conversation_history), 0)  # Should be removed
    
    @patch('requests.post')
    def test_openai_model_not_found(self, mock_post):
        """Test OpenAI model not found error handling."""
        # Mock model not found error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result = self.openai_chat_session.send_message("Hello")
        
        self.assertIn("not found or unavailable for OpenAI", result)
        self.assertEqual(len(self.openai_chat_session.conversation_history), 0)  # Should be removed
    
    @patch('requests.post')
    def test_openai_timeout_error(self, mock_post):
        """Test OpenAI timeout error handling."""
        # Mock timeout error
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result = self.openai_chat_session.send_message("Hello")
        
        self.assertIn("timed out", result)
        self.assertEqual(len(self.openai_chat_session.conversation_history), 0)  # Should be removed
    
    @patch('requests.post')
    def test_anthropic_connection_error(self, mock_post):
        """Test Anthropic connection error handling."""
        # Mock connection error
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result = self.anthropic_chat_session.send_message("Hello")
        
        self.assertIn("Connection failed", result)
        self.assertEqual(len(self.anthropic_chat_session.conversation_history), 0)  # Should be removed
    
    @patch('requests.post')
    def test_openai_invalid_response_format(self, mock_post):
        """Test OpenAI invalid response format handling."""
        # Mock invalid response format
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'invalid': 'format'}
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result = self.openai_chat_session.send_message("Hello")
        
        self.assertIn("Invalid response format from OpenAI API", result)
        self.assertEqual(len(self.openai_chat_session.conversation_history), 0)  # Should be removed
    
    @patch('requests.post')
    def test_anthropic_invalid_response_format(self, mock_post):
        """Test Anthropic invalid response format handling."""
        # Mock invalid response format
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'invalid': 'format'}
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result = self.anthropic_chat_session.send_message("Hello")
        
        self.assertIn("Invalid response format from Anthropic API", result)
        self.assertEqual(len(self.anthropic_chat_session.conversation_history), 0)  # Should be removed
    
    def test_send_message_no_api_key(self):
        """Test sending message without API key."""
        # Set API key to None
        self.openai_chat_session.api_key = None
        
        result = self.openai_chat_session.send_message("Hello")
        
        self.assertIn("OpenAI API key not configured", result)
        self.assertEqual(len(self.openai_chat_session.conversation_history), 0)
    
    def test_format_openai_payload(self):
        """Test OpenAI payload formatting."""
        payload = self.openai_chat_session._format_openai_payload("Hello")
        
        self.assertEqual(payload["model"], "gpt-4o")
        self.assertEqual(payload["max_tokens"], 1000)
        self.assertEqual(payload["temperature"], 0.7)
        self.assertEqual(len(payload["messages"]), 1)
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(payload["messages"][0]["content"], "Hello")
    
    def test_format_anthropic_payload(self):
        """Test Anthropic payload formatting."""
        payload = self.anthropic_chat_session._format_anthropic_payload("Hello")
        
        self.assertEqual(payload["model"], "claude-3-5-sonnet-20241022")
        self.assertEqual(payload["max_tokens"], 1000)
        self.assertEqual(payload["temperature"], 0.7)
        self.assertEqual(len(payload["messages"]), 1)
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(payload["messages"][0]["content"], "Hello")

    @patch('requests.post')
    def test_openai_streaming_success(self, mock_post):
        """Test successful streaming response from OpenAI."""
        # Mock streaming response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            b'data: {"choices": [{"delta": {"content": "Hello"}}]}',
            b'data: {"choices": [{"delta": {"content": " there"}}]}',
            b'data: {"choices": [{"delta": {"content": "!"}}]}',
            b'data: [DONE]'
        ]
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result_parts = list(self.openai_chat_session.stream_response("Hello"))
        
        self.assertEqual(result_parts, ["Hello", " there", "!"])
        self.assertEqual(len(self.openai_chat_session.conversation_history), 2)
        self.assertEqual(self.openai_chat_session.conversation_history[1]["content"], "Hello there!")

    @patch('requests.post')
    def test_anthropic_streaming_success(self, mock_post):
        """Test successful streaming response from Anthropic."""
        # Mock streaming response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            b'data: {"type": "content_block_delta", "delta": {"text": "Hello"}}',
            b'data: {"type": "content_block_delta", "delta": {"text": " there"}}',
            b'data: {"type": "content_block_delta", "delta": {"text": "!"}}',
            b'data: [DONE]'
        ]
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result_parts = list(self.anthropic_chat_session.stream_response("Hello"))
        
        self.assertEqual(result_parts, ["Hello", " there", "!"])
        self.assertEqual(len(self.anthropic_chat_session.conversation_history), 2)
        self.assertEqual(self.anthropic_chat_session.conversation_history[1]["content"], "Hello there!")

    @patch('requests.post')
    def test_streaming_error_handling(self, mock_post):
        """Test error handling in streaming mode."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            result_parts = list(self.openai_chat_session.stream_response("Hello"))
        
        self.assertEqual(len(result_parts), 1)
        self.assertIn("Authentication failed", result_parts[0])
        self.assertEqual(len(self.openai_chat_session.conversation_history), 0)  # Should be removed

    def test_streaming_no_api_key(self):
        """Test streaming without API key."""
        self.openai_chat_session.api_key = None
        result_parts = list(self.openai_chat_session.stream_response("Hello"))
        
        self.assertEqual(len(result_parts), 1)
        self.assertIn("OpenAI API key not configured", result_parts[0])
        self.assertEqual(len(self.openai_chat_session.conversation_history), 0)


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key',
        'OPENAI_BASE_URL': 'https://api.openai.com/v1',
        'ANTHROPIC_BASE_URL': 'https://api.anthropic.com/v1',
        'DEFAULT_MODEL': 'gpt-4o',
        'DEFAULT_PROVIDER': 'OpenAI'
    })
    def test_get_openai_api_key(self):
        """Test getting OpenAI API key from environment."""
        config = ConfigManager()
        api_key = config.get_openai_api_key()
        self.assertEqual(api_key, 'test_openai_key')
    
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key',
        'OPENAI_BASE_URL': 'https://api.openai.com/v1',
        'ANTHROPIC_BASE_URL': 'https://api.anthropic.com/v1',
        'DEFAULT_MODEL': 'gpt-4o',
        'DEFAULT_PROVIDER': 'OpenAI'
    })
    def test_get_anthropic_api_key(self):
        """Test getting Anthropic API key from environment."""
        config = ConfigManager()
        api_key = config.get_anthropic_api_key()
        self.assertEqual(api_key, 'test_anthropic_key')
    
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key',
        'OPENAI_BASE_URL': 'https://api.openai.com/v1',
        'ANTHROPIC_BASE_URL': 'https://api.anthropic.com/v1',
        'DEFAULT_MODEL': 'gpt-4o',
        'DEFAULT_PROVIDER': 'OpenAI'
    })
    def test_get_openai_base_url(self):
        """Test getting OpenAI base URL from environment."""
        config = ConfigManager()
        base_url = config.get_openai_base_url()
        self.assertEqual(base_url, 'https://api.openai.com/v1')
    
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key',
        'OPENAI_BASE_URL': 'https://api.openai.com/v1',
        'ANTHROPIC_BASE_URL': 'https://api.anthropic.com/v1',
        'DEFAULT_MODEL': 'gpt-4o',
        'DEFAULT_PROVIDER': 'OpenAI'
    })
    def test_get_anthropic_base_url(self):
        """Test getting Anthropic base URL from environment."""
        config = ConfigManager()
        base_url = config.get_anthropic_base_url()
        self.assertEqual(base_url, 'https://api.anthropic.com/v1')
    
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key',
        'OPENAI_BASE_URL': 'https://api.openai.com/v1',
        'ANTHROPIC_BASE_URL': 'https://api.anthropic.com/v1',
        'DEFAULT_MODEL': 'gpt-4o',
        'DEFAULT_PROVIDER': 'OpenAI'
    })
    def test_get_default_model(self):
        """Test getting default model from environment."""
        config = ConfigManager()
        model = config.get_default_model()
        self.assertEqual(model, 'gpt-4o')
    
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key',
        'OPENAI_BASE_URL': 'https://api.openai.com/v1',
        'ANTHROPIC_BASE_URL': 'https://api.anthropic.com/v1',
        'DEFAULT_MODEL': 'gpt-4o',
        'DEFAULT_PROVIDER': 'OpenAI'
    })
    def test_get_default_provider(self):
        """Test getting default provider from environment."""
        config = ConfigManager()
        provider = config.get_default_provider()
        self.assertEqual(provider, 'OpenAI')
    
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key',
        'OPENAI_BASE_URL': 'https://api.openai.com/v1',
        'ANTHROPIC_BASE_URL': 'https://api.anthropic.com/v1',
        'DEFAULT_MODEL': 'gpt-4o',
        'DEFAULT_PROVIDER': 'OpenAI'
    })
    def test_validate_config_success(self):
        """Test successful configuration validation."""
        config = ConfigManager()
        result = config.validate_config()
        self.assertTrue(result)
    
    def test_validate_config_failure(self):
        """Test failed configuration validation."""
        # Remove API keys from environment
        with patch.dict(os.environ, {}, clear=True):
            config = ConfigManager(load_env=False)
            result = config.validate_config()
            self.assertFalse(result)
    
    def test_get_available_providers(self):
        """Test getting available providers."""
        config = ConfigManager()
        providers = config.get_available_providers()
        self.assertIn("OpenAI", providers)
        self.assertIn("Anthropic", providers)
        self.assertEqual(len(providers), 2)
    
    def test_get_available_providers_openai_only(self):
        """Test getting available providers when only OpenAI key is set."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}, clear=True):
            config = ConfigManager(load_env=False)
            providers = config.get_available_providers()
            self.assertIn("OpenAI", providers)
            self.assertNotIn("Anthropic", providers)
            self.assertEqual(len(providers), 1)
    
    def test_get_available_providers_anthropic_only(self):
        """Test getting available providers when only Anthropic key is set."""
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'}, clear=True):
            config = ConfigManager(load_env=False)
            providers = config.get_available_providers()
            self.assertIn("Anthropic", providers)
            self.assertNotIn("OpenAI", providers)
            self.assertEqual(len(providers), 1)

    def test_get_primary_provider(self):
        """Test getting the primary provider."""
        config = ConfigManager()
        primary = config.get_primary_provider()
        self.assertIn(primary, ["OpenAI", "Anthropic"])
        
        # Test with only one provider
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}, clear=True):
            config = ConfigManager()
            primary = config.get_primary_provider()
            self.assertEqual(primary, "OpenAI")
    
    def test_get_primary_provider_none(self):
        """Test getting primary provider when none are available."""
        with patch.dict(os.environ, {}, clear=True):
            config = ConfigManager(load_env=False)
            primary = config.get_primary_provider()
            self.assertIsNone(primary)
    
    def test_require_api_keys_success(self):
        """Test require_api_keys when keys are available."""
        config = ConfigManager()
        # Should not raise an exception
        config.require_api_keys()
    
    def test_require_api_keys_failure(self):
        """Test require_api_keys when no keys are available."""
        with patch.dict(os.environ, {}, clear=True):
            config = ConfigManager(load_env=False)
            with self.assertRaises(ValueError) as context:
                config.require_api_keys()
            self.assertIn("No API keys configured", str(context.exception))


if __name__ == '__main__':
    unittest.main()
