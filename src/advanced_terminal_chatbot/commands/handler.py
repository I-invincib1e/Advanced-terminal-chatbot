"""Command handler for the chatbot."""

from typing import Dict, Callable, Any

class CommandHandler:
    """Handles the registration and execution of chat commands."""

    def __init__(self, chat_session: Any):
        self.chat_session = chat_session
        self.commands: Dict[str, Callable] = {}
        self._register_commands()

    def _register_commands(self):
        """Register all available commands with their aliases."""
        # Core commands
        self.commands["/help"] = self.chat_session.display_help
        self.commands["/h"] = self.chat_session.display_help
        
        self.commands["/clear"] = self.chat_session.clear_history
        self.commands["/c"] = self.chat_session.clear_history
        
        self.commands["/history"] = self.chat_session.display_history
        self.commands["/hist"] = self.chat_session.display_history
        
        self.commands["/stream"] = self.chat_session.toggle_streaming
        self.commands["/s"] = self.chat_session.toggle_streaming
        
        self.commands["/quit"] = self.chat_session.quit
        self.commands["/q"] = self.chat_session.quit
        self.commands["/exit"] = self.chat_session.quit
        self.commands["/e"] = self.chat_session.quit
        
        # Code analysis commands
        self.commands["/analyze"] = self.chat_session.analyze_code_command
        self.commands["/a"] = self.chat_session.analyze_code_command
        
        self.commands["/analyze-file"] = self.chat_session.analyze_file_command
        self.commands["/af"] = self.chat_session.analyze_file_command
        
        self.commands["/analyze-dir"] = self.chat_session.analyze_dir_command
        self.commands["/ad"] = self.chat_session.analyze_dir_command
        
        self.commands["/analyze-project"] = self.chat_session.analyze_project_command
        self.commands["/ap"] = self.chat_session.analyze_project_command
        
        self.commands["/highlight"] = self.chat_session.highlight_code_command
        self.commands["/hl"] = self.chat_session.highlight_code_command
        
        self.commands["/paste"] = self.chat_session.paste_mode_command
        
        # New feature commands
        self.commands["/resume"] = self.chat_session.resume_conversation
        self.commands["/r"] = self.chat_session.resume_conversation
        
        self.commands["/export"] = self.chat_session.export_conversation
        self.commands["/exp"] = self.chat_session.export_conversation
        
        self.commands["/set-provider"] = self.chat_session.set_provider
        self.commands["/sp"] = self.chat_session.set_provider
        
        self.commands["/set-model"] = self.chat_session.set_model
        self.commands["/sm"] = self.chat_session.set_model
        
        self.commands["/copy"] = self.chat_session.copy_last_response
        self.commands["/cp"] = self.chat_session.copy_last_response
        
        self.commands["/save"] = self.chat_session.save_conversation
        self.commands["/sv"] = self.chat_session.save_conversation
        
        self.commands["/list-sessions"] = self.chat_session.list_sessions
        self.commands["/ls"] = self.chat_session.list_sessions
        
        self.commands["/delete-session"] = self.chat_session.delete_session
        self.commands["/del"] = self.chat_session.delete_session
        
        self.commands["/models"] = self.chat_session.show_models
        self.commands["/m"] = self.chat_session.show_models
        
        self.commands["/providers"] = self.chat_session.show_providers
        self.commands["/p"] = self.chat_session.show_providers
        
        # Template commands
        self.commands["/template"] = self.chat_session.use_template
        self.commands["/t"] = self.chat_session.use_template
        
        self.commands["/templates"] = self.chat_session.list_templates
        
        # Format control commands
        self.commands["/format"] = self.chat_session.set_format
        self.commands["/f"] = self.chat_session.set_format
        
        self.commands["/formats"] = self.chat_session.list_formats

    def execute(self, command: str) -> bool:
        """Execute a command."""
        parts = command.split(' ')
        command_name = parts[0]
        args = parts[1:]

        if command_name in self.commands:
            self.commands[command_name](args)
            return True
        return False

    def get_all_commands(self) -> list:
        """Get list of all available commands."""
        return list(self.commands.keys())
