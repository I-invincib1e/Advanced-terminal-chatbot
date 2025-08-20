<div align="center">
  
# 🤖 Enhanced Advanced Terminal Chatbot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.0-orange.svg)](https://github.com/Neorex80/advanced-terminal-chatbot)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](https://github.com/Neorex80/advanced-terminal-chatbot)

> A powerful, feature-rich terminal-based chatbot with multi-line input, persistent history, and advanced AI provider support

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🧩 Modules](#-modules) • [📖 Usage](#-usage) • [🤝 Contributing](#-contributing)

</div>

## 🚀 Quick Start

Get up and running with the Enhanced Advanced Terminal Chatbot in just a few minutes.

### Prerequisites
- **Python**: 3.8 or higher
- **Dependencies**: All listed in requirements.txt
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

## ✨ Enhanced Features

Experience the power of AI in your terminal with cutting-edge features:

| Feature | Description | Commands |
|---------|-------------|----------|
| 🧠 **Multi-Provider Support** | Seamlessly switch between OpenAI and Anthropic models | `/sp`, `/sm` |
| 🎨 **Beautiful UI** | Modern terminal interface with rich panels and colors | Built-in |
| 🌈 **Code Analysis** | Syntax highlighting and code analysis with save options | `/analyze --save` |
| ⚡ **Streaming Mode** | Real-time response streaming for better interaction | `/stream`, `/s` |
| 📝 **Persistent History** | Save, resume, and export conversations | `/save`, `/resume`, `/export` |
| 🎯 **Smart Commands** | Comprehensive command set with short aliases | `/h`, `/q`, `/cp` |
| 💻 **Multi-line Input** | Advanced input with Ctrl+Enter submission | Built-in |
| 📋 **Clipboard Integration** | Copy AI responses directly to clipboard | `/copy`, `/cp` |
| 🔄 **Session Management** | Full conversation lifecycle management | `/ls`, `/del` |
| ⌨️ **Auto-completion** | Tab completion for commands and history | Built-in |

## 🧩 Core Modules

<details>
<summary><b>Click to expand enhanced module overview</b></summary>

| Module | Functionality |
|--------|---------------|
| `chatbot.py` | Main application orchestrator with enhanced UI |
| `chat.py` | Advanced chat session with multi-line input and persistence |
| `provider.py` | AI provider selection and dynamic model switching |
| `code_analyzer.py` | Enhanced code analysis with file export |
| `history_manager.py` | SQLite-based conversation persistence |
| `input_handler.py` | Multi-line input with prompt_toolkit |
| `clipboard_manager.py` | Clipboard operations for response copying |
| `commands/handler.py` | Comprehensive command system with aliases |

</details>

## 📖 Enhanced Usage

### Essential Chat Commands (with aliases)
```bash
/help or /h          # Show comprehensive help with all features
/clear or /c         # Clear conversation history
/history or /hist    # Show conversation history in styled panels
/stream or /s        # Toggle streaming mode
/quit or /q          # Exit the chat
/exit or /e          # Exit the chat
```

### Advanced Code Analysis
```bash
/analyze def hello(): print("Hello World")              # Full code analysis
/analyze --save report.txt print("Hello")               # Analyze and save to file
/highlight function greet(name) { return `Hello ${name}!`; }  # Syntax highlighting only
/a for x in range(10): print(x)                        # Short alias
```

### Session Management
```bash
/save or /sv                    # Save current conversation
/resume <session_id> or /r      # Resume a previous conversation
/list-sessions or /ls           # List all saved conversations
/export json or /exp markdown   # Export conversation (json/markdown/txt)
/delete-session <id> or /del    # Delete a conversation
```

### Provider & Model Management
```bash
/set-provider openai or /sp     # Switch to OpenAI
/set-model gpt-4 or /sm         # Change to GPT-4
/providers or /p                # Show available providers
/models or /m                   # Show available models
```

### Clipboard Operations
```bash
/copy or /cp                    # Copy last AI response to clipboard
```

### Multi-line Input
- **Enter**: New line in multi-line mode
- **Ctrl+Enter**: Submit your message
- **Ctrl+D**: Add a new line
- **Tab**: Command completion
- **Up/Down**: Navigate command history

### Example Enhanced Session
```
🚀 Starting chat with OpenAI (gpt-4)
💡 Type /help or /h for available commands
💡 Use Ctrl+Enter to submit multi-line input
💡 Use Tab for command completion

👤 You: /h
╭─ Available Commands ─────────────────────────────────────────╮
│                                                              │
│ 📚 Chat Commands:                                            │
│ • /help or /h - Show this help message                      │
│ • /clear or /c - Clear conversation history                 │
│ • /history or /hist - Show conversation history             │
│                                                              │
│ 💾 Session Management:                                       │
│ • /save or /sv - Save current conversation                  │
│ • /resume <id> or /r <id> - Resume a previous conversation  │
│ • /list-sessions or /ls - List saved conversations          │
│                                                              │
│ 🔧 Provider & Model:                                         │
│ • /set-provider <name> or /sp <name> - Change AI provider   │
│ • /set-model <name> or /sm <name> - Change AI model         │
│                                                              │
│ 📋 Clipboard:                                                │
│ • /copy or /cp - Copy last AI response to clipboard         │
╰──────────────────────────────────────────────────────────────╯

👤 You: Write a Python function to calculate fibonacci
      def fibonacci(n):
          if n <= 1:
              return n
          return fibonacci(n-1) + fibonacci(n-2)

╭─ 🤖 Assistant ──────────────────────────────────────────────╮
│ Here's an enhanced version of the Fibonacci function with   │
│ multiple implementations:                                    │
│                                                              │
│ ```python                                                   │
│ # Recursive (your version)                                  │
│ def fibonacci_recursive(n):                                 │
│     if n <= 1:                                              │
│         return n                                             │
│     return fibonacci_recursive(n-1) + fibonacci_recursive(n-2) │
│                                                              │
│ # Iterative (more efficient)                               │
│ def fibonacci_iterative(n):                                 │
│     if n <= 1:                                              │
│         return n                                             │
│     a, b = 0, 1                                             │
│     for _ in range(2, n + 1):                               │
│         a, b = b, a + b                                     │
│     return b                                                 │
│ ```                                                          │
╰──────────────────────────────────────────────────────────────╯

👤 You: /cp
✅ Copied to clipboard: Here's an enhanced version of the Fibonacci function with multiple implementations...

👤 You: /save
✅ Conversation saved with ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890

👤 You: /ls
╭─ 💾 Saved Conversations ─────────────────────────────────────╮
│ ID       │ Title                      │ Provider │ Model │ Date    │
├──────────┼────────────────────────────┼──────────┼───────┼─────────┤
│ a1b2c3d4 │ Write a Python function... │ openai   │ gpt-4 │ 2025... │
╰──────────┴────────────────────────────┴──────────┴───────┴─────────╯
```

## 🎨 UI Highlights

The enhanced chatbot features a modern, professional interface:

- **Rich Panels**: All messages displayed in beautifully styled panels
- **Color Coding**: User messages in blue, assistant in magenta, errors in red
- **Status Indicators**: Animated "Thinking..." spinner during processing
- **Markdown Support**: Full markdown rendering in responses
- **Multi-line Input**: Advanced text editor with syntax highlighting
- **Tab Completion**: Smart command completion and history
- **Persistent Sessions**: Seamless conversation management

## 🧪 Testing

We use pytest for testing with coverage reports to ensure code quality.

```bash
# Run all tests with coverage
python run_tests.py

# Run specific test module
python -m unittest tests.test_chat -v
```

## 📁 File Structure

```
advanced-terminal-chatbot/
├── src/advanced_terminal_chatbot/
│   ├── __init__.py
│   ├── chatbot.py              # Main orchestrator
│   ├── chat.py                 # Enhanced chat session
│   ├── provider.py             # AI provider management
│   ├── code_analyzer.py        # Code analysis tools
│   ├── utils.py               # Configuration utilities
│   ├── history_manager.py      # Persistent conversation storage
│   ├── input_handler.py        # Multi-line input handler
│   ├── clipboard_manager.py    # Clipboard operations
│   ├── commands/
│   │   └── handler.py         # Command system with aliases
│   └── providers/
│       ├── base.py            # Base provider interface
│       ├── openai.py          # OpenAI implementation
│       └── anthropic.py       # Anthropic implementation
├── tests/                      # Test suite
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies
├── .env.sample                # Environment template
└── README.md                   # This file
```

## 🆕 What's New in v1.2

### 🎨 Enhanced UI & Experience
- **Beautiful ASCII Art Banners**: Stunning startup screens with `pyfiglet`
- **Loading Animations**: Smooth spinners and progress indicators with `halo`
- **Enhanced Prompts**: Interactive selection menus with `questionary`
- **Cross-Platform Colors**: Consistent colors across all platforms with `colorama`
- **Progress Visualization**: Real-time progress bars for long operations

### 🔧 Technical Improvements
- **Enhanced Logging**: Colorful, rotating logs with `loguru`
- **Modular UI Architecture**: Reusable components in `ui_enhancements.py`
- **Graceful Error Handling**: Fallback mechanisms for library failures
- **Performance Optimizations**: Lazy loading and efficient rendering

### 📋 New Features
- **Categorized Help System**: Organized command help with visual separation
- **Status Tables**: Professional status displays with icons and colors
- **Information Panels**: Success, error, and info panels with consistent styling
- **Demo Mode**: Interactive feature demonstration with `demo_enhanced_features.py`

### 🚀 Ready for Future
- **Textual Framework**: Prepared for full TUI development
- **Async Support**: Ready for `aiohttp` and `websockets` integration
- **Theme System**: Foundation for customizable themes

## 🆕 Previous Updates (v2.0)

- **Multi-line Input**: Advanced text editor with Ctrl+Enter submission
- **Persistent History**: SQLite-based conversation storage and retrieval
- **Session Management**: Save, resume, export, and delete conversations
- **Dynamic Provider Switching**: Change AI providers and models on-the-fly
- **Command Aliases**: Short versions of all commands (e.g., `/h` for `/help`)
- **Clipboard Integration**: Copy AI responses directly to system clipboard
- **Enhanced Code Analysis**: Save analysis results to files
- **Auto-completion**: Tab completion for commands and history navigation
- **Export Options**: Export conversations in JSON, Markdown, or plain text
- **Improved UI**: Better visual feedback and status indicators

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
