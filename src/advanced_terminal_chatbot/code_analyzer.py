"""
Code analysis and syntax highlighting for the terminal chatbot.
"""

import re
import ast
import json
import math
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import pygments
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import TerminalFormatter
from pygments.styles import get_style_by_name


class CodeAnalyzer:
    """Analyzes code for syntax highlighting, explanation, and improvements."""
    
    def __init__(self):
        """Initialize the code analyzer."""
        self.supported_languages = {
            'python': 'Python',
            'py': 'Python',
            'js': 'JavaScript',
            'javascript': 'JavaScript',
            'ts': 'TypeScript',
            'typescript': 'TypeScript',
            'java': 'Java',
            'cpp': 'C++',
            'c++': 'C++',
            'c': 'C',
            'cs': 'C#',
            'csharp': 'C#',
            'php': 'PHP',
            'rb': 'Ruby',
            'ruby': 'Ruby',
            'go': 'Go',
            'rs': 'Rust',
            'rust': 'Rust',
            'swift': 'Swift',
            'kt': 'Kotlin',
            'kotlin': 'Kotlin',
            'scala': 'Scala',
            'r': 'R',
            'sql': 'SQL',
            'html': 'HTML',
            'css': 'CSS',
            'scss': 'SCSS',
            'sass': 'Sass',
            'xml': 'XML',
            'json': 'JSON',
            'yaml': 'YAML',
            'yml': 'YAML',
            'toml': 'TOML',
            'ini': 'INI',
            'sh': 'Bash',
            'bash': 'Bash',
            'zsh': 'Bash',
            'fish': 'Fish',
            'ps1': 'PowerShell',
            'powershell': 'PowerShell',
            'bat': 'Batch',
            'cmd': 'Batch',
            'dockerfile': 'Dockerfile',
            'docker': 'Dockerfile',
            'makefile': 'Makefile',
            'mk': 'Makefile',
            'cmake': 'CMake',
            'txt': 'Text',
            'md': 'Markdown',
            'markdown': 'Markdown',
            # Extended language support
            'dart': 'Dart',
            'kotlin': 'Kotlin',
            'swift': 'Swift',
            'rs': 'Rust',
            'scala': 'Scala',
            'hs': 'Haskell',
            'lhs': 'Haskell',
            'erl': 'Erlang',
            'hrl': 'Erlang',
            'ex': 'Elixir',
            'exs': 'Elixir',
            'clj': 'Clojure',
            'cljs': 'Clojure',
            'cljc': 'Clojure',
            'fs': 'F#',
            'fsx': 'F#',
            'fsi': 'F#',
            'ml': 'OCaml',
            'mli': 'OCaml',
            'elm': 'Elm',
            'jl': 'Julia',
            'm': 'MATLAB',
            'f': 'Fortran',
            'for': 'Fortran',
            'f90': 'Fortran',
            'f95': 'Fortran',
            'cob': 'COBOL',
            'cbl': 'COBOL',
            'adb': 'Ada',
            'ads': 'Ada',
            'ada': 'Ada',
            'lua': 'Lua',
            'pl': 'Perl',
            'pm': 'Perl',
            'groovy': 'Groovy',
            'gy': 'Groovy',
            'gvy': 'Groovy',
            'gv': 'Groovy',
            'd': 'D',
            'nim': 'Nim',
            'cr': 'Crystal',
            'zig': 'Zig',
            'v': 'V',
            'sol': 'Solidity',
            'graphql': 'GraphQL',
            'gql': 'GraphQL',
            'proto': 'Protocol Buffers',
            'tf': 'Terraform',
            'tfvars': 'Terraform'
        }
        
        # Initialize Pygments formatter
        try:
            self.formatter = TerminalFormatter(style='monokai')
        except:
            # Fallback to default style if monokai is not available
            self.formatter = TerminalFormatter()
    
    def detect_language(self, code: str, filename: str = "") -> str:
        """Detect the programming language from code or filename."""
        # First try to detect from filename
        if filename:
            ext = Path(filename).suffix.lower().lstrip('.')
            if ext in self.supported_languages:
                return self.supported_languages[ext]
        
        # Try to detect from code content with enhanced heuristics
        code_lines = code.strip().split('\n')
        
        # Python detection
        if any(line.startswith('def ') or line.startswith('class ') or 
               line.startswith('import ') or line.startswith('from ') 
               for line in code_lines[:10]):
            return 'Python'
        
        # JavaScript/TypeScript detection
        if any('function ' in line or 'const ' in line or 'let ' in line or 
               'var ' in line or '=>' in line for line in code_lines[:10]):
            if any(': ' in line and ('interface ' in line or 'type ' in line) 
                   for line in code_lines[:10]):
                return 'TypeScript'
            return 'JavaScript'
        
        # Java detection
        if any('public class ' in line or 'public static void main' in line 
               for line in code_lines[:10]):
            return 'Java'
        
        # C/C++ detection
        if any('#include' in line or 'int main(' in line for line in code_lines[:10]):
            if any('cout' in line or 'cin' in line for line in code_lines):
                return 'C++'
            return 'C'
        
        # HTML detection
        if any(line.strip().startswith('<') and line.strip().endswith('>') 
               for line in code_lines[:5]):
            return 'HTML'
        
        # SQL detection
        if any(line.strip().upper().startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP'))
               for line in code_lines[:5]):
            return 'SQL'
        
        # Enhanced language detection with statistical analysis
        # Check for specific language patterns
        if any('fn ' in line and '{' in line for line in code_lines[:10]):
            # Could be Rust
            if any('let ' in line or 'mut ' in line for line in code_lines[:10]):
                return 'Rust'
        
        if any('func ' in line and '{' in line for line in code_lines[:10]):
            # Could be Go
            if any('package ' in line for line in code_lines[:5]):
                return 'Go'
        
        if any('sub ' in line or 'my $' in line for line in code_lines[:10]):
            return 'Perl'
        
        if any(':-' in line or ':-' in line for line in code_lines[:10]):
            # Could be Prolog
            return 'Prolog'
        
        if any('module ' in line and 'where' in line for line in code_lines[:10]):
            return 'Haskell'
        
        # Default to text
        return 'Text'
    
    def highlight_syntax(self, code: str, language: str = "auto") -> str:
        """Apply syntax highlighting to code."""
        if language == "auto":
            language = self.detect_language(code)
        
        try:
            if language in self.supported_languages:
                lexer = get_lexer_by_name(language)
            else:
                lexer = TextLexer()
            
            highlighted = pygments.highlight(code, lexer, self.formatter)
            return highlighted
        except Exception as e:
            # Fallback to plain text if highlighting fails
            return code
    
    def analyze_code_structure(self, code: str, language: str = "auto") -> Dict[str, Any]:
        """Analyze the structure of the code."""
        if language == "auto":
            language = self.detect_language(code)
        
        analysis = {
            'language': language,
            'lines': len(code.split('\n')),
            'characters': len(code),
            'complexity': 0,
            'functions': [],
            'classes': [],
            'imports': [],
            'comments': [],
            'issues': []
        }
        
        if language == 'Python':
            analysis.update(self._analyze_python(code))
        elif language in ['JavaScript', 'TypeScript']:
            analysis.update(self._analyze_javascript(code))
        elif language == 'Java':
            analysis.update(self._analyze_java(code))
        elif language == 'C++':
            analysis.update(self._analyze_cpp(code))
        elif language == 'Rust':
            analysis.update(self._analyze_rust(code))
        elif language == 'Go':
            analysis.update(self._analyze_go(code))
        
        return analysis
    
    def _analyze_python(self, code: str) -> Dict[str, Any]:
        """Analyze Python code structure."""
        analysis = {}
        try:
            tree = ast.parse(code)
            
            functions = []
            classes = []
            imports = []
            comments = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'decorators': [d.id for d in node.decorator_list if hasattr(d, 'id')]
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line': node.lineno,
                        'bases': [base.id for base in node.bases if hasattr(base, 'id')],
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        imports.append(f"from {node.module} import {', '.join([alias.name for alias in node.names])}")
            
            analysis = {
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'complexity': self._calculate_cyclomatic_complexity(tree)
            }
            
        except SyntaxError as e:
            analysis['issues'] = [f"Syntax error at line {e.lineno}: {e.text}"]
        except Exception as e:
            analysis['issues'] = [f"Analysis error: {str(e)}"]
        
        return analysis
    
    def _analyze_javascript(self, code: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript code structure."""
        analysis = {}
        
        # Simple regex-based analysis for JavaScript
        functions = re.findall(r'function\s+(\w+)\s*\(', code)
        arrow_functions = re.findall(r'(\w+)\s*=\s*\([^)]*\)\s*=>', code)
        const_functions = re.findall(r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>', code)
        let_functions = re.findall(r'let\s+(\w+)\s*=\s*\([^)]*\)\s*=>', code)
        classes = re.findall(r'class\s+(\w+)', code)
        imports = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', code)
        
        all_functions = functions + arrow_functions + const_functions + let_functions
        
        analysis = {
            'functions': [{'name': name, 'type': 'function'} for name in all_functions],
            'classes': [{'name': name, 'type': 'class'} for name in classes],
            'imports': imports,
            'complexity': len(all_functions) + len(classes)  # Simple complexity metric
        }
        
        return analysis
    
    def _analyze_java(self, code: str) -> Dict[str, Any]:
        """Analyze Java code structure."""
        analysis = {}
        
        try:
            # Simple regex-based analysis for Java
            classes = re.findall(r'public\s+class\s+(\w+)', code)
        except Exception as e:
            analysis["issues"] = [f"Error during Java analysis: {str(e)}"]
        methods = re.findall(r'public\s+(?:static\s+)?(?:void|int|String|boolean|double|float|long|char|byte|short)\s+(\w+)\s*\(', code)
        imports = re.findall(r'import\s+(.+?);', code)
        
        analysis = {
            'functions': [{'name': name, 'type': 'method'} for name in methods],
            'classes': [{'name': name, 'type': 'class'} for name in classes],
            'imports': imports,
            'complexity': len(methods) + len(classes)
        }
        
        return analysis
    
    def _analyze_cpp(self, code: str) -> Dict[str, Any]:
        """Analyze C++ code structure."""
        analysis = {}
        
        try:
            # Simple regex-based analysis for C++
            functions = re.findall(r'(?:int|void|double|float|char|bool|string)\s+(\w+)\s*\(', code)
            classes = re.findall(r'class\s+(\w+)', code)
            includes = re.findall(r'#include\s*[<"]([^>"]+)[>"]', code)
        except Exception as e:
            analysis["issues"] = [f"Error during C++ analysis: {str(e)}"]
        
        analysis = {
            'functions': [{'name': name, 'type': 'function'} for name in functions],
            'classes': [{'name': name, 'type': 'class'} for name in classes],
            'imports': includes,
            'complexity': len(functions) + len(classes)
        }
        
        return analysis
    
    def _analyze_rust(self, code: str) -> Dict[str, Any]:
        """Analyze Rust code structure."""
        analysis = {}
        
        try:
            # Simple regex-based analysis for Rust
            functions = re.findall(r'fn\s+(\w+)\s*\(', code)
            structs = re.findall(r'struct\s+(\w+)', code)
            impls = re.findall(r'impl\s+(\w+)', code)
            uses = re.findall(r'use\s+(.+?);', code)
        except Exception as e:
            analysis["issues"] = [f"Error during Rust analysis: {str(e)}"]
        
        analysis = {
            'functions': [{'name': name, 'type': 'function'} for name in functions],
            'classes': [{'name': name, 'type': 'struct'} for name in structs],
            'imports': uses,
            'complexity': len(functions) + len(structs)
        }
        
        return analysis
    
    def _analyze_go(self, code: str) -> Dict[str, Any]:
        """Analyze Go code structure."""
        analysis = {}
        
        try:
            # Simple regex-based analysis for Go
            functions = re.findall(r'func\s+(\w+)\s*\(', code)
            types = re.findall(r'type\s+(\w+)', code)
            imports = re.findall(r'import\s+(.+)', code)
        except Exception as e:
            analysis["issues"] = [f"Error during Go analysis: {str(e)}"]
        
        analysis = {
            'functions': [{'name': name, 'type': 'function'} for name in functions],
            'classes': [{'name': name, 'type': 'type'} for name in types],
            'imports': imports,
            'complexity': len(functions) + len(types)
        }
        
        return analysis
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for Python code."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def generate_code_explanation(self, code: str, language: str = "auto") -> str:
        """Generate a human-readable explanation of the code."""
        analysis = self.analyze_code_structure(code, language)
        
        explanation = f"📊 **Code Analysis for {analysis['language']}**\n\n"
        explanation += f"📏 **Structure**: {analysis['lines']} lines, {analysis['characters']} characters\n"
        explanation += f"🔧 **Complexity**: {analysis['complexity']} (cyclomatic complexity)\n\n"
        
        if analysis['imports']:
            explanation += f"📦 **Imports**: {', '.join(analysis['imports'][:5])}"
            if len(analysis['imports']) > 5:
                explanation += f" and {len(analysis['imports']) - 5} more...\n\n"
            else:
                explanation += "\n\n"
        
        if analysis['classes']:
            explanation += f"🏗️  **Classes**: {len(analysis['classes'])} found\n"
            for cls in analysis['classes'][:3]:
                explanation += f"   - `{cls['name']}`"
                if 'methods' in cls and cls['methods']:
                    explanation += f" with {len(cls['methods'])} methods"
                explanation += "\n"
            explanation += "\n"
        
        if analysis['functions']:
            explanation += f"⚙️  **Functions**: {len(analysis['functions'])} found\n"
            for func in analysis['functions'][:3]:
                explanation += f"   - `{func['name']}`"
                if 'args' in func and func['args']:
                    explanation += f"({', '.join(func['args'])})"
                explanation += "\n"
            explanation += "\n"
        
        if analysis['issues']:
            explanation += f"⚠️  **Issues Found**:\n"
            for issue in analysis['issues']:
                explanation += f"   - {issue}\n"
        
        return explanation
    
    def suggest_improvements(self, code: str, language: str = "auto") -> List[str]:
        """Suggest improvements for the code."""
        suggestions = []
        analysis = self.analyze_code_structure(code, language)
        
        # General suggestions
        if analysis['complexity'] > 10:
            suggestions.append("🔴 Consider breaking down complex functions into smaller, more manageable pieces")
        
        if analysis['lines'] > 100:
            suggestions.append("🟡 Code is quite long - consider splitting into multiple files or functions")
        
        if len(analysis['functions']) > 20:
            suggestions.append("🟡 Many functions detected - consider organizing into classes or modules")
        
        # Language-specific suggestions
        if language == 'Python':
            if not any('def ' in line for line in code.split('\n')):
                suggestions.append("💡 Consider adding a main function or entry point")
            
            if 'import *' in code:
                suggestions.append("⚠️  Avoid wildcard imports - import specific modules instead")
        
        elif language in ['JavaScript', 'TypeScript']:
            if 'var ' in code:
                suggestions.append("💡 Use 'const' or 'let' instead of 'var' for better scoping")
            
            if 'function ' in code and '=>' in code:
                suggestions.append("💡 Consider using consistent function syntax (either traditional or arrow functions)")
        
        elif language == 'Java':
            if 'System.out.println' in code:
                suggestions.append("💡 Consider using a logging framework instead of System.out.println")
        
        elif language == 'C++':
            if 'using namespace std' in code:
                suggestions.append("⚠️  Avoid 'using namespace std' in header files")
        
        elif language == 'Rust':
            if 'unwrap()' in code:
                suggestions.append("💡 Consider using proper error handling instead of unwrap()")
        
        if not suggestions:
            suggestions.append("✅ Code looks well-structured! No major improvements needed.")
        
        return suggestions


def format_code_block(code: str, language: str = "auto", show_analysis: bool = True) -> str:
    """Format code with syntax highlighting and optional analysis."""
    analyzer = CodeAnalyzer()
    
    # Detect language if auto
    if language == "auto":
        language = analyzer.detect_language(code)
    
    # Apply syntax highlighting
    highlighted_code = analyzer.highlight_syntax(code, language)
    
    # Format the output
    output = f"```{language}\n{highlighted_code}\n```\n\n"
    
    if show_analysis:
        explanation = analyzer.generate_code_explanation(code, language)
        output += explanation + "\n\n"
        
        suggestions = analyzer.suggest_improvements(code, language)
        if suggestions:
            output += "💡 **Suggestions**:\n"
            for suggestion in suggestions:
                output += f"   {suggestion}\n"
    
    return output
