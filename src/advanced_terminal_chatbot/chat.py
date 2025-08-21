"""
Enhanced chat session management for the terminal chatbot.
"""

from typing import Dict, List, Any, Optional, Generator
import os
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from .utils import ConfigManager
from .provider import ProviderManager
from .code_analyzer import CodeAnalyzer
from .commands.handler import CommandHandler
from .history_manager import HistoryManager
from .input_handler import HybridInputHandler
from .clipboard_manager import ClipboardManager
from .ui_enhancements import enhanced_ui
from .features.templates import TemplateManager
from .features.format_controls import FormatController


class ChatSession:
    """Enhanced chat session with conversation history, multi-line input, and advanced features."""

    def __init__(self, config: ConfigManager, model: str, provider_name: str):
        """Initialize the enhanced chat session."""
        try:
            self.config = config
            self.model = model
            self.provider_name = provider_name
            self.provider_manager = ProviderManager(config)
            self.provider = self.provider_manager.get_provider(provider_name)

            if not self.provider:
                raise ValueError(f"Unknown provider: {provider_name}")

            self.conversation_history: List[Dict[str, str]] = []
            self.max_tokens = int(config.get("MAX_TOKENS", "2000"))  # Increased default
            self.temperature = float(config.get("TEMPERATURE", "0.7"))
            self.streaming_mode = False
            self.console = Console(force_terminal=False, legacy_windows=False)
            
            # Session management
            self.current_session_id: Optional[str] = None
            self.last_response = ""

            # Initialize enhanced features with error handling
            try:
                self.code_analyzer = CodeAnalyzer()
            except Exception as e:
                self.console.print(f"[yellow]⚠️ Code analyzer initialization failed: {e}[/yellow]")
                self.code_analyzer = None
                
            try:
                self.history_manager = HistoryManager()
            except Exception as e:
                self.console.print(f"[yellow]⚠️ History manager initialization failed: {e}[/yellow]")
                self.history_manager = None
                
            try:
                self.clipboard_manager = ClipboardManager()
            except Exception as e:
                self.console.print(f"[yellow]⚠️ Clipboard manager initialization failed: {e}[/yellow]")
                self.clipboard_manager = None
            
            # Initialize template and format managers
            try:
                self.template_manager = TemplateManager()
            except Exception as e:
                self.console.print(f"[yellow]⚠️ Template manager initialization failed: {e}[/yellow]")
                self.template_manager = None
                
            try:
                self.format_controller = FormatController()
            except Exception as e:
                self.console.print(f"[yellow]⚠️ Format controller initialization failed: {e}[/yellow]")
                self.format_controller = None
            
            # Initialize input handler with all commands
            all_commands = [
                "/help", "/h", "/clear", "/c", "/history", "/hist", "/stream", "/s",
                "/quit", "/q", "/exit", "/e", "/analyze", "/a", "/highlight", "/hl",
                "/analyze-file", "/af", "/analyze-dir", "/ad", "/analyze-project", "/ap",
                "/paste",
                "/resume", "/r", "/export", "/exp", "/set-provider", "/sp",
                "/set-model", "/sm", "/copy", "/cp", "/save", "/sv",
                "/list-sessions", "/ls", "/delete-session", "/del",
                "/models", "/m", "/providers", "/p"
            ]
            
            try:
                self.input_handler = HybridInputHandler(all_commands, self.history_manager)
            except Exception as e:
                self.console.print(f"[yellow]⚠️ Input handler initialization failed: {e}[/yellow]")
                self.input_handler = None
            
            # Initialize command handler
            try:
                self.command_handler = CommandHandler(self)
            except Exception as e:
                self.console.print(f"[yellow]⚠️ Command handler initialization failed: {e}[/yellow]")
                self.command_handler = None
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize ChatSession: {e}")

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def clear_history(self, args: List[str] = None) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
        self.current_session_id = None
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
                self.last_response = result
                self.clipboard_manager.set_last_response(result)
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
                self.last_response = full_response
                self.clipboard_manager.set_last_response(full_response)

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
        """Display enhanced help information using the UI enhancements."""
        enhanced_ui.show_command_help_enhanced({})

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
        # Auto-save current session if it has messages
        if self.conversation_history and not self.current_session_id:
            self.save_conversation([])
        self.console.print("[bold yellow]👋 Goodbye![/bold yellow]")
        raise SystemExit

    def analyze_code_command(self, args: List[str]) -> None:
        """Handle the /analyze command with optional save functionality."""
        if not args:
            self.console.print(Panel(
                "[bold red]❌ Please provide code to analyze[/bold red]\n"
                "Usage: /analyze <code> [--save filename]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))
            return

        # Check for --save flag
        save_file = None
        if "--save" in args:
            save_index = args.index("--save")
            if save_index + 1 < len(args):
                save_file = args[save_index + 1]
                args = args[:save_index] + args[save_index + 2:]
            else:
                args.remove("--save")

        code = " ".join(args)
        result = self.analyze_code(code)
        
        self.console.print(Panel(
            Markdown(f"```\n{result}\n```"),
            title="[bold green]🔍 Code Analysis[/bold green]",
            border_style="green"
        ))

        # Save to file if requested
        if save_file:
            try:
                output_dir = Path("code_analysis")
                output_dir.mkdir(exist_ok=True)
                file_path = output_dir / save_file
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Code Analysis Report\n")
                    f.write(f"====================\n\n")
                    f.write(f"Original Code:\n{code}\n\n")
                    f.write(f"Analysis:\n{result}\n")
                
                self.console.print(f"[bold green]✅ Analysis saved to {file_path}[/bold green]")
            except Exception as e:
                self.console.print(f"[bold red]❌ Failed to save analysis: {str(e)}[/bold red]")

    def analyze_file_command(self, args: List[str]) -> None:
        """Handle the /analyze-file command."""
        if not args:
            self.console.print(Panel(
                "[bold red]❌ Please provide a file path to analyze[/bold red]\n"
                "Usage: /analyze-file <path> [--save filename]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))
            return

        file_path_str = args[0]
        save_file = None
        if "--save" in args:
            save_index = args.index("--save")
            if save_index + 1 < len(args):
                save_file = args[save_index + 1]
            else:
                self.console.print(Panel(
                    "[bold red]❌ Please provide a filename for --save[/bold red]",
                    title="[bold red]Error[/bold red]",
                    border_style="red"
                ))
                return
        
        try:
            file_path = Path(file_path_str)
            if not file_path.is_file():
                self.console.print(Panel(
                    f"[bold red]❌ File not found: {file_path_str}[/bold red]",
                    title="[bold red]Error[/bold red]",
                    border_style="red"
                ))
                return

            code_content = file_path.read_text(encoding='utf-8')
            result = self.analyze_code(code_content, language=file_path.suffix.lstrip('.'))
            
            self.console.print(Panel(
                Markdown(f"### Analysis of {file_path.name}\n\n```\n{result}\n```"),
                title=f"[bold green]🔍 File Analysis: {file_path.name}[/bold green]",
                border_style="green"
            ))

            if save_file:
                output_dir = Path("code_analysis")
                output_dir.mkdir(exist_ok=True)
                output_file_path = output_dir / save_file
                
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Code Analysis Report for {file_path.name}\n")
                    f.write(f"=========================================\n\n")
                    f.write(f"File: {file_path.absolute()}\n\n")
                    f.write(f"Original Content:\n```\n{code_content}\n```\n\n")
                    f.write(f"Analysis:\n{result}\n")
                
                self.console.print(f"[bold green]✅ Detailed analysis saved to {output_file_path}[/bold green]")

        except Exception as e:
            self.console.print(Panel(
                f"[bold red]❌ Failed to analyze file: {str(e)}[/bold red]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))

    def analyze_dir_command(self, args: List[str]) -> None:
        """Handle the /analyze-dir command."""
        if not args:
            self.console.print(Panel(
                "[bold red]❌ Please provide a directory path to analyze[/bold red]\n"
                "Usage: /analyze-dir <path> [--save filename]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))
            return

        dir_path_str = args[0]
        save_file = None
        if "--save" in args:
            save_index = args.index("--save")
            if save_index + 1 < len(args):
                save_file = args[save_index + 1]
            else:
                self.console.print(Panel(
                    "[bold red]❌ Please provide a filename for --save[/bold red]",
                    title="[bold red]Error[/bold red]",
                    border_style="red"
                ))
                return

        try:
            dir_path = Path(dir_path_str)
            if not dir_path.is_dir():
                self.console.print(Panel(
                    f"[bold red]❌ Directory not found: {dir_path_str}[/bold red]",
                    title="[bold red]Error[/bold red]",
                    border_style="red"
                ))
                return

            analysis_results = []
            file_count = 0
            
            # Recursive scan, excluding common ignored directories
            ignored_dirs = ['__pycache__', 'node_modules', '.git', 'venv', '.venv', 'env', '.env', 'htmlcov', 'exports', 'code_analysis']
            
            for root, dirs, files in os.walk(dir_path):
                dirs[:] = [d for d in dirs if d not in ignored_dirs] # Modify dirs in-place to skip
                
                for file_name in files:
                    current_file_path = Path(root) / file_name
                    # Only analyze common source code files
                    if current_file_path.suffix.lower() in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rb', '.php', '.html', '.css', '.json', '.xml', '.yml', '.yaml']:
                        try:
                            code_content = current_file_path.read_text(encoding='utf-8')
                            analysis = self.analyze_code(code_content, language=current_file_path.suffix.lstrip('.'))
                            analysis_results.append({
                                "file": str(current_file_path.relative_to(dir_path)),
                                "content": code_content,
                                "analysis": analysis
                            })
                            file_count += 1
                        except Exception as e:
                            self.console.print(f"[bold yellow]⚠️  Could not analyze {current_file_path}: {e}[/bold yellow]")

            self.console.print(Panel(
                f"[bold green]📁 Analysis Summary for: {dir_path_str}[/bold green]\n\n"
                f"✅ {file_count} files analyzed.",
                title="[bold green]🔍 Directory Analysis[/bold green]",
                border_style="green"
            ))

            if save_file:
                output_dir = Path("code_analysis")
                output_dir.mkdir(exist_ok=True)
                output_file_path = output_dir / save_file
                
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Directory Analysis Report for {dir_path_str}\n")
                    f.write(f"===========================================\n\n")
                    f.write(f"Analyzed Directory: {dir_path.absolute()}\n")
                    f.write(f"Total Files Analyzed: {file_count}\n\n")
                    
                    for res in analysis_results:
                        f.write(f"--- File: {res['file']} ---\n\n")
                        f.write(f"Original Content:\n```\n{res['content']}\n```\n\n")
                        f.write(f"Analysis:\n{res['analysis']}\n\n")
                        f.write("-" * 50 + "\n\n")
                
                self.console.print(f"[bold green]✅ Detailed analysis saved to {output_file_path}[/bold green]")

        except Exception as e:
            self.console.print(Panel(
                f"[bold red]❌ Failed to analyze directory: {str(e)}[/bold red]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))

    def analyze_project_command(self, args: List[str]) -> None:
        """Handle the /analyze-project command (analyzes current working directory)."""
        self.analyze_dir_command([os.getcwd()] + args) # Pass current working directory

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

    def paste_mode_command(self, args: List[str]) -> None:
        """Handle the /paste command to enter multi-line paste mode."""
        self.console.print(Panel(
            "[bold cyan]Entering Paste Mode. Type your multi-line content, then press Ctrl+D to submit.[/bold cyan]",
            title="[bold cyan]📝 Paste Mode[/bold cyan]",
            border_style="cyan"
        ))
        try:
            paste_content = self.input_handler.get_paste_input()
            if paste_content:
                self.console.print(f"[bold green]✅ Content pasted ({len(paste_content)} characters)[/bold green]")
                # Optionally, process the pasted content as a regular message or save it.
                # For now, we'll just treat it as a regular message for the AI.
                if self.streaming_mode:
                    with self.console.status("[bold yellow]🤔 Thinking...[/bold yellow]"):
                        full_response = ""
                        for part in self.stream_response(paste_content):
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
                        response = self.send_message(paste_content)
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
                # Removed redundant self.console.print() here
            else:
                self.console.print("[bold yellow]⚠️ Paste mode exited without content.[/bold yellow]")
        except KeyboardInterrupt:
            self.console.print("[bold yellow]⚠️ Paste mode cancelled.[/bold yellow]")
        except Exception as e:
            self.console.print(Panel(
                f"[bold red]❌ Error in paste mode: {str(e)}[/bold red]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))


    def save_conversation(self, args: List[str] = None) -> None:
        """Save the current conversation."""
        if not self.conversation_history:
            self.console.print("[bold yellow]⚠️ No conversation to save[/bold yellow]")
            return

        try:
            session_id = self.history_manager.save_conversation(
                self.conversation_history,
                self.provider_name,
                self.model,
                self.current_session_id
            )
            self.current_session_id = session_id
            self.console.print(f"[bold green]✅ Conversation saved with ID: {session_id}[/bold green]")
        except Exception as e:
            self.console.print(f"[bold red]❌ Failed to save conversation: {str(e)}[/bold red]")

    def resume_conversation(self, args: List[str]) -> None:
        """Resume a previous conversation."""
        if not args:
            # Show list of recent conversations
            self.list_sessions([])
            return

        session_id = args[0]
        try:
            conversation = self.history_manager.load_conversation(session_id)
            if conversation:
                self.conversation_history = conversation["messages"]
                self.current_session_id = session_id
                self.provider_name = conversation["provider"]
                self.model = conversation["model"]
                
                # Update provider if needed
                self.provider = self.provider_manager.get_provider(self.provider_name)
                
                self.console.print(f"[bold green]✅ Resumed conversation: {conversation['title']}[/bold green]")
                self.console.print(f"[bold blue]📅 From: {conversation['timestamp']}[/bold blue]")
                self.console.print(f"[bold cyan]🤖 Provider: {self.provider_name} ({self.model})[/bold cyan]")
            else:
                self.console.print(f"[bold red]❌ Conversation not found: {session_id}[/bold red]")
        except Exception as e:
            self.console.print(f"[bold red]❌ Failed to resume conversation: {str(e)}[/bold red]")

    def list_sessions(self, args: List[str] = None) -> None:
        """List saved conversations."""
        try:
            conversations = self.history_manager.list_conversations()
            if not conversations:
                self.console.print("[bold yellow]📝 No saved conversations found[/bold yellow]")
                return

            table = Table(title="💾 Saved Conversations")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Title", style="white")
            table.add_column("Provider", style="green")
            table.add_column("Model", style="yellow")
            table.add_column("Date", style="blue")

            for conv in conversations:
                table.add_row(
                    conv["id"][:8] + "...",
                    conv["title"][:50],
                    conv["provider"],
                    conv["model"],
                    str(conv["timestamp"])[:19] # Convert datetime object to string
                )

            self.console.print(table)
        except Exception as e:
            self.console.print(f"[bold red]❌ Failed to list conversations: {str(e)}[/bold red]")

    def export_conversation(self, args: List[str] = None) -> None:
        """Export current conversation."""
        if not self.conversation_history:
            self.console.print("[bold yellow]⚠️ No conversation to export[/bold yellow]")
            return

        format_type = args[0] if args else "json"
        if format_type not in ["json", "markdown", "txt"]:
            format_type = "json"

        # Save current conversation first if not already saved
        if not self.current_session_id:
            self.save_conversation([])

        try:
            content = self.history_manager.export_conversation(self.current_session_id, format_type)
            if content:
                export_dir = Path("exports")
                export_dir.mkdir(exist_ok=True)
                filename = f"conversation_{self.current_session_id[:8]}.{format_type}"
                file_path = export_dir / filename
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.console.print(f"[bold green]✅ Conversation exported to {file_path}[/bold green]")
            else:
                self.console.print("[bold red]❌ Failed to generate export content[/bold red]")
        except Exception as e:
            self.console.print(f"[bold red]❌ Failed to export conversation: {str(e)}[/bold red]")

    def delete_session(self, args: List[str]) -> None:
        """Delete a saved conversation."""
        if not args:
            self.console.print("[bold red]❌ Please provide a session ID to delete[/bold red]")
            return

        session_id = args[0]
        if self.input_handler.confirm_action(f"Delete conversation {session_id[:8]}...?"):
            try:
                if self.history_manager.delete_conversation(session_id):
                    self.console.print(f"[bold green]✅ Conversation deleted: {session_id}[/bold green]")
                    if self.current_session_id == session_id:
                        self.current_session_id = None
                else:
                    self.console.print(f"[bold red]❌ Conversation not found: {session_id}[/bold red]")
            except Exception as e:
                self.console.print(f"[bold red]❌ Failed to delete conversation: {str(e)}[/bold red]")

    def set_provider(self, args: List[str]) -> None:
        """Change the AI provider."""
        if not args:
            self.show_providers([])
            return

        provider_name = args[0].lower()
        try:
            # Validate provider exists and has valid API key
            validation_results = self.provider_manager.validate_api_keys()
            
            if provider_name not in validation_results:
                self.console.print(f"[bold red]❌ Unknown provider: {provider_name}[/bold red]")
                self.show_providers([])
                return
            
            if not validation_results[provider_name]:
                self.console.print(f"[bold red]❌ Invalid API key for provider: {provider_name}[/bold red]")
                return

            # Update provider
            self.provider_name = provider_name
            self.provider = self.provider_manager.get_provider(provider_name)
            
            # Get available models for new provider, prioritizing common ones
            models = self.provider_manager.fetch_api_models(provider_name, use_defaults=True)
            if models:
                # Use default model for new provider, or first available
                default_model_for_provider = self.provider_manager.get_default_model(provider_name)
                if default_model_for_provider and default_model_for_provider in models:
                    self.model = default_model_for_provider
                else:
                    self.model = models[0] # Fallback to first common model
                
                self.console.print(f"[bold green]✅ Provider changed to: {provider_name}[/bold green]")
                self.console.print(f"[bold cyan]🤖 Model set to: {self.model}[/bold cyan]")
            else:
                self.console.print(f"[bold red]❌ No models available for provider: {provider_name}[/bold red]")
                
        except Exception as e:
            self.console.print(f"[bold red]❌ Failed to change provider: {str(e)}[/bold red]")

    def set_model(self, args: List[str]) -> None:
        """Change the AI model."""
        if not args:
            self.show_models([])
            return

        model_name = args[0]
        try:
            models = self.provider_manager.fetch_api_models(self.provider_name, use_defaults=False) # Check all models
            if model_name in models:
                self.model = model_name
                self.console.print(f"[bold green]✅ Model changed to: {model_name}[/bold green]")
            else:
                self.console.print(f"[bold red]❌ Model not available for {self.provider_name}: {model_name}[/bold red]")
                self.show_models([])
        except Exception as e:
            self.console.print(f"[bold red]❌ Failed to change model: {str(e)}[/bold red]")

    def show_providers(self, args: List[str] = None) -> None:
        """Show available providers."""
        try:
            validation_results = self.provider_manager.validate_api_keys()
            
            table = Table(title="🔧 Available Providers")
            table.add_column("Provider", style="cyan")
            table.add_column("Status", style="white")
            table.add_column("Current", style="yellow")

            for provider, is_valid in validation_results.items():
                status = "✅ Valid" if is_valid else "❌ Invalid API Key"
                current = "👈 Current" if provider == self.provider_name else ""
                table.add_row(provider, status, current)

            self.console.print(table)
        except Exception as e:
            self.console.print(f"[bold red]❌ Failed to show providers: {str(e)}[/bold red]")

    def show_models(self, args: List[str] = None) -> None:
        """Show available models for current provider."""
        try:
            # Check if user wants to see all models
            show_all = args and '--all' in args
            
            if show_all:
                models = self.provider_manager.fetch_api_models(self.provider_name, use_defaults=False)
                title_suffix = " (All Models)"
                hint = f"[dim]Showing all {len(models)} models. Use /models for common models only.[/dim]"
            else:
                models = self.provider_manager.fetch_api_models(self.provider_name, use_defaults=True)
                title_suffix = " (Common Models)"
                hint = f"[dim]Showing {len(models)} common models. Use /models --all to see all available models.[/dim]"
            
            if not models:
                self.console.print(f"[bold yellow]⚠️ No models available for {self.provider_name}[/bold yellow]")
                return

            table = Table(title=f"🤖 Available Models for {self.provider_name}{title_suffix}")
            table.add_column("Model", style="cyan")
            table.add_column("Current", style="yellow")
            
            # Show default model first if it exists
            default_model = self.provider_manager.get_default_model(self.provider_name)
            if default_model and default_model in models:
                current = "👈 Current" if default_model == self.model else ""
                default_marker = " (Default)" if default_model != self.model else " (Default, Current)"
                table.add_row(f"[bold green]{default_model}[/bold green]", f"[green]{default_marker}[/green]{current}")
                # Remove from models list to avoid duplication
                models = [m for m in models if m != default_model]

            for model in models:
                current = "👈 Current" if model == self.model else ""
                table.add_row(model, current)

            self.console.print(table)
            self.console.print(hint)
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Failed to show models: {str(e)}[/bold red]")

    def copy_last_response(self, args: List[str] = None) -> None:
        """Copy the last AI response to clipboard."""
        self.clipboard_manager.copy_last_response()

    # Template-related methods
    def use_template(self, args: List[str]) -> None:
        """Use a conversation template."""
        if not self.template_manager:
            self.console.print("[bold red]❌ Template manager not available[/bold red]")
            return
            
        if not args:
            self.template_manager.list_templates()
            return

        template_name = args[0]
        template_content = self.template_manager.get_template(template_name)
        
        if template_content:
            self.console.print(Panel(
                template_content,
                title=f"[bold cyan]📝 Template: {template_name}[/bold cyan]",
                border_style="cyan"
            ))
            self.console.print("[dim]💡 Edit this template as needed and submit as your message.[/dim]")
        else:
            self.console.print(f"[bold red]❌ Template '{template_name}' not found[/bold red]")
            self.template_manager.list_templates()

    def list_templates(self, args: List[str] = None) -> None:
        """List available templates."""
        if not self.template_manager:
            self.console.print("[bold red]❌ Template manager not available[/bold red]")
            return
        self.template_manager.list_templates()

    # Format control methods
    def set_format(self, args: List[str]) -> None:
        """Set response format."""
        if not self.format_controller:
            self.console.print("[bold red]❌ Format controller not available[/bold red]")
            return
            
        if not args:
            self.format_controller.list_formats()
            return

        format_name = args[0]
        if self.format_controller.set_format(format_name):
            format_info = self.format_controller.get_format_info()
            self.console.print(f"[bold green]✅ Format changed to: {format_info['icon']} {format_info['name']}[/bold green]")
        else:
            self.console.print(f"[bold red]❌ Format '{format_name}' not found[/bold red]")
            self.format_controller.list_formats()

    def list_formats(self, args: List[str] = None) -> None:
        """List available response formats."""
        if not self.format_controller:
            self.console.print("[bold red]❌ Format controller not available[/bold red]")
            return
        self.format_controller.list_formats()

    def start_chat(self) -> None:
        """Start the enhanced interactive chat loop."""
        self.console.print(
            Panel(
                f"🚀 Starting chat with [bold green]{self.provider_name}[/bold green] ([bold yellow]{self.model}[/bold yellow])\n"
                f"💡 Type [bold cyan]/help[/bold cyan] or [bold cyan]/h[/bold cyan] for available commands\n"
                f"💡 Press [bold cyan]Shift+Enter[/bold cyan] for new line, [bold cyan]Enter[/bold cyan] to submit\n"
                f"💡 Use [bold cyan]/paste[/bold cyan] for multi-line code/text input\n"
                f"💡 Use [bold cyan]Tab[/bold cyan] for command completion",
                title="[bold]🤖 Enhanced Advanced Terminal Chatbot 🤖[/bold]",
                border_style="green",
            )
        )
        # Removed redundant self.console.print() here

        while True:
            try:
                user_input = self.input_handler.get_input()

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
                # Removed redundant self.console.print() here

            except (KeyboardInterrupt, EOFError, SystemExit):
                self.console.print("\n\n[bold yellow]👋 Goodbye![/bold yellow]")
                break
