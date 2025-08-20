"""
UI Enhancement module using the best libraries for terminal interfaces.
Includes ASCII banners, loading spinners, enhanced prompts, and visual improvements.
"""

import os
import sys
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.align import Align
from rich.columns import Columns
from rich.text import Text
import pyfiglet
import questionary
from questionary import Style
import colorama
from halo import Halo
import time
from loguru import logger
import random


class EnhancedUI:
    """Enhanced UI manager with beautiful terminal interfaces."""
    
    def __init__(self):
        # Initialize colorama for cross-platform color support
        colorama.init(autoreset=True)
        
        self.console = Console(force_terminal=True, legacy_windows=False)
        
        # Custom questionary style
        self.questionary_style = Style([
            ('qmark', 'fg:#ff9d00 bold'),       # Question mark
            ('question', 'bold'),                # Question text
            ('answer', 'fg:#ff9d00 bold'),       # Answer text
            ('pointer', 'fg:#ff9d00 bold'),      # Pointer used in select and checkbox prompts
            ('highlighted', 'fg:#ff9d00 bold'),  # Pointed-at choice in select and checkbox prompts
            ('selected', 'fg:#cc5454'),          # Style for a selected item of a checkbox
            ('separator', 'fg:#cc5454'),         # Separator in lists
            ('instruction', ''),                 # User instructions for select, rawselect, checkbox
            ('text', ''),                        # Plain text
            ('disabled', 'fg:#858585 italic')    # Disabled choices for select and checkbox prompts
        ])
        
        # ASCII art fonts for banners
        self.banner_fonts = ['slant', 'big', 'block', 'digital', 'starwars', 'doom']
        
        # Setup enhanced logging with loguru
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup enhanced logging with loguru."""
        # Remove default logger
        logger.remove()
        
        # Add colorful console logging
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO",
            colorize=True
        )
        
        # Add file logging for debugging
        logger.add(
            "chatbot_debug.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="7 days"
        )

    def create_ascii_banner(self, text: str, font: str = None) -> str:
        """Create ASCII art banner using pyfiglet."""
        try:
            if font is None:
                font = random.choice(self.banner_fonts)
            
            # Try the specified font first
            try:
                banner = pyfiglet.figlet_format(text, font=font)
            except:
                # Fallback to default font
                banner = pyfiglet.figlet_format(text)
                
            return banner.strip()
        except Exception as e:
            logger.warning(f"Failed to create ASCII banner: {e}")
            return f"=== {text.upper()} ==="

    def show_startup_banner(self):
        """Display an enhanced startup banner."""
        self.console.clear()
        
        # Create ASCII banner
        banner = self.create_ascii_banner("ChatBot AI", "slant")
        
        # Create gradient effect for the banner
        banner_text = Text()
        lines = banner.split('\n')
        colors = ['#ff0080', '#ff4080', '#ff8080', '#ffb380', '#ffe680', '#b3ff80']
        
        for i, line in enumerate(lines):
            color = colors[i % len(colors)]
            banner_text.append(line + '\n', style=color)
        
        # Center the banner
        centered_banner = Align.center(banner_text)
        
        # Create info panel
        info_panel = Panel(
            Markdown("""
# 🚀 **Advanced Terminal Chatbot**

✨ **Enhanced Features:**
- 🎨 **Beautiful UI** with Rich formatting and colors
- 🤖 **Multi-Provider AI** (OpenAI, Anthropic, and more)
- 💬 **Interactive Chat** with streaming responses
- 🔍 **Code Analysis** with syntax highlighting  
- 📝 **Session Management** with history and export
- 🎯 **Smart Input** with auto-completion and multi-line support
- 🔧 **Extensible Commands** for power users

