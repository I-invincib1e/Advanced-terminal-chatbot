"""
Unit tests for the chat module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from advanced_terminal_chatbot.chat import ChatSession
from advanced_terminal_chatbot.utils import ConfigManager

class TestChatSession(unittest.TestCase):
    """Test cases for ChatSession class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_config = Mock(spec=ConfigManager)
        self.mock_config.get_openai_api_key.return_value = "test_openai_key"
        self.mock_config.get_openai_base_url.return_value = "https://api.openai.com/v1"
        
        # Mock different config values based on the key
        def mock_get(key, default=None):
            if key == "MAX_TOKENS":
                return "1000"
            elif key == "TEMPERATURE":
                return "0.7"
            return default
        
        self.mock_config.get.side_effect = mock_get

        with patch('advanced_terminal_chatbot.provider.ProviderManager'):
            with patch('advanced_terminal_chatbot.chat.CodeAnalyzer'):
                with patch('advanced_terminal_chatbot.chat.HistoryManager'):
                    with patch('advanced_terminal_chatbot.chat.ClipboardManager'):
                        with patch('advanced_terminal_chatbot.chat.HybridInputHandler'):
                            with patch('advanced_terminal_chatbot.chat.CommandHandler'):
                                self.chat_session = ChatSession(
                                    config=self.mock_config,
                                    model="gpt-4o",
                                    provider_name="OpenAI"
                                )
                                self.chat_session.provider = Mock()

    def test_initialization(self):
        """Test ChatSession initialization."""
        self.assertEqual(self.chat_session.model, "gpt-4o")
        self.assertEqual(self.chat_session.provider_name, "OpenAI")
        self.assertIsNotNone(self.chat_session.provider)
        self.assertEqual(self.chat_session.max_tokens, 1000)
        self.assertEqual(self.chat_session.temperature, 0.7)

    def test_add_message(self):
        """Test adding messages to conversation history."""
        self.chat_session.add_message("user", "Hello")
        self.assertEqual(len(self.chat_session.conversation_history), 1)
        self.assertEqual(self.chat_session.conversation_history[0]["role"], "user")
        self.assertEqual(self.chat_session.conversation_history[0]["content"], "Hello")

    def test_clear_history(self):
        """Test clearing conversation history."""
        self.chat_session.add_message("user", "Hello")
        self.chat_session.add_message("assistant", "Hi!")
        self.assertEqual(len(self.chat_session.conversation_history), 2)
        
        self.chat_session.clear_history()
        self.assertEqual(len(self.chat_session.conversation_history), 0)
        self.assertIsNone(self.chat_session.current_session_id)

    def test_get_history(self):
        """Test getting conversation history copy."""
        self.chat_session.add_message("user", "Hello")
        history = self.chat_session.get_history()
        
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["content"], "Hello")
        
        # Verify it's a copy, not reference
        history.append({"role": "test", "content": "test"})
        self.assertEqual(len(self.chat_session.conversation_history), 1)

    def test_send_message_success(self):
        """Test successful message sending."""
        self.chat_session.provider.send_message.return_value = "Hi there!"
        response = self.chat_session.send_message("Hello")
        self.assertEqual(response, "Hi there!")
        self.assertEqual(len(self.chat_session.conversation_history), 2)
        self.assertEqual(self.chat_session.conversation_history[1]["role"], "assistant")
        self.assertEqual(self.chat_session.last_response, "Hi there!")

    def test_send_message_error(self):
        """Test message sending with provider error."""
        self.chat_session.provider.send_message.return_value = "❌ Error"
        response = self.chat_session.send_message("Hello")
        self.assertIn("❌ Error", response)
        self.assertEqual(len(self.chat_session.conversation_history), 0)

    def test_send_message_exception(self):
        """Test message sending with exception."""
        self.chat_session.provider.send_message.side_effect = Exception("Network error")
        response = self.chat_session.send_message("Hello")
        self.assertIn("❌ Unexpected error", response)
        self.assertEqual(len(self.chat_session.conversation_history), 0)

    def test_stream_response_success(self):
        """Test successful streaming response."""
        self.chat_session.provider.stream_response.return_value = iter(["Hello", " there", "!"])
        
        full_response = ""
        for part in self.chat_session.stream_response("Hi"):
            full_response += part
        
        self.assertEqual(full_response, "Hello there!")
        self.assertEqual(len(self.chat_session.conversation_history), 2)
        self.assertEqual(self.chat_session.last_response, "Hello there!")

    def test_stream_response_error(self):
        """Test streaming response with error."""
        self.chat_session.provider.stream_response.return_value = iter(["❌ Error"])
        
        response_parts = list(self.chat_session.stream_response("Hi"))
        self.assertEqual(response_parts, ["❌ Error"])
        self.assertEqual(len(self.chat_session.conversation_history), 0)

    def test_stream_response_exception(self):
        """Test streaming response with exception."""
        self.chat_session.provider.stream_response.side_effect = Exception("Network error")
        
        response_parts = list(self.chat_session.stream_response("Hi"))
        self.assertEqual(len(response_parts), 1)
        self.assertIn("❌ Unexpected error", response_parts[0])

    def test_toggle_streaming(self):
        """Test toggling streaming mode."""
        initial_mode = self.chat_session.streaming_mode
        self.chat_session.toggle_streaming()
        self.assertEqual(self.chat_session.streaming_mode, not initial_mode)
        
        self.chat_session.toggle_streaming()
        self.assertEqual(self.chat_session.streaming_mode, initial_mode)

    def test_analyze_code_success(self):
        """Test successful code analysis."""
        self.chat_session.code_analyzer.format_code_block.return_value = "Formatted code"
        result = self.chat_session.analyze_code("print('hello')", "python")
        self.assertEqual(result, "Formatted code")

    def test_analyze_code_error(self):
        """Test code analysis with error."""
        self.chat_session.code_analyzer.format_code_block.side_effect = Exception("Analysis failed")
        result = self.chat_session.analyze_code("invalid code")
        self.assertIn("❌ Code analysis failed", result)

if __name__ == '__main__':
    unittest.main()
