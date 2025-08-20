"""
Chat session management for the terminal chatbot.
"""

from typing import Dict, List, Any, Optional, Generator
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from .utils import ConfigManager
from .provider import ProviderManager
from .code_analyzer import CodeAnalyzer
from .commands.handler import CommandHandler


class ChatSession:
    """Manages a chat session with conversation history and API communication."""

    def __init__(self, config: ConfigManager, model: str, provider_name: str):
        """Initialize the chat session."""
        self.config = config
        self.model = model
        self.provider_name = provider_name
        self.provider_manager = ProviderManager(config)
        self.provider = self.provider_manager.get_provider(provider_name)

        if not self.provider:
            raise ValueError(f"Unknown provider: {provider_name}")

        self.conversation_history: List[Dict[str, str]] = []
        self.max_tokens = int(config.get("MAX_TOKENS", "1000"))
        self.temperature = float(config.get("TEMPERATURE", "0.7"))
        self.streaming_mode = False
        self.console = Console()

        # Initialize features
        self.code_analyzer = CodeAnalyzer()
        self.command_handler = CommandHandler(self)

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def clear_history(self, args: List[str] = None) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
        self.console.print("[bold green]🧹 Conversation history cleared![/bold green]")

    def get_history(self) -> List[Dict[str, str]]:
        """Get a copy of the conversation history."""
        return self.conversation_history.copy()

    def send_message(self, message: str) -> str:
        """Send a message and get a response (non-streaming)."""
        self.add_message("user", message)
        try:
            result = self.provider.send_message(message, self.model, self.conversation_history)

            if not result.startswith("❌"):
                self.add_message("assistant", result)
            else:
                self.conversation_history.pop()
            return result
        except Exception as e:
            self.conversation_history.pop()
            return f"❌ Unexpected error: {str(e)}"

    def stream_response(self, message: str) -> Generator[str, None, None]:
        """Stream a response from the API."""
        self.add_message("user", message)
        try:
            full_response = ""
            for part in self.provider.stream_response(message, self.model, self.conversation_history):
                if part.startswith("❌"):
                    self.conversation_history.pop()
                    yield part
                    return

                full_response += part
                yield part

            if full_response:
                self.add_message("assistant", full_response)

        except Exception as e:
            self.conversation_history.pop()
            yield f"❌ Unexpected error: {str(e)}"

    def analyze_code(self, code: str, language: str = "auto", show_analysis: bool = True) -> str:
        """Analyze code with syntax highlighting and explanation."""
        try:
            return self.code_analyzer.format_code_block(code, language, show_analysis)
        except Exception as e:
            return f"❌ Code analysis failed: {str(e)}"

    def display_help(self, args: List[str] = None) -> None:
        """Display help information."""
        self.console.print(Panel(
            Markdown("""
## 📚 **Chat Commands:**
- `/help` - Show this help message
- `/clear` - Clear conversation history
- `/history` - Show conversation history
- `/stream` - Toggle streaming mode
- `/quit` or `/exit` - Exit the chat

## 🔍 **Code Analysis:**
- `/analyze <code>` - Analyze code with syntax highlighting
- `/highlight <code>` - Apply syntax highlighting only
            """),
            title="[bold cyan]Available Commands[/bold cyan]",
            border_style="cyan"
        ))

    def display_history(self, args: List[str] = None) -> None:
        """Display the conversation history."""
        if not self.conversation_history:
            self.console.print(
                Panel(
                    "[bold yellow]📝 No conversation history yet.[/bold yellow]",
                    title="[bold cyan]Conversation History[/bold cyan]",
                    border_style="yellow",
                )
            )
        else:
            self.console.print()
            for msg in self.conversation_history:
                if msg["role"] == "user":
                    self.console.print(
                        Panel(
                            Markdown(msg["content"]),
                            title="[bold blue]👤 You[/bold blue]",
                            border_style="blue",
                            title_align="left",
                        )
                    )
                else:
                    self.console.print(
                        Panel(
                            Markdown(msg["content"]),
                            title="[bold magenta]🤖 Assistant[/bold magenta]",
                            border_style="magenta",
                            title_align="left",
                        )
                    )
            self.console.print()

    def toggle_streaming(self, args: List[str] = None) -> None:
        """Toggle streaming mode."""
        self.streaming_mode = not self.streaming_mode
        mode = "ON" if self.streaming_mode else "OFF"
        self.console.print(f"[bold green]🔄 Streaming mode: {mode}[/bold green]")

    def quit(self, args: List[str] = None) -> None:
        """Exit the chat."""
        self.console.print("[bold yellow]👋 Goodbye![/bold yellow]")
        raise SystemExit

    def analyze_code_command(self, args: List[str]) -> None:
        """Handle the /analyze command."""
        if args:
            code = " ".join(args)
            result = self.analyze_code(code)
            self.console.print(Panel(
                Markdown(f"```\n{result}\n```"),
                title="[bold green]🔍 Code Analysis[/bold green]",
                border_style="green"
            ))
        else:
            self.console.print(Panel(
                "[bold red]❌ Please provide code to analyze[/bold red]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))

    def highlight_code_command(self, args: List[str]) -> None:
        """Handle the /highlight command."""
        if args:
            code = " ".join(args)
            try:
                highlighted = self.code_analyzer.highlight_syntax(code)
                self.console.print(Panel(
                    Markdown(f"```\n{highlighted}\n```"),
                    title="[bold yellow]🎨 Syntax Highlighting[/bold yellow]",
                    border_style="yellow"
                ))
            except Exception as e:
                self.console.print(Panel(
                    f"[bold red]❌ Highlighting failed: {str(e)}[/bold red]",
                    title="[bold red]Error[/bold red]",
                    border_style="red"
                ))
        else:
            self.console.print(Panel(
                "[bold red]❌ Please provide code to highlight[/bold red]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))

    def start_chat(self) -> None:
        """Start the interactive chat loop."""
        self.console.print(
            Panel(
                f"🚀 Starting chat with [bold green]{self.provider_name}[/bold green] ([bold yellow]{self.model}[/bold yellow])\n"
                "💡 Type [bold cyan]/help[/bold cyan] for available commands\n"
                "💡 Type [bold cyan]/stream[/bold cyan] to toggle streaming mode",
                title="[bold]🤖 Advanced Terminal Chatbot 🤖[/bold]",
                border_style="green",
            )
        )
        self.console.print()

        while True:
            try:
                user_input = Prompt.ask("[bold blue]👤 You[/bold blue]")

                if not user_input:
                    continue

                if user_input.startswith("/"):
                    if not self.command_handler.execute(user_input):
                        self.console.print(
                            Panel(
                                f"❌ Unknown command: {user_input.split(' ')[0]}",
                                title="[bold red]Error[/bold red]",
                                border_style="red",
                            )
                        )
                    continue

                # Regular chat message
                if self.streaming_mode:
                    with self.console.status("[bold yellow]🤔 Thinking...[/bold yellow]"):
                        full_response = ""
                        for part in self.stream_response(user_input):
                            full_response += part

                    self.console.print(
                        Panel(
                            Markdown(full_response),
                            title="[bold magenta]🤖 Assistant[/bold magenta]",
                            border_style="magenta",
                            title_align="left",
                        )
                    )

                else:
                    with self.console.status("[bold yellow]🤔 Thinking...[/bold yellow]"):
                        response = self.send_message(user_input)
                    
                    if response.startswith("❌"):
                        self.console.print(
                            Panel(
                                response,
                                title="[bold red]Error[/bold red]",
                                border_style="red",
                            )
                        )
                    else:
                        self.console.print(
                            Panel(
                                Markdown(response),
                                title="[bold magenta]🤖 Assistant[/bold magenta]",
                                border_style="magenta",
                                title_align="left",
                            )
                        )
                self.console.print()

            except (KeyboardInterrupt, EOFError, SystemExit):
                self.console.print("\n\n[bold yellow]👋 Goodbye![/bold yellow]")
                break
