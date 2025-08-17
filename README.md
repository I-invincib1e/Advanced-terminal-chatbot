<div align="center">
  
# 🤖 Advanced Terminal Chatbot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/Neorex80/advanced-terminal-chatbot)

> A powerful, modular terminal-based chatbot with direct support for OpenAI and Anthropic APIs

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🧩 Modules](#-modules) • [� Contributing](#-contributing)

</div>

## � Quick Start

### Prerequisites
- Python 3.8+
- OpenAI or Anthropic API key

### Installation & Setup
```bash
# Clone the repository
git clone https://github.com/Neorex80/advanced-terminal-chatbot.git
cd advanced-terminal-chatbot

# Install dependencies
pip install -r requirements.txt

# Create and configure environment file
python main.py --create-env
# Edit .env with your API keys

# Run the chatbot
python main.py
```

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| � **Multi-Provider Support** | Works with both OpenAI and Anthropic APIs |
| 🌈 **Syntax Highlighting** | Beautiful code display with Pygments |
| 🗂️ **Conversation Branching** | Create multiple conversation threads |
| � **Context Management** | Switch between different contexts seamlessly |
| � **Memory System** | Store and recall important information |
| 🧪 **Code Analysis** | Analyze code structure and suggest improvements |

## 🧩 Core Modules

<details>
<summary><b>Click to expand module overview</b></summary>

| Module | Functionality |
|--------|---------------|
| `chatbot.py` | Main application orchestrator |
| `chat.py` | Chat session management and API communication |
| `provider.py` | AI provider selection and model management |
| `code_analyzer.py` | Code analysis and syntax highlighting |
| `context_manager.py` | Context switching and memory storage |
| `conversation_brancher.py` | Branch management for conversations |
| `utils.py` | Configuration and utility functions |

</details>

## 📖 Usage Examples

### Basic Chat Commands
```bash
/help          # Show help information
/clear         # Clear conversation history
/history       # Show conversation history
/stream        # Toggle streaming mode
/quit          # Exit the chat
```

### Code Analysis
```bash
/analyze def hello(): print("Hello World")  # Full code analysis
/highlight function greet(name) { return `Hello ${name}!`; }  # Syntax only
```

### Context Management
```bash
/context create Python Development python,development  # Create new context
/context switch ctx_abc123                            # Switch context
```

### Branch Management
```bash
/branch create Feature Development feature,new        # Create new branch
/branch fork Experiment                               # Fork current branch
/branch tree                                         # View branch structure
```

### Memory System
```bash
/memory add "Python is great for data analysis" 0.8 python,data fact  # Add memory
/memory search python                                                 # Search memories
```

## 🧪 Testing

```bash
# Run all tests
python run_tests.py

# Run specific test
python -m unittest tests.test_chat -v
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## � Show Your Support

If you find this project useful, please consider giving it a star! ⭐
