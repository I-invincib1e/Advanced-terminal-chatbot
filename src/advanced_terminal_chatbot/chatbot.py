"""
Main chatbot orchestrator module.
"""

import sys
import argparse
from typing import Optional
from .utils import ConfigManager, create_env_sample
from .provider import ProviderManager
from .chat import ChatSession


class TerminalChatBot:
    """Main chatbot orchestrator class."""
    
    def __init__(self):
        self.config = ConfigManager()
        self.provider_manager = ProviderManager(self.config)
        self.selected_model: Optional[str] = None
        self.selected_provider: Optional[str] = None
    
    def display_welcome(self) -> None:
        """Display the welcome message."""
        print("\n" + "═" * 70)
        print("🤖  ADVANCED TERMINAL CHATBOT  🤖".center(70))
        print("═" * 70)
        print("🌐 Direct API Support: OpenAI & Anthropic".center(70))
        print("🚀 Multi-Provider AI Models".center(70))
        print("💬 Intelligent Conversation with Memory".center(70))
        print("═" * 70)
        print()
    
    def get_api_keys(self) -> None:
        """Get API keys from user input if not in environment."""
        # Check what's already configured
        available_providers = self.config.get_available_providers()
        
        if not available_providers:
            print("❌ No API keys found in environment variables.")
            print("   Please set at least one of the following:")
            print("   - OPENAI_API_KEY for OpenAI models")
            print("   - ANTHROPIC_API_KEY for Anthropic models")
            print()
            
            # Ask for at least one API key
            while True:
                provider_choice = input("Which provider would you like to use? (openai/anthropic): ").strip().lower()
                if provider_choice in ['openai', 'o']:
                    api_key = input("Enter your OpenAI API key: ").strip()
                    if api_key:
                        # Set environment variable for this session
                        import os
                        os.environ['OPENAI_API_KEY'] = api_key
                        print("✅ OpenAI API key set for this session")
                        break
                    else:
                        print("❌ API key cannot be empty")
                elif provider_choice in ['anthropic', 'a']:
                    api_key = input("Enter your Anthropic API key: ").strip()
                    if api_key:
                        # Set environment variable for this session
                        import os
                        os.environ['ANTHROPIC_API_KEY'] = api_key
                        print("✅ Anthropic API key set for this session")
                        break
                    else:
                        print("❌ API key cannot be empty")
                else:
                    print("❌ Please enter 'openai' or 'anthropic'")
        else:
            # At least one provider is configured
            if len(available_providers) == 1:
                print(f"✅ Using configured {available_providers[0]} API key")
            else:
                print(f"✅ Multiple providers configured: {', '.join(available_providers)}")
                print("   You can select which one to use during setup")

    def setup_provider_and_model(self) -> None:
        """Set up the provider and model selection."""
        # Get default provider and model from config
        default_provider = self.config.get_default_provider()
        default_model = self.config.get_default_model()
        
        # Check if default provider is available
        available_providers = self.config.get_available_providers()
        if default_provider and default_provider in available_providers:
            print(f"📋 Using default provider: {default_provider}")
            self.selected_provider = default_provider
        else:
            # Auto-select if only one provider available, otherwise let user choose
            if len(available_providers) == 1:
                self.selected_provider = available_providers[0]
                print(f"✅ Auto-selected provider: {self.selected_provider}")
            else:
                self.selected_provider = self.provider_manager.select_provider()
        
        try:
            # Fetch models for the selected provider
            models = self.provider_manager.fetch_api_models(self.selected_provider)
            if not models:
                print("❌ Cannot proceed without available models.")
                print("   Please check your API key and internet connection.")
                sys.exit(1)
            
            # Check if default model is available for selected provider
            if default_model and self.provider_manager.validate_model(default_model, self.selected_provider):
                print(f"📋 Using default model: {default_model}")
                self.selected_model = default_model
            else:
                # Let user select model
                self.selected_model = self.provider_manager.select_api_model(models)
                
        except Exception as e:
            print(f"❌ Error during setup: {e}")
            sys.exit(1)

    def run(self) -> None:
        """Run the chatbot."""
        try:
            self.display_welcome()
            
            # Validate configuration and require at least one API key
            try:
                self.config.require_api_keys()
            except ValueError as e:
                print(f"\n❌ Configuration Error: {e}")
                print("\n�� Tip: Create a .env file with your API keys")
                print("   Run with --create-env to create a sample .env file")
                print("   You need at least one of: OPENAI_API_KEY or ANTHROPIC_API_KEY")
                sys.exit(1)
            
            # Get API keys if needed
            self.get_api_keys()
            
            # Setup provider and model
            self.setup_provider_and_model()
            
            # Create and start chat session
            chat_session = ChatSession(
                self.config,
                self.selected_model,
                self.selected_provider
            )
            chat_session.start_chat()
            
        except KeyboardInterrupt:
            print("\n\n👋 Chatbot interrupted. Goodbye!")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("   Please check your configuration and try again.")
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
        version='%(prog)s 1.0.0'
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
