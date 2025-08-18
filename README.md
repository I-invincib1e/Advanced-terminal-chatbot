<div align="center">
  
# 🤖 Advanced Terminal Chatbot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/Neorex80/advanced-terminal-chatbot)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](https://github.com/Neorex80/advanced-terminal-chatbot)

> A powerful, modular terminal-based chatbot with direct support for OpenAI and Anthropic APIs

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🧩 Modules](#-modules) • [📖 Usage](#-usage) • [🤝 Contributing](#-contributing)

</div>

## 🚀 Quick Start

Get up and running with the Advanced Terminal Chatbot in just a few minutes.

### Prerequisites
- **Python**: 3.8 or higher
- **Dependencies**: requests, python-dotenv, pygments libraries
- **API Key**: Valid key from OpenAI or Anthropic
- **Internet**: Stable connection required

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

Experience the full power of AI in your terminal with these advanced features:

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Provider Support** | Seamlessly switch between OpenAI and Anthropic models |
| 🌈 **Syntax Highlighting** | Beautiful code display with Pygments for better readability |
| 🗂️ **Conversation Branching** | Create multiple conversation threads for different topics |
| 🌿 **Context Management** | Switch between different contexts to organize your chats |
| 💾 **Memory System** | Store and recall important information across conversations |
| 🧪 **Code Analysis** | Analyze code structure and get suggestions for improvements |

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

## 📖 Usage

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
/context info                                        # Show current context
```

### Branch Management
```bash
/branch create Feature Development feature,new        # Create new branch
/branch fork Experiment                               # Fork current branch
/branch switch branch_abc123                          # Switch to branch
/branch tree                                         # View branch structure
/branch info                                         # Show current branch
```

### Memory System
```bash
/memory add "Python is great for data analysis" 0.8 python,data fact  # Add memory
/memory search python                                                 # Search memories
```

## 🧪 Testing

We use pytest for testing with coverage reports to ensure code quality.

```bash
# Run all tests with coverage
python run_tests.py

# Run specific test module
python -m unittest tests.test_chat -v
```

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## 🌟 Show Your Support

If you find this project useful, please consider giving it a star! ⭐

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://github.com/Neorex80">Neorex80</a></sub>
</p>
