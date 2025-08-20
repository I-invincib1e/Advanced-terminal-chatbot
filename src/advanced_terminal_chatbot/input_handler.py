"""
Enhanced hybrid input handler with beautiful prompts and improved user experience.
Uses the best libraries for terminal interfaces: prompt_toolkit, questionary, and rich.
"""

from typing import List, Optional, Callable, Any
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers import get_lexer_by_name, guess_lexer
from rich.console import Console
import questionary
from questionary import Style as QuestionaryStyle
from halo import Halo
import colorama


class ChatCompleter(Completer):
    """Custom completer for chat commands and context-aware suggestions."""

    def __init__(self, commands: List[str], history_manager: Any = None):
        self.commands = commands
        self.history_manager = history_manager

    def get_completions(self, document, complete_event):
        """Generate completions based on current input."""
        text = document.text_before_cursor
        
        # Command completion
        if text.startswith('/'):
            for command in self.commands:
                if command.startswith(text):
                    yield Completion(
                        command[len(text):],
                        display=command,
                        display_meta=self._get_command_description(command)
                    )
        
        # History-based completion for regular text
        elif self.history_manager and len(text) > 2:
            # This could be enhanced with more sophisticated completion logic
            pass

    def _get_command_description(self, command: str) -> str:
        """Get description for a command."""
        descriptions = {
            '/help': 'Show available commands',
            '/h': 'Show available commands',
            '/clear': 'Clear conversation history',
            '/c': 'Clear conversation history',
            '/history': 'Show conversation history',
            '/hist': 'Show conversation history',
            '/stream': 'Toggle streaming mode',
            '/s': 'Toggle streaming mode',
            '/quit': 'Exit the chatbot',
            '/q': 'Exit the chatbot',
            '/exit': 'Exit the chatbot',
            '/e': 'Exit the chatbot',
            '/analyze': 'Analyze code with syntax highlighting',
            '/a': 'Analyze code with syntax highlighting',
            '/analyze-file': 'Analyze a specific file',
            '/af': 'Analyze a specific file',
            '/analyze-dir': 'Analyze all files in directory',
            '/ad': 'Analyze all files in directory',
            '/analyze-project': 'Analyze current project',
            '/ap': 'Analyze current project',
            '/highlight': 'Apply syntax highlighting to code',
            '/hl': 'Apply syntax highlighting to code',
            '/paste': 'Enter multi-line paste mode',
            '/resume': 'Resume a previous conversation',
            '/r': 'Resume a previous conversation',
            '/export': 'Export conversation to file',
            '/exp': 'Export conversation to file',
            '/set-provider': 'Change AI provider',
            '/sp': 'Change AI provider',
            '/set-model': 'Change AI model',
            '/sm': 'Change AI model',
            '/copy': 'Copy last response to clipboard',
            '/cp': 'Copy last response to clipboard',
            '/save': 'Save current conversation',
            '/sv': 'Save current conversation',
            '/list-sessions': 'List saved conversations',
            '/ls': 'List saved conversations',
            '/delete-session': 'Delete a conversation',
            '/del': 'Delete a conversation',
            '/models': 'Show available models',
            '/m': 'Show available models',
            '/providers': 'Show available providers',
            '/p': 'Show available providers'
        }
        return descriptions.get(command, 'Custom command')


