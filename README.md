<div align="center">

# 🤖 Advanced Terminal Chatbot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/Neorex80/advanced-terminal-chatbot)
[![Tests](https://github.com/Neorex80/advanced-terminal-chatbot/actions/workflows/python-app.yml/badge.svg)](https://github.com/Neorex80/advanced-terminal-chatbot/actions)

> **A powerful, modular terminal-based chatbot with direct support for OpenAI and Anthropic APIs, featuring advanced code analysis, context management, and conversation branching**

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🔧 Configuration](#-configuration) • [🧪 Testing](#-testing)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Code Analysis Features](#-code-analysis-features)
- [Context Management](#-context-management)
- [Conversation Branching](#-conversation-branching)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Architecture](#-architecture)
- [Testing](#-testing)
- [Package Information](#-package-information)
- [API Compatibility](#-api-compatibility)
- [Error Handling](#-error-handling)
- [Contributing](#-contributing)
- [License](#-license)
- [Support & Troubleshooting](#-support--troubleshooting)
- [Star the Project](#-star-the-project)
- [Links](#-links)

---

## ✨ Features

| Category | Features |
|----------|----------|
| 🤖 **AI Integration** | Direct OpenAI & Anthropic API support, Multi-model selection, Conversation memory |
| 🔍 **Code Analysis** | Syntax highlighting, Language detection, Code structure analysis, Improvement suggestions |
| 🌿 **Context Management** | Multiple conversation contexts, Memory storage, Context switching, Relevance scoring |
| 🗂️ **Conversation Branching** | Multiple conversation threads, Branch forking, Thread merging, Navigation history |
| 🏗️ **Architecture** | Modular design, Clean separation of concerns, Extensible provider system |
| 🔧 **Configuration** | Environment-based config, .env file support, Customizable settings |
| 🧪 **Quality** | Comprehensive testing, Error handling, Type hints, Code coverage |
| 📦 **Deployment** | Pip installable, Cross-platform, Minimal dependencies |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key and/or Anthropic API key

### Installation

<details>
<summary><b>Option 1: From Source (Recommended)</b></summary>

```bash
# Clone the repository
git clone https://github.com/Neorex80/advanced-terminal-chatbot.git
cd advanced-terminal-chatbot

# Install dependencies
pip install -r requirements.txt

# Create environment file
python main.py --create-env

# Edit .env with your API keys
# Then run the chatbot
python main.py
```

</details>

<details>
<summary><b>Option 2: Pip Install</b></summary>

```bash
# Install from PyPI (when available)
pip install advanced-terminal-chatbot

# Run the chatbot
advanced-chatbot
```

</details>

---

## 🔍 Code Analysis Features

The chatbot includes powerful code analysis capabilities:

### Syntax Highlighting
- **Automatic Language Detection**: Detects programming languages from code content or file extensions
- **Rich Syntax Highlighting**: Uses Pygments for beautiful, colored code output
- **Multiple Language Support**: Python, JavaScript, TypeScript, Java, C++, HTML, CSS, SQL, and more

### Code Structure Analysis
- **Function & Class Detection**: Identifies functions, classes, methods, and their relationships
- **Complexity Metrics**: Calculates cyclomatic complexity for Python code
- **Import Analysis**: Tracks dependencies and import statements
- **Code Quality Assessment**: Provides suggestions for improvements

### Usage Examples
```bash
# Analyze code with full analysis
/analyze def hello(): print("Hello World")

# Syntax highlighting only
/highlight function greet(name) { return `Hello ${name}!`; }

# Language-specific analysis
/analyze class Calculator: def add(self, a, b): return a + b
```

---

## 🌿 Context Management

### Conversation Contexts
- **Multiple Contexts**: Create separate conversation contexts for different topics
- **Context Switching**: Seamlessly switch between different conversation threads
- **Context Metadata**: Store descriptions, tags, and custom metadata
- **Context Export**: Export contexts in JSON or Markdown format

### Memory System
- **Persistent Memory**: Store important information across sessions
- **Memory Types**: Facts, preferences, instructions, and examples
- **Importance Scoring**: Rate memories by importance (0.0 to 1.0)
- **Smart Search**: Find relevant memories using semantic search

### Usage Examples
```bash
# Create a new context
/context create Python Development Working on Python projects python,development

# Switch to a context
/context switch ctx_abc123

# Add a memory
/memory add "Python is great for data analysis" 0.8 python,data fact

# Search memories
/memory search python
```

---

## 🗂️ Conversation Branching

### Branch Management
- **Multiple Branches**: Create separate conversation branches within contexts
- **Branch Forking**: Fork existing branches to explore different conversation paths
- **Branch Merging**: Combine multiple branches with different merge strategies
- **Branch Navigation**: Navigate through branch history and tree structure

### Thread Organization
- **Hierarchical Structure**: Organize conversations in parent-child relationships
- **Message Tracking**: Keep track of messages per branch
- **Branch Metadata**: Store tags, descriptions, and custom data
- **Export Capabilities**: Export branches in multiple formats

### Usage Examples
```bash
# Create a new branch
/branch create Technical Questions technical,help

# Switch to a branch
/branch switch branch_abc123

# Fork current branch
/branch fork Side Discussion

# View branch tree
/branch tree
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file in your project directory:

```bash
# Required: At least one API key
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Custom API base URLs
OPENAI_BASE_URL=https://api.openai.com/v1
ANTHROPIC_BASE_URL=https://api.anthropic.com/v1

# Optional: Default settings
DEFAULT_PROVIDER=OpenAI
DEFAULT_MODEL=gpt-4o
MAX_TOKENS=1000
TEMPERATURE=0.7
```

### Quick Setup Commands
```bash
# Create sample .env file
python main.py --create-env

# Show help
python main.py --help

# Show version
python main.py --version
```

---

## 📖 Usage Guide

### Basic Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show help information | `/help` |
| `/clear` | Clear conversation history | `/clear` |
| `/history` | Show conversation history | `/history` |
| `/stream` | Toggle streaming mode | `/stream` |
| `/quit` | Exit the chat | `/quit` |

### Code Analysis Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/analyze` | Analyze code with syntax highlighting | `/analyze def hello(): pass` |
| `/highlight` | Apply syntax highlighting only | `/highlight print("Hello")` |

### Context Management Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/context create` | Create new context | `/context create MyProject Description` |
| `/context switch` | Switch to context | `/context switch ctx_123` |
| `/context info` | Show current context info | `/context info` |

### Branch Management Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/branch create` | Create new branch | `/branch create Feature1 feature,new` |
| `/branch switch` | Switch to branch | `/branch switch branch_123` |
| `/branch fork` | Fork current branch | `/branch fork Experiment` |
| `/branch tree` | Show branch tree | `/branch tree` |

### Memory Management Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/memory add` | Add new memory | `/memory add "Important fact" 0.9 tag1,tag2 fact` |
| `/memory search` | Search memories | `/memory search python` |

### System Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/stats` | Show system statistics | `/stats` |

---

## 🏗️ Architecture

### Module Structure
```
src/advanced_terminal_chatbot/
├── __init__.py              # Package initialization
├── chatbot.py               # Main orchestrator
├── provider.py              # AI provider management
├── chat.py                  # Chat session and API communication
├── utils.py                 # Configuration and utilities
├── code_analyzer.py         # Code analysis and syntax highlighting
├── context_manager.py       # Context and memory management
└── conversation_brancher.py # Conversation branching system
```

### Module Responsibilities
| Module | Responsibility |
|--------|----------------|
| `chatbot.py` | Main application flow, user interaction |
| `provider.py` | AI provider selection, model management |
| `chat.py` | Chat sessions, API communication, command processing |
| `utils.py` | Configuration loading, environment management |
| `code_analyzer.py` | Code analysis, syntax highlighting, language detection |
| `context_manager.py` | Context switching, memory storage, relevance scoring |
| `conversation_brancher.py` | Branch management, thread organization |

---

## 🧪 Testing

### Running Tests
```bash
# Run all tests with coverage
python run_tests.py

# Run specific test file
python -m unittest tests.test_chat -v

# Run with pytest (if installed)
python -m pytest tests/ -v
```

### Test Coverage
The test suite covers:
- ✅ API communication (OpenAI & Anthropic)
- ✅ Code analysis and syntax highlighting
- ✅ Context management and memory system
- ✅ Conversation branching and thread management
- ✅ Configuration management
- ✅ Error handling and edge cases

---

## 📦 Package Information

### Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | ≥2.25.0 | HTTP client for API communication |
| `python-dotenv` | ≥0.19.0 | Environment variable management |
| `pygments` | ≥2.15.0 | Syntax highlighting and code analysis |

### Development Dependencies
| Package | Purpose |
|---------|---------|
| `pytest` | Testing framework |
| `pytest-cov` | Test coverage reporting |
| `black` | Code formatting |
| `flake8` | Linting |
| `mypy` | Type checking |

---

## 🔌 API Compatibility

### OpenAI API
- **Models**: GPT-4, GPT-3.5, GPT-4o, GPT-4o-mini
- **Endpoints**: `/v1/chat/completions`
- **Features**: Streaming, function calling, temperature control
- **Authentication**: Bearer token

### Anthropic API
- **Models**: Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus
- **Endpoints**: `/v1/messages`
- **Features**: Streaming, system prompts, temperature control
- **Authentication**: x-api-key header

---

## 🚨 Error Handling

| Error Type | Description | Resolution |
|------------|-------------|------------|
| **Authentication** | Invalid or missing API key | Check API key in .env file |
| **Rate Limiting** | Too many requests | Wait and retry later |
| **Model Unavailable** | Model not found | Check model name and provider |
| **Network Issues** | Connection problems | Check internet connection |
| **Invalid Response** | Malformed API response | Report as bug |

---

## 🤝 Contributing

### Development Setup
```bash
# Clone and setup
git clone https://github.com/Neorex80/advanced-terminal-chatbot.git
cd advanced-terminal-chatbot

# Install development dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install

# Run tests
python run_tests.py
```

### Code Quality Standards
- **Formatting**: Black code formatter
- **Linting**: Flake8 with strict rules
- **Type Checking**: MyPy with strict mode
- **Testing**: Minimum 90% coverage
- **Documentation**: Comprehensive docstrings

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support & Troubleshooting

### Common Issues
<details>
<summary><b>API Key Issues</b></summary>

- Ensure API keys are set in `.env` file
- Check API key format and validity
- Verify API key has sufficient credits

</details>

<details>
<summary><b>Import Errors</b></summary>

- Install all dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)
- Verify virtual environment activation

</details>

<details>
<summary><b>Code Analysis Issues</b></summary>

- Ensure Pygments is installed: `pip install pygments`
- Check code syntax for supported languages
- Verify file extensions for language detection

</details>

### Environment Details
- **OS**: Windows, macOS, Linux
- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Dependencies**: See requirements.txt
- **Storage**: Local JSON files for contexts and branches

---

## ⭐ Star the Project

If you find this project useful, please consider giving it a star on GitHub!

---

## 🔗 Links

- [GitHub Repository](https://github.com/Neorex80/advanced-terminal-chatbot)
- [Issue Tracker](https://github.com/Neorex80/advanced-terminal-chatbot/issues)
- [Documentation](https://github.com/Neorex80/advanced-terminal-chatbot/wiki)
- [Contributing Guide](CONTRIBUTING.md)

---

<div align="center">

**Made with ❤️ by the Advanced Terminal Chatbot Team**

</div>
