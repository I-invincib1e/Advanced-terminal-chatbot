"""
Clipboard management for copying AI responses.
"""

import pyperclip
from typing import Optional
from rich.console import Console


class ClipboardManager:
    """Manages clipboard operations for the chatbot."""

    def __init__(self):
        self.console = Console()
        self.last_response = ""

    def set_last_response(self, response: str) -> None:
        """Store the last AI response."""
        self.last_response = response

    def copy_last_response(self) -> bool:
        """Copy the last AI response to clipboard."""
        if not self.last_response:
            self.console.print("[red]❌ No response to copy[/red]")
            return False

        try:
            # Clean the response (remove markdown formatting if needed)
            clean_response = self._clean_response(self.last_response)
            pyperclip.copy(clean_response)
            
            # Show preview of what was copied
            preview = clean_response[:100] + ("..." if len(clean_response) > 100 else "")
            self.console.print(f"[green]✅ Copied to clipboard:[/green] {preview}")
            return True
            
        except Exception as e:
            self.console.print(f"[red]❌ Failed to copy to clipboard: {str(e)}[/red]")
            return False

    def copy_text(self, text: str) -> bool:
        """Copy arbitrary text to clipboard."""
        try:
            pyperclip.copy(text)
            preview = text[:100] + ("..." if len(text) > 100 else "")
            self.console.print(f"[green]✅ Copied to clipboard:[/green] {preview}")
            return True
        except Exception as e:
            self.console.print(f"[red]❌ Failed to copy to clipboard: {str(e)}[/red]")
            return False

    def get_clipboard_content(self) -> Optional[str]:
        """Get current clipboard content."""
        try:
            return pyperclip.paste()
        except Exception as e:
            self.console.print(f"[red]❌ Failed to read clipboard: {str(e)}[/red]")
            return None

    def _clean_response(self, response: str) -> str:
        """Clean the response for clipboard copying."""
        # Remove error prefixes
        if response.startswith("❌"):
            return response[2:].strip()
        
        # Could add more cleaning logic here if needed
        # For example, removing certain markdown formatting
        
        return response.strip()

    def is_available(self) -> bool:
        """Check if clipboard functionality is available."""
        try:
            # Test clipboard access
            test_content = pyperclip.paste()
            return True
        except Exception:
            return False
