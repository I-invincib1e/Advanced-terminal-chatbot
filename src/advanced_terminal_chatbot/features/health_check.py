"""
Health check functionality for the Advanced Terminal Chatbot.
"""

import os
import sys
import importlib
from typing import Dict, List, Tuple, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from ..utils import ConfigManager


class HealthChecker:
    """System health check and diagnostics."""
    
    def __init__(self):
        self.console = Console()
        self.config = ConfigManager()
    
    def check_python_version(self) -> Tuple[bool, str]:
        """Check if Python version is compatible."""
        version = sys.version_info
        if version >= (3, 8):
            return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
        return False, f"❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)"
    
    def check_dependencies(self) -> Dict[str, Tuple[bool, str]]:
        """Check if all required dependencies are installed."""
        required_deps = [
            'requests',
            'python-dotenv',
            'pygments',
            'rich',
            'pyperclip',
            'prompt_toolkit',
            'questionary',
            'pyfiglet',
            'halo',
            'tqdm',
            'colorama',
            'loguru'
        ]
        
        results = {}
        for dep in required_deps:
            try:
                importlib.import_module(dep.replace('-', '_'))
                results[dep] = (True, "✅ Installed")
            except ImportError:
                results[dep] = (False, "❌ Missing")
        
        return results
    
    def check_api_keys(self) -> Dict[str, Tuple[bool, str]]:
        """Check if API keys are configured."""
        api_checks = {}
        
        # Check OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            if openai_key.startswith('sk-') and len(openai_key) > 20:
                api_checks['OpenAI'] = (True, "✅ Configured")
            else:
                api_checks['OpenAI'] = (False, "❌ Invalid format")
        else:
            api_checks['OpenAI'] = (False, "❌ Not set")
        
        # Check Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            if anthropic_key.startswith('sk-ant-') and len(anthropic_key) > 20:
                api_checks['Anthropic'] = (True, "✅ Configured")
            else:
                api_checks['Anthropic'] = (False, "❌ Invalid format")
        else:
            api_checks['Anthropic'] = (False, "❌ Not set")
        
        return api_checks
    
    def check_database(self) -> Tuple[bool, str]:
        """Check if the database can be accessed."""
        try:
            from ..database import DatabaseManager
            db = DatabaseManager("chatbot_history.db")
            # Try to perform a simple query to test database connectivity
            db.fetch_one("SELECT 1")
            db.close()
            return True, "✅ Database accessible"
        except Exception as e:
            return False, f"❌ Database error: {str(e)[:50]}..."
    
    def check_clipboard(self) -> Tuple[bool, str]:
        """Check if clipboard functionality works."""
        try:
            import pyperclip
            # Test clipboard by setting and getting a test value
            test_text = "health_check_test"
            pyperclip.copy(test_text)
            if pyperclip.paste() == test_text:
                return True, "✅ Clipboard working"
            else:
                return False, "❌ Clipboard read/write failed"
        except Exception as e:
            return False, f"❌ Clipboard error: {str(e)[:30]}..."
    
    def run_full_health_check(self) -> None:
        """Run comprehensive health check and display results."""
        self.console.print("\n[bold cyan]🔍 Running System Health Check...[/bold cyan]\n")
        
        # Python version check
        python_ok, python_msg = self.check_python_version()
        
        # Dependencies check
        deps = self.check_dependencies()
        deps_ok = all(status for status, _ in deps.values())
        
        # API keys check
        api_keys = self.check_api_keys()
        api_ok = any(status for status, _ in api_keys.values())
        
        # Database check
        db_ok, db_msg = self.check_database()
        
        # Clipboard check
        clipboard_ok, clipboard_msg = self.check_clipboard()
        
        # Overall status
        overall_ok = python_ok and deps_ok and api_ok and db_ok
        
        # Create status table
        table = Table(title="System Health Status", show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan", no_wrap=True)
        table.add_column("Status", style="white")
        table.add_column("Details", style="dim")
        
        # Add rows
        table.add_row("Python Version", "✅ OK" if python_ok else "❌ FAIL", python_msg)
        
        # Dependencies summary
        deps_passed = sum(1 for status, _ in deps.values() if status)
        deps_total = len(deps)
        deps_summary = f"{deps_passed}/{deps_total} installed"
        table.add_row("Dependencies", "✅ OK" if deps_ok else "❌ FAIL", deps_summary)
        
        # API Keys summary
        api_configured = sum(1 for status, _ in api_keys.values() if status)
        api_summary = f"{api_configured} provider(s) configured"
        table.add_row("API Keys", "✅ OK" if api_ok else "❌ FAIL", api_summary)
        
        table.add_row("Database", "✅ OK" if db_ok else "❌ FAIL", db_msg)
        table.add_row("Clipboard", "✅ OK" if clipboard_ok else "❌ WARN", clipboard_msg)
        
        self.console.print(table)
        
        # Show detailed issues if any
        if not overall_ok:
            self.console.print("\n[bold red]⚠️  Issues Found:[/bold red]")
            
            if not deps_ok:
                self.console.print("\n[yellow]Missing Dependencies:[/yellow]")
                for dep, (status, msg) in deps.items():
                    if not status:
                        self.console.print(f"  • {dep}: {msg}")
                self.console.print("  [dim]Fix: pip install -r requirements.txt[/dim]")
            
            if not api_ok:
                self.console.print("\n[yellow]API Key Issues:[/yellow]")
                for provider, (status, msg) in api_keys.items():
                    if not status:
                        self.console.print(f"  • {provider}: {msg}")
                self.console.print("  [dim]Fix: Set API keys in .env file[/dim]")
            
            if not db_ok:
                self.console.print(f"\n[yellow]Database Issue:[/yellow]")
                self.console.print(f"  • {db_msg}")
        
        # Overall result
        if overall_ok:
            self.console.print(Panel(
                "[bold green]🎉 All systems operational! Your chatbot is ready to use.[/bold green]",
                title="Health Check Complete",
                border_style="green"
            ))
        else:
            self.console.print(Panel(
                "[bold yellow]⚠️  Some issues found. Please address them for optimal performance.[/bold yellow]",
                title="Health Check Complete",
                border_style="yellow"
            ))
    
    def quick_status(self) -> bool:
        """Quick health check returning True if system is ready."""
        try:
            python_ok, _ = self.check_python_version()
            api_keys = self.check_api_keys()
            api_ok = any(status for status, _ in api_keys.values())
            db_ok, _ = self.check_database()
            
            return python_ok and api_ok and db_ok
        except:
            return False


def run_health_check():
    """Convenience function to run health check."""
    checker = HealthChecker()
    checker.run_full_health_check()


if __name__ == "__main__":
    run_health_check()