**Type `/help` to see all available commands!**
            """),
            title="[bold cyan]Welcome to the Future of Terminal AI[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        # Display everything
        self.console.print(centered_banner)
        self.console.print()
        self.console.print(info_panel)
        self.console.print()

    def create_loading_spinner(self, text: str = "Processing...") -> Halo:
        """Create a beautiful loading spinner using halo."""
        spinners = ['dots', 'line', 'star', 'arrow3', 'bouncingBar', 'bouncingBall']
        spinner_type = random.choice(spinners)
        
        return Halo(
            text=text,
            spinner=spinner_type,
            color='cyan',
            text_color='white'
        )

    def show_thinking_animation(self, duration: float = 2.0):
        """Show a 'thinking' animation for AI processing."""
        thinking_messages = [
            "🤔 Analyzing your request...",
            "🧠 Processing with AI...",
            "⚡ Generating response...",
            "🎯 Crafting the perfect answer...",
            "🔍 Searching knowledge base...",
            "💭 Thinking deeply..."
        ]
        
        message = random.choice(thinking_messages)
        
        with self.create_loading_spinner(message) as spinner:
            time.sleep(duration)
            spinner.succeed("✅ Ready!")

    def enhanced_select(self, 
                       choices: List[str], 
                       message: str = "Please select an option:",
                       instruction: str = "(Use arrow keys to move, Enter to select)") -> Optional[str]:
        """Enhanced selection prompt using questionary."""
        try:
            return questionary.select(
                message,
                choices=choices,
                instruction=instruction,
                style=self.questionary_style,
                use_shortcuts=True,
                use_arrow_keys=True,
                use_emacs_keys=True
            ).ask()
        except KeyboardInterrupt:
            return None

    def enhanced_confirm(self, message: str, default: bool = False) -> bool:
        """Enhanced confirmation prompt."""
        try:
            return questionary.confirm(
                message,
                default=default,
                style=self.questionary_style
            ).ask()
        except KeyboardInterrupt:
            return False

    def enhanced_text_input(self, 
                           message: str, 
                           default: str = "",
                           validate_func=None) -> Optional[str]:
        """Enhanced text input with validation."""
        try:
            return questionary.text(
                message,
                default=default,
                validate=validate_func,
                style=self.questionary_style
            ).ask()
        except KeyboardInterrupt:
            return None

    def show_provider_selection(self, providers: Dict[str, bool]) -> Optional[str]:
        """Enhanced provider selection interface."""
        self.console.print("\n[bold cyan]🔧 Select AI Provider[/bold cyan]")
        
        # Filter valid providers
        valid_providers = [name for name, valid in providers.items() if valid]
        
        if not valid_providers:
            self.console.print("[bold red]❌ No valid providers found![/bold red]")
            return None
        
        # Create choices with status indicators
        choices = []
        for provider in valid_providers:
            status = "✅" if providers[provider] else "❌"
            choices.append(f"{status} {provider.title()}")
        
        selected = self.enhanced_select(
            choices,
            "Choose your AI provider:",
            "(Navigate with ↑↓, select with Enter)"
        )
        
        if selected:
            # Extract provider name from choice
            provider_name = selected.split(' ', 1)[1].lower()
            return provider_name
        
        return None

    def show_model_selection(self, models: List[str], provider: str) -> Optional[str]:
        """Enhanced model selection interface."""
        self.console.print(f"\n[bold cyan]🤖 Select Model for {provider.title()}[/bold cyan]")
        
        if not models:
            self.console.print("[bold red]❌ No models available![/bold red]")
            return None
        
        # Limit display for very long lists
        display_models = models[:20] if len(models) > 20 else models
        if len(models) > 20:
            display_models.append("... (and more)")
        
        selected = self.enhanced_select(
            display_models,
            f"Choose a model for {provider}:",
            f"(Showing {len(display_models)} models, navigate with ↑↓)"
        )
        
        return selected if selected and selected != "... (and more)" else None

    def show_progress_bar(self, items: List[Any], description: str = "Processing"):
        """Show a progress bar for long operations."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True
        ) as progress:
            
            task = progress.add_task(description, total=len(items))
            
            for item in items:
                # Yield control back to caller
                yield item
                progress.advance(task)
                time.sleep(0.1)  # Small delay for visual effect

    def create_status_table(self, data: Dict[str, Any], title: str = "Status") -> Table:
        """Create a beautiful status table."""
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Status", justify="center")
        
        for key, value in data.items():
            if isinstance(value, bool):
                status = "✅" if value else "❌"
                value_str = "Enabled" if value else "Disabled"
            elif isinstance(value, (int, float)):
                status = "📊"
                value_str = str(value)
            else:
                status = "ℹ️"
                value_str = str(value)
            
            table.add_row(key, value_str, status)
        
        return table

    def show_command_help_enhanced(self, commands: Dict[str, str]):
        """Display enhanced command help with categories."""
        
        # Categorize commands
        categories = {
            "💬 Chat Commands": {
                "/help": "Show this help message",
                "/clear": "Clear conversation history", 
                "/history": "Show conversation history",
                "/stream": "Toggle streaming mode",
                "/quit": "Exit the chatbot"
            },
            "🔍 Code Analysis": {
                "/analyze": "Analyze code with syntax highlighting",
                "/analyze-file": "Analyze a specific file",
                "/analyze-dir": "Analyze directory",
                "/analyze-project": "Analyze entire project",
                "/highlight": "Apply syntax highlighting"
            },
            "💾 Session Management": {
                "/save": "Save current conversation",
                "/resume": "Resume previous conversation",
                "/list-sessions": "List saved conversations", 
                "/export": "Export conversation",
                "/delete-session": "Delete a conversation"
            },
            "🔧 Configuration": {
                "/set-provider": "Change AI provider",
                "/set-model": "Change AI model",
                "/providers": "Show available providers",
                "/models": "Show available models"
            },
            "📋 Utilities": {
                "/copy": "Copy last response to clipboard",
                "/paste": "Enter multi-line paste mode"
            }
        }
        
        panels = []
        for category, cmds in categories.items():
            cmd_text = ""
            for cmd, desc in cmds.items():
                cmd_text += f"[bold cyan]{cmd}[/bold cyan] - {desc}\n"
            
            panel = Panel(
                cmd_text.rstrip(),
                title=category,
                border_style="blue",
                padding=(0, 1)
            )
            panels.append(panel)
        
        # Display in columns
        self.console.print()
        self.console.print(Columns(panels, equal=True, expand=True))
        self.console.print()

    def show_error_panel(self, error_message: str, title: str = "Error"):
        """Display a formatted error panel."""
        self.console.print(Panel(
            f"[bold red]{error_message}[/bold red]",
            title=f"[bold red]❌ {title}[/bold red]",
            border_style="red",
            padding=(1, 2)
        ))

    def show_success_panel(self, message: str, title: str = "Success"):
        """Display a formatted success panel."""
        self.console.print(Panel(
            f"[bold green]{message}[/bold green]",
            title=f"[bold green]✅ {title}[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))

    def show_info_panel(self, message: str, title: str = "Information"):
        """Display a formatted info panel."""
        self.console.print(Panel(
            f"[bold blue]{message}[/bold blue]",
            title=f"[bold blue]ℹ️ {title}[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        ))

    def create_conversation_panel(self, role: str, content: str, timestamp: str = None) -> Panel:
        """Create a beautifully formatted conversation panel."""
        if role == "user":
            icon = "👤"
            title_style = "bold blue"
            border_style = "blue"
            title = f"{icon} You"
        else:
            icon = "🤖"
            title_style = "bold magenta" 
            border_style = "magenta"
            title = f"{icon} Assistant"
        
        if timestamp:
            title += f" [dim]({timestamp})[/dim]"
        
        # Format content as markdown for better rendering
        formatted_content = Markdown(content)
        
        return Panel(
            formatted_content,
            title=f"[{title_style}]{title}[/{title_style}]",
            border_style=border_style,
            title_align="left",
            padding=(0, 1)
        )


# Global instance for easy access
enhanced_ui = EnhancedUI()
