"""
Main chatbot orchestrator module.
"""

import sys
import argparse
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from .utils import ConfigManager, create_env_sample
from .provider import ProviderManager
from .chat import ChatSession
from .ui_enhancements import enhanced_ui


class TerminalChatBot:
    """Main chatbot orchestrator class."""
    
    def __init__(self):
        self.config = ConfigManager()
        self.provider_manager = ProviderManager(self.config)
        self.selected_model: Optional[str] = None
        self.selected_provider: Optional[str] = None
        self.console = Console()
    
    def display_welcome(self) -> None:
        """Display the enhanced welcome message with ASCII banner."""
        enhanced_ui.show_startup_banner()
    
    def setup_provider_and_model(self) -> None:
        """Set up the provider and model selection."""
        # Get default provider and model from config
        default_provider = self.config.get_default_provider()
        default_model = self.config.get_default_model()

        self.console.print("[bold cyan]🔍 Validating API keys...[/bold cyan]")
        validation_results = self.provider_manager.validate_api_keys()

        valid_providers = [
            provider for provider, is_valid in validation_results.items() if is_valid
        ]

        if not valid_providers:
            self.console.print(
                Panel(
                    "[bold red]No valid API keys found. Please check your configuration. Run with --create-env to create a sample .env file.[/bold red]",
                    title="[bold red]Validation Error[/bold red]",
                    border_style="red",
                )
            )
            sys.exit(1)

        for provider in valid_providers:
            self.console.print(f"[bold green]✅ {provider} API key is valid[/bold green]")

        if default_provider and default_provider in valid_providers:
            self.console.print(f"[bold blue]📋 Using default provider: {default_provider}[/bold blue]")
            self.selected_provider = default_provider
        else:
            if len(valid_providers) == 1:
                self.selected_provider = valid_providers[0]
                self.console.print(f"[bold green]✅ Auto-selected provider: {self.selected_provider}[/bold green]")
            else:
                self.selected_provider = self.provider_manager.select_provider_from_list(
                    valid_providers
                )

        try:
            # First try to get default model for this provider
            provider_default = self.provider_manager.get_default_model(self.selected_provider)
            
            # Get filtered common models (not all 53+ models)
            models = self.provider_manager.fetch_api_models(self.selected_provider, use_defaults=True)
            if not models:
                self.console.print(
                    Panel(
                        "[bold red]Cannot proceed without available models. Please check your API key and internet connection.[/bold red]",
                        title="[bold red]API Error[/bold red]",
                        border_style="red",
                    )
                )
                sys.exit(1)

            # Priority: 1) Config default 2) Provider default 3) First available model
            if default_model and default_model in models:
                self.console.print(f"[bold blue]📋 Using config default model: {default_model}[/bold blue]")
                self.selected_model = default_model
            elif provider_default and provider_default in models:
                self.console.print(f"[bold green]🎯 Using provider default model: {provider_default}[/bold green]")
                self.selected_model = provider_default
            else:
                self.console.print(f"[bold cyan]📝 Showing {len(models)} common models (use /models to see all)[/bold cyan]")
                self.selected_model = self.provider_manager.select_api_model(models)

        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Error during setup: {e}[/bold red]",
                    title="[bold red]Setup Error[/bold red]",
                    border_style="red",
                )
            )
            sys.exit(1)

    def run(self) -> None:
        """Run the chatbot."""
        try:
            self.display_welcome()
            
            try:
                self.config.require_api_keys()
            except ValueError as e:
                self.console.print(
                    Panel(
                        f"[bold red]Configuration Error: {e}\n\nTip: Create a .env file with your API keys. Run with --create-env to create a sample .env file. You need at least one of: OPENAI_API_KEY or ANTHROPIC_API_KEY.[/bold red]",
                        title="[bold red]Configuration Error[/bold red]",
                        border_style="red",
                    )
                )
                sys.exit(1)
            
            self.setup_provider_and_model()
            
            chat_session = ChatSession(
                self.config, self.selected_model, self.selected_provider
            )
            chat_session.start_chat()
            
        except KeyboardInterrupt:
            self.console.print("\n\n[bold yellow]👋 Chatbot interrupted. Goodbye![/bold yellow]")
        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Unexpected error: {e}. Please check your configuration and try again.[/bold red]",
                    title="[bold red]Error[/bold red]",
                    border_style="red",
                )
            )
            sys.exit(1)


def main():
    """Main entry point with command line argument support."""
    parser = argparse.ArgumentParser(
        description="Advanced Terminal Chatbot with direct OpenAI and Anthropic API support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start interactive chatbot
  %(prog)s --create-env       # Create sample .env file
  %(prog)s --help             # Show this help message

Environment Variables:
  OPENAI_API_KEY              # Your OpenAI API key (optional)
  ANTHROPIC_API_KEY           # Your Anthropic API key (optional)
  OPENAI_BASE_URL             # Custom OpenAI API base URL (optional)
  ANTHROPIC_BASE_URL          # Custom Anthropic API base URL (optional)
  DEFAULT_MODEL                # Default model to use (optional)
  DEFAULT_PROVIDER             # Default provider (optional)
  MAX_TOKENS                   # Max tokens per response (optional)
  TEMPERATURE                  # Response temperature (optional)

Note: At least one API key (OPENAI_API_KEY or ANTHROPIC_API_KEY) must be set.
        """
    )
    
    parser.add_argument(
        '--create-env',
        action='store_true',
        help='Create a sample .env file'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.2.0'
    )
    
    args = parser.parse_args()
    
    if args.create_env:
        create_env_sample()
        return
    
    # Start the chatbot
    chatbot = TerminalChatBot()
    chatbot.run()


if __name__ == "__main__":
    main()
