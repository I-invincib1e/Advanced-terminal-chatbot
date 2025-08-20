"""
Advanced Terminal Chatbot

A powerful terminal-based chatbot with multi-provider support.
"""

__version__ = "1.0.0"
__author__ = "Advanced Terminal Chatbot Team"

from .chatbot import TerminalChatBot
from .provider import ProviderManager
from .chat import ChatSession
from .utils import ConfigManager
from .code_analyzer import CodeAnalyzer

__all__ = [
    "TerminalChatBot",
    "ProviderManager",
    "ChatSession",
    "ConfigManager",
    "CodeAnalyzer"
]
