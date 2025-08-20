"""
Unit tests for the chat module.
"""

import unittest
from unittest.mock import Mock, patch
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
        self.mock_config.get.return_value = "1000"

        with patch('advanced_terminal_chatbot.provider.ProviderManager'):
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

    def test_add_message(self):
        """Test adding messages to conversation history."""
        self.chat_session.add_message("user", "Hello")
        self.assertEqual(len(self.chat_session.conversation_history), 1)
        self.assertEqual(self.chat_session.conversation_history[0]["role"], "user")
        self.assertEqual(self.chat_session.conversation_history[0]["content"], "Hello")

    def test_send_message_success(self):
        """Test successful message sending."""
        self.chat_session.provider.send_message.return_value = "Hi there!"
        response = self.chat_session.send_message("Hello")
        self.assertEqual(response, "Hi there!")
        self.assertEqual(len(self.chat_session.conversation_history), 2)
        self.assertEqual(self.chat_session.conversation_history[1]["role"], "assistant")

    def test_send_message_error(self):
        """Test message sending with provider error."""
        self.chat_session.provider.send_message.return_value = "❌ Error"
        response = self.chat_session.send_message("Hello")
        self.assertIn("❌ Error", response)
        self.assertEqual(len(self.chat_session.conversation_history), 0)

if __name__ == '__main__':
    unittest.main()
