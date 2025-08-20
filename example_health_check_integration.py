"""
Example integration of health check feature into the main chatbot.
This shows how to add the --health-check command line option.
"""

import argparse
import sys
from src.advanced_terminal_chatbot.features.health_check import run_health_check


def main_with_health_check():
    """Enhanced main function with health check support."""
    parser = argparse.ArgumentParser(
        description="Advanced Terminal Chatbot with health check support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start interactive chatbot
  %(prog)s --health-check     # Run system health check
  %(prog)s --create-env       # Create sample .env file
  %(prog)s --help             # Show this help message

Health Check:
  The --health-check option verifies:
  • Python version compatibility (3.8+)
  • Required dependencies installation
  • API key configuration
  • Database connectivity
  • Clipboard functionality

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
        '--health-check',
        action='store_true',
        help='Run comprehensive system health check'
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
    
    # Handle health check
    if args.health_check:
        run_health_check()
        return
    
    # Handle env creation
    if args.create_env:
        from src.advanced_terminal_chatbot.utils import create_env_sample
        create_env_sample()
        return
    
    # Start the regular chatbot
    from src.advanced_terminal_chatbot.chatbot import TerminalChatBot
    chatbot = TerminalChatBot()
    chatbot.run()


if __name__ == "__main__":
    main_with_health_check()
