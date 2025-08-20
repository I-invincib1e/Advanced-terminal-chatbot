"""
Template system for predefined conversation starters.
"""

from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class TemplateManager:
    """Manages conversation templates and quick starters."""
    
    def __init__(self):
        self.console = Console()
        self.templates = {
            'debug': {
                'name': 'Debug Help',
                'description': 'Get help debugging code issues',
                'template': 'Help me debug this code issue. Here\'s what\'s happening:\n\n[Describe the problem]\n\nCode:\n```\n[Your code here]\n```\n\nExpected behavior: [What should happen]\nActual behavior: [What actually happens]\nError message (if any): [Error details]'
            },
            'review': {
                'name': 'Code Review',
                'description': 'Request code review and best practices',
                'template': 'Please review this code for best practices, security, optimization, and maintainability:\n\n```\n[Your code here]\n```\n\nSpecific areas to focus on:\n- Performance optimization\n- Security vulnerabilities\n- Code readability\n- Best practices\n- Potential bugs'
            },
            'explain': {
                'name': 'Concept Explanation',
                'description': 'Get simple explanations with examples',
                'template': 'Explain this concept in simple terms with practical examples:\n\n[Concept or topic]\n\nPlease include:\n- Clear, beginner-friendly explanation\n- Real-world examples\n- Common use cases\n- Key benefits and drawbacks'
            },
            'optimize': {
                'name': 'Code Optimization',
                'description': 'Get suggestions for performance improvements',
                'template': 'How can I optimize this code for better performance, memory usage, and efficiency?\n\n```\n[Your code here]\n```\n\nCurrent performance concerns:\n- [Describe performance issues]\n- [Mention constraints or requirements]\n\nPlease suggest improvements for:\n- Speed optimization\n- Memory efficiency\n- Code complexity reduction'
            },
            'translate': {
                'name': 'Code Translation',
                'description': 'Convert code between programming languages',
                'template': 'Translate this code from [SOURCE_LANGUAGE] to [TARGET_LANGUAGE]:\n\n```[SOURCE_LANGUAGE]\n[Your code here]\n```\n\nPlease ensure:\n- Equivalent functionality\n- Idiomatic code in target language\n- Proper error handling\n- Comments explaining key differences'
            },
            'learn': {
                'name': 'Learning Path',
                'description': 'Get structured learning recommendations',
                'template': 'I want to learn [TOPIC/TECHNOLOGY]. Please provide:\n\n- Learning roadmap with clear steps\n- Essential concepts to master first\n- Recommended resources (books, tutorials, projects)\n- Practical exercises to reinforce learning\n- Common pitfalls to avoid\n\nMy current level: [Beginner/Intermediate/Advanced]\nTime available: [Hours per week]'
            },
            'architecture': {
                'name': 'System Design',
                'description': 'Get help with software architecture',
                'template': 'Help me design the architecture for this system:\n\n**Requirements:**\n- [List key requirements]\n- [Performance needs]\n- [Scale expectations]\n- [Technology constraints]\n\n**Current thoughts:**\n[Your initial ideas]\n\nPlease suggest:\n- Overall architecture pattern\n- Technology stack recommendations\n- Scalability considerations\n- Security best practices'
            },
            'troubleshoot': {
                'name': 'Troubleshooting',
                'description': 'Systematic problem-solving assistance',
                'template': 'I\'m having trouble with [SYSTEM/TECHNOLOGY]. Here are the details:\n\n**Problem:** [Brief description]\n\n**Environment:**\n- OS: [Operating system]\n- Version: [Software/framework version]\n- Setup: [Relevant configuration]\n\n**Steps to reproduce:**\n1. [Step 1]\n2. [Step 2]\n3. [Step 3]\n\n**What I\'ve tried:**\n- [Previous attempts]\n\n**Logs/Error messages:**\n```\n[Error details]\n```'
            }
        }
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Get a template by name."""
        if template_name in self.templates:
            return self.templates[template_name]['template']
        return None
    
    def list_templates(self) -> None:
        """Display all available templates."""
        self.console.print("\n[bold cyan]📝 Available Templates[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Description", style="dim")
        
        for key, template in self.templates.items():
            table.add_row(
                f"/template {key}",
                template['name'],
                template['description']
            )
        
        self.console.print(table)
        
        self.console.print("\n[dim]💡 Usage: /template <name> to use a template")
        self.console.print("💡 Example: /template debug[/dim]")
    
    def show_template_preview(self, template_name: str) -> None:
        """Show a preview of a specific template."""
        if template_name not in self.templates:
            self.console.print(f"[bold red]❌ Template '{template_name}' not found.[/bold red]")
            self.console.print("[dim]Use /templates to see all available templates.[/dim]")
            return
        
        template_info = self.templates[template_name]
        
        self.console.print(Panel(
            template_info['template'],
            title=f"[bold cyan]📝 Template: {template_info['name']}[/bold cyan]",
            subtitle=f"[dim]{template_info['description']}[/dim]",
            border_style="cyan"
        ))
        
        self.console.print("\n[dim]💡 This template will be loaded into your input. Edit as needed before sending.[/dim]")
    
    def get_template_names(self) -> List[str]:
        """Get list of all template names for tab completion."""
        return list(self.templates.keys())
    
    def search_templates(self, query: str) -> Dict[str, dict]:
        """Search templates by name or description."""
        results = {}
        query_lower = query.lower()
        
        for key, template in self.templates.items():
            if (query_lower in key.lower() or 
                query_lower in template['name'].lower() or 
                query_lower in template['description'].lower()):
                results[key] = template
        
        return results
    
    def add_custom_template(self, name: str, description: str, template: str) -> bool:
        """Add a custom user template."""
        if name in self.templates:
            return False  # Template already exists
        
        self.templates[name] = {
            'name': name.title(),
            'description': description,
            'template': template,
            'custom': True
        }
        return True
    
    def remove_custom_template(self, name: str) -> bool:
        """Remove a custom template (not built-in ones)."""
        if name not in self.templates:
            return False
        
        template_info = self.templates[name]
        if not template_info.get('custom', False):
            return False  # Can't remove built-in templates
        
        del self.templates[name]
        return True


# Global template manager instance
template_manager = TemplateManager()


def get_template(name: str) -> Optional[str]:
    """Convenience function to get a template."""
    return template_manager.get_template(name)


def list_templates() -> None:
    """Convenience function to list templates."""
    template_manager.list_templates()


def show_template_preview(name: str) -> None:
    """Convenience function to show template preview."""
    template_manager.show_template_preview(name)
