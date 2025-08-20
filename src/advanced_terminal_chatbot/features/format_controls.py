"""
Response format controls for optimizing AI responses.
"""

from typing import Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class FormatController:
    """Manages response format presets and controls."""
    
    def __init__(self):
        self.console = Console()
        self.current_format = "default"
        self.formats = {
            'default': {
                'name': 'Default',
                'description': 'Balanced responses with explanations',
                'prompt_modifier': '',
                'icon': '💬'
            },
            'brief': {
                'name': 'Brief',
                'description': 'Concise, bullet-point responses',
                'prompt_modifier': 'Please provide a brief, concise response using bullet points where appropriate. Focus on key information only.',
                'icon': '⚡'
            },
            'detailed': {
                'name': 'Detailed',
                'description': 'Comprehensive explanations with examples',
                'prompt_modifier': 'Please provide a detailed, comprehensive response with examples, explanations, and thorough coverage of the topic.',
                'icon': '📚'
            },
            'code': {
                'name': 'Code-Focused',
                'description': 'Minimal explanations, maximum code',
                'prompt_modifier': 'Focus primarily on code examples with minimal explanations. Provide working code solutions with brief comments.',
                'icon': '💻'
            },
            'teaching': {
                'name': 'Teaching',
                'description': 'Educational style with step-by-step breakdowns',
                'prompt_modifier': 'Explain in a teaching style with step-by-step breakdowns, learning objectives, and educational examples. Make it beginner-friendly.',
                'icon': '🎓'
            },
            'professional': {
                'name': 'Professional',
                'description': 'Formal, business-appropriate tone',
                'prompt_modifier': 'Use a formal, professional tone suitable for business environments. Be precise and authoritative.',
                'icon': '💼'
            },
            'creative': {
                'name': 'Creative',
                'description': 'Engaging, creative explanations',
                'prompt_modifier': 'Be creative and engaging in your explanations. Use analogies, storytelling, and interesting examples to make concepts memorable.',
                'icon': '🎨'
            },
            'debug': {
                'name': 'Debug Mode',
                'description': 'Systematic debugging approach',
                'prompt_modifier': 'Approach this as a systematic debugging session. Provide step-by-step analysis, potential causes, and methodical solutions.',
                'icon': '🔍'
            }
        }
    
    def set_format(self, format_name: str) -> bool:
        """Set the current response format."""
        if format_name in self.formats:
            self.current_format = format_name
            return True
        return False
    
    def get_current_format(self) -> str:
        """Get the current format name."""
        return self.current_format
    
    def get_format_info(self, format_name: Optional[str] = None) -> Dict:
        """Get information about a format or current format."""
        format_name = format_name or self.current_format
        return self.formats.get(format_name, self.formats['default'])
    
    def get_prompt_modifier(self) -> str:
        """Get the prompt modifier for the current format."""
        format_info = self.get_format_info()
        return format_info.get('prompt_modifier', '')
    
    def list_formats(self) -> None:
        """Display all available formats."""
        self.console.print("\n[bold cyan]🎨 Response Format Controls[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Format", style="white")
        table.add_column("Description", style="dim")
        table.add_column("Status", style="green")
        
        for key, format_info in self.formats.items():
            status = "✅ Active" if key == self.current_format else ""
            table.add_row(
                f"/format {key}",
                f"{format_info['icon']} {format_info['name']}",
                format_info['description'],
                status
            )
        
        self.console.print(table)
        
        current_info = self.get_format_info()
        self.console.print(f"\n[bold green]Current Format:[/bold green] {current_info['icon']} {current_info['name']}")
        
        if current_info['prompt_modifier']:
            self.console.print(Panel(
                current_info['prompt_modifier'],
                title="[bold cyan]Current Prompt Modifier[/bold cyan]",
                border_style="cyan"
            ))
        
        self.console.print("\n[dim]💡 Usage: /format <name> to change format")
        self.console.print("💡 Example: /format brief[/dim]")
    
    def show_format_preview(self, format_name: str) -> None:
        """Show a preview of a specific format."""
        if format_name not in self.formats:
            self.console.print(f"[bold red]❌ Format '{format_name}' not found.[/bold red]")
            self.console.print("[dim]Use /formats to see all available formats.[/dim]")
            return
        
        format_info = self.formats[format_name]
        
        self.console.print(Panel(
            f"**Name:** {format_info['icon']} {format_info['name']}\n\n"
            f"**Description:** {format_info['description']}\n\n"
            f"**Prompt Modifier:**\n{format_info['prompt_modifier'] or 'None (default behavior)'}",
            title=f"[bold cyan]🎨 Format Preview: {format_name}[/bold cyan]",
            border_style="cyan"
        ))
    
    def reset_format(self) -> None:
        """Reset to default format."""
        self.current_format = "default"
        self.console.print("[bold green]✅ Format reset to default.[/bold green]")
    
    def get_format_indicator(self) -> str:
        """Get a format indicator for the UI."""
        if self.current_format == "default":
            return ""
        
        format_info = self.get_format_info()
        return f" [{format_info['icon']} {format_info['name']}]"
    
    def apply_format_to_prompt(self, user_prompt: str) -> str:
        """Apply current format modifier to user prompt."""
        modifier = self.get_prompt_modifier()
        if not modifier:
            return user_prompt
        
        # Add format instruction at the beginning
        return f"{modifier}\n\nUser request: {user_prompt}"
    
    def get_available_formats(self) -> list:
        """Get list of format names for tab completion."""
        return list(self.formats.keys())
    
    def add_custom_format(self, name: str, description: str, prompt_modifier: str, icon: str = "🔧") -> bool:
        """Add a custom format."""
        if name in self.formats:
            return False  # Format already exists
        
        self.formats[name] = {
            'name': name.title(),
            'description': description,
            'prompt_modifier': prompt_modifier,
            'icon': icon,
            'custom': True
        }
        return True
    
    def remove_custom_format(self, name: str) -> bool:
        """Remove a custom format (not built-in ones)."""
        if name not in self.formats:
            return False
        
        format_info = self.formats[name]
        if not format_info.get('custom', False):
            return False  # Can't remove built-in formats
        
        # Reset to default if removing current format
        if self.current_format == name:
            self.current_format = "default"
        
        del self.formats[name]
        return True


# Global format controller instance
format_controller = FormatController()


def set_format(name: str) -> bool:
    """Convenience function to set format."""
    return format_controller.set_format(name)


def get_current_format() -> str:
    """Convenience function to get current format."""
    return format_controller.get_current_format()


def list_formats() -> None:
    """Convenience function to list formats."""
    format_controller.list_formats()


def apply_format_to_prompt(prompt: str) -> str:
    """Convenience function to apply format to prompt."""
    return format_controller.apply_format_to_prompt(prompt)


def get_format_indicator() -> str:
    """Convenience function to get format indicator."""
    return format_controller.get_format_indicator()