class HybridInputHandler:
    """Hybrid input handler: Enter to submit, Shift+Enter for new lines, /paste for multi-line."""

    def __init__(self, commands: List[str], history_manager: Any = None):
        self.commands = commands
        self.history_manager = history_manager
        self.console = Console()
        
        # Setup prompt toolkit components
        self.completer = ChatCompleter(commands, history_manager)
        self.history = InMemoryHistory()
        # self.global_key_bindings = self._create_global_key_bindings() # This is no longer needed as bindings are added explicitly
        self.style = self._create_style()
        
        # Load command history if available
        if self.history_manager:
            self._load_command_history()

    def _create_global_key_bindings(self) -> KeyBindings:
        """Create global key bindings applicable to all prompts."""
        kb = KeyBindings()
        @kb.add('c-c')  # Ctrl+C to cancel
        def _(event):
            event.app.exit(exception=KeyboardInterrupt)
        return kb

    def _create_style(self) -> Style:
        """Create custom style for the input."""
        return Style.from_dict({
            'prompt': '#00aa00 bold',
            'input': '#ffffff',
            'completion-menu.completion': 'bg:#008888 #ffffff',
            'completion-menu.completion.current': 'bg:#00aaaa #000000',
            'scrollbar.background': 'bg:#888888',
            'scrollbar.button': 'bg:#444444',
        })

    def _load_command_history(self) -> None:
        """Load command history from the history manager."""
        try:
            commands = self.history_manager.get_command_history()
            for command in reversed(commands):  # Add in reverse order for proper history
                self.history.append_string(command)
        except Exception:
            pass  # Ignore errors in loading history

    def get_input(self, prompt_text: str = "👤 You") -> str:
        """Get input from user - Enter to submit, Shift+Enter for new line."""
        
        # Create a new KeyBindings object with specific bindings for this input mode
        kb = KeyBindings()
        
        # Add Ctrl+C binding for cancellation
        @kb.add('c-c')
        def _(event):
            event.app.exit(exception=KeyboardInterrupt)

        # Bind Enter to submit (with eager=True for default Shift+Enter newline behavior)
        @kb.add('enter', eager=True) 
        def _(event):
            event.app.exit(result=event.app.current_buffer.text)

        # Shift+Enter automatically inserts a newline when multiline=True and Enter is bound with eager=True.
        # No explicit Shift+Enter binding is needed here.

        try:
            result = prompt(
                HTML(f'<prompt>{prompt_text}:</prompt> '),
                completer=self.completer,
                complete_while_typing=True,
                history=self.history,
                key_bindings=kb,  # Use specific key bindings for this prompt
                style=self.style,
                multiline=True,  # Enable multiline input
                wrap_lines=True,
                mouse_support=False,  # Disable mouse support to allow normal scrolling
                enable_history_search=True
            )
            
            # Save non-empty inputs to history
            if result.strip() and self.history_manager:
                self.history_manager.save_command(result.strip())
            
            return result.strip()
            
        except KeyboardInterrupt:
            raise
        except EOFError:
            return ""

    def get_paste_input(self, prompt_text: str = "📝 Paste Mode") -> str:
        """Get multi-line paste input - dedicated mode for large text blocks (Ctrl+D to submit)."""
        
        kb = KeyBindings()
        
        # Add Ctrl+C binding for cancellation
        @kb.add('c-c')
        def _(event):
            event.app.exit(exception=KeyboardInterrupt)

        @kb.add('c-d')  # Ctrl+D to submit in paste mode
        def _(event):
            event.app.exit(result=event.app.current_buffer.text)

        bottom_toolbar = HTML(
            '<b>Paste Mode</b> - Enter your multi-line content, press <b>Ctrl+D</b> to submit'
        )

        try:
            result = prompt(
                HTML(f'<prompt>{prompt_text}:</prompt>\n'),
                key_bindings=kb,
                style=self.style,
                bottom_toolbar=bottom_toolbar,
                multiline=True, # Allow multiline input
                wrap_lines=True,
                mouse_support=False  # Disable mouse support to allow normal scrolling
            )
            
            return result.strip()
            
        except KeyboardInterrupt:
            raise
        except EOFError:
            return ""

    def get_code_input(self, language: str = "python") -> str:
        """Get multi-line code input with syntax highlighting (Ctrl+D to submit)."""
        try:
            lexer = PygmentsLexer(get_lexer_by_name(language))
        except:
            lexer = None

        kb = KeyBindings()
        
        # Add Ctrl+C binding for cancellation
        @kb.add('c-c')
        def _(event):
            event.app.exit(exception=KeyboardInterrupt)

        @kb.add('c-d')  # Ctrl+D to submit
        def _(event):
            event.app.exit(result=event.app.current_buffer.text)

        bottom_toolbar = HTML(
            f'<b>Code Mode ({language})</b> - Press <b>Ctrl+D</b> to submit, <b>Enter</b> for new line'
        )

        try:
            result = prompt(
                HTML('📝 <prompt>Code:</prompt>\n'),
                lexer=lexer,
                key_bindings=kb,
                style=self.style,
                bottom_toolbar=bottom_toolbar,
                multiline=True, # Allow multiline input
                wrap_lines=True,
                mouse_support=False  # Disable mouse support to allow normal scrolling
            )
            
            return result.strip()
            
        except KeyboardInterrupt:
            raise
        except EOFError:
            return ""

    def confirm_action(self, message: str) -> bool:
        """Get confirmation from user."""
        try:
            return confirm(
                HTML(f'<prompt>{message}</prompt>'),
                style=self.style
            )
        except KeyboardInterrupt:
            return False

    def select_from_list(self, items: List[str], title: str = "Select an option") -> Optional[str]:
        """Allow user to select from a list of options."""
        if not items:
            return None
        
        self.console.print(f"\n[bold cyan]{title}:[/bold cyan]")
        for i, item in enumerate(items, 1):
            self.console.print(f"  {i}. {item}")
        
        while True:
            try:
                choice = prompt(
                    HTML('<prompt>Enter choice (number or name):</prompt> '),
                    style=self.style
                )
                
                # Try to parse as number
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(items):
                        return items[index]
                except ValueError:
                    pass
                
                # Try to match by name
                for item in items:
                    if item.lower() == choice.lower():
                        return item
                
                self.console.print("[red]Invalid choice. Please try again.[/red]")
                
            except (KeyboardInterrupt, EOFError):
                return None


# Backwards compatibility alias
MultiLineInputHandler = HybridInputHandler
