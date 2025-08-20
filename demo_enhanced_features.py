#!/usr/bin/env python3
"""
Demo script to showcase the enhanced terminal chatbot features.
This script demonstrates the new UI enhancements and library integrations.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from advanced_terminal_chatbot.ui_enhancements import enhanced_ui
from rich.console import Console
import time

def main():
    """Demonstrate the enhanced features."""
    console = Console()
    
    # Initialize colorama for cross-platform support
    import colorama
    colorama.init()
    
    console.print("[bold green]🚀 Enhanced Terminal Chatbot Demo[/bold green]")
    console.print()
    
    # 1. Demonstrate ASCII Banner
    console.print("[bold cyan]1. ASCII Art Banner:[/bold cyan]")
    enhanced_ui.show_startup_banner()
    
    input("\nPress Enter to continue...")
    console.clear()
    
    # 2. Demonstrate Loading Spinners
    console.print("[bold cyan]2. Loading Spinners & Animations:[/bold cyan]")
    
    # Show thinking animation
    enhanced_ui.show_thinking_animation(duration=3.0)
    
    # Show custom spinner
    with enhanced_ui.create_loading_spinner("Processing your request...") as spinner:
        time.sleep(2)
        spinner.succeed("✅ Request processed successfully!")
    
    input("\nPress Enter to continue...")
    console.clear()
    
    # 3. Demonstrate Enhanced Prompts
    console.print("[bold cyan]3. Enhanced Interactive Prompts:[/bold cyan]")
    
    # Provider selection demo
    mock_providers = {
        "openai": True,
        "anthropic": True,
        "local": False
    }
    
    console.print("\n[yellow]Demo: Provider Selection[/yellow]")
    selected_provider = enhanced_ui.show_provider_selection(mock_providers)
    if selected_provider:
        console.print(f"[green]✅ You selected: {selected_provider}[/green]")
    
    # Model selection demo
    mock_models = ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet", "claude-3-haiku"]
    console.print("\n[yellow]Demo: Model Selection[/yellow]")
    selected_model = enhanced_ui.show_model_selection(mock_models, selected_provider or "openai")
    if selected_model:
        console.print(f"[green]✅ You selected: {selected_model}[/green]")
    
    input("\nPress Enter to continue...")
    console.clear()
    
    # 4. Demonstrate Enhanced Help
    console.print("[bold cyan]4. Enhanced Command Help:[/bold cyan]")
    enhanced_ui.show_command_help_enhanced({})
    
    input("\nPress Enter to continue...")
    console.clear()
    
    # 5. Demonstrate Status Tables and Panels
    console.print("[bold cyan]5. Status Display & Information Panels:[/bold cyan]")
    
    # Status table
    status_data = {
        "API Connection": True,
        "Streaming Mode": False,
        "History Enabled": True,
        "Model": "gpt-4",
        "Provider": "openai",
        "Session ID": "abc123...",
        "Messages": 15,
        "Temperature": 0.7
    }
    
    status_table = enhanced_ui.create_status_table(status_data, "Chatbot Status")
    console.print(status_table)
    
    console.print()
    
    # Different panel types
    enhanced_ui.show_success_panel("All systems operational!", "System Status")
    enhanced_ui.show_info_panel("New features have been successfully integrated.", "Feature Update")
    enhanced_ui.show_error_panel("This is just a demo error message.", "Demo Error")
    
    input("\nPress Enter to continue...")
    console.clear()
    
    # 6. Demonstrate Progress Bars
    console.print("[bold cyan]6. Progress Bars for Long Operations:[/bold cyan]")
    
    # Simulate file processing
    files = [f"file_{i}.py" for i in range(1, 21)]
    console.print("\n[yellow]Demo: Processing files...[/yellow]")
    
    for file in enhanced_ui.show_progress_bar(files, "Analyzing files"):
        # Simulate processing time
        time.sleep(0.1)
    
    console.print("\n[green]✅ File processing complete![/green]")
    
    input("\nPress Enter to continue...")
    console.clear()
    
    # 7. Final Summary
    console.print("[bold green]🎉 Enhanced Features Demo Complete![/bold green]")
    console.print()
    console.print("✨ [bold]New features integrated:[/bold]")
    console.print("  🎨 Beautiful ASCII art banners with pyfiglet")
    console.print("  🔄 Loading spinners and animations with halo")
    console.print("  📊 Interactive prompts with questionary")
    console.print("  🌈 Enhanced colors with colorama")
    console.print("  📈 Progress bars for long operations")
    console.print("  📋 Status tables and information panels")
    console.print("  🎯 Improved command help with categorization")
    console.print("  🔧 Enhanced logging with loguru")
    console.print()
    console.print("[bold blue]Ready to run the enhanced chatbot with:[/bold blue]")
    console.print("  [cyan]python main.py[/cyan]")
    console.print()

if __name__ == "__main__":
    main()
