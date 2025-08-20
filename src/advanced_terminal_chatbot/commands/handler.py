"""Command handler for the chatbot."""

from typing import Dict, Callable, Any

class CommandHandler:
    """Handles the registration and execution of chat commands."""

    def __init__(self, chat_session: Any):
        self.chat_session = chat_session
        self.commands: Dict[str, Callable] = {}
        self._register_commands()

    def _register_commands(self):
        """Register all available commands."""
        self.commands["/help"] = self.chat_session.display_help
        self.commands["/clear"] = self.chat_session.clear_history
        self.commands["/history"] = self.chat_session.display_history
        self.commands["/stream"] = self.chat_session.toggle_streaming
        self.commands["/quit"] = self.chat_session.quit
        self.commands["/exit"] = self.chat_session.quit
        self.commands["/analyze"] = self.chat_session.analyze_code_command
        self.commands["/highlight"] = self.chat_session.highlight_code_command

    def execute(self, command: str) -> bool:
        """Execute a command."""
        parts = command.split(' ')
        command_name = parts[0]
        args = parts[1:]

        if command_name in self.commands:
            self.commands[command_name](args)
            return True
        return False
