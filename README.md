<div align="center">
  
# 🤖 Advanced Terminal Chatbot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/Neorex80/advanced-terminal-chatbot)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](https://github.com/Neorex80/advanced-terminal-chatbot)

> A beautiful, streamlined terminal-based chatbot with direct support for OpenAI and Anthropic APIs

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🧩 Modules](#-modules) • [📖 Usage](#-usage) • [🤝 Contributing](#-contributing)

</div>

## 🚀 Quick Start

Get up and running with the Advanced Terminal Chatbot in just a few minutes.

### Prerequisites
- **Python**: 3.8 or higher
- **Dependencies**: requests, python-dotenv, pygments, rich libraries
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

Experience the power of AI in your terminal with a clean, intuitive interface:

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Provider Support** | Seamlessly switch between OpenAI and Anthropic models |
| 🎨 **Beautiful UI** | Modern terminal interface with rich panels and colors |
| 🌈 **Code Analysis** | Syntax highlighting and code analysis with Pygments |
| ⚡ **Streaming Mode** | Real-time response streaming for better interaction |
| 📝 **Conversation History** | View past conversations in beautifully formatted panels |
| 🎯 **Simple Commands** | Streamlined command set focused on essential features |

## 🧩 Core Modules

<details>
<summary><b>Click to expand module overview</b></summary>

| Module | Functionality |
|--------|---------------|
| `chatbot.py` | Main application orchestrator with enhanced UI |
| `chat.py` | Streamlined chat session management and API communication |
| `provider.py` | AI provider selection and model management |
| `code_analyzer.py` | Code analysis and syntax highlighting |
| `utils.py` | Configuration and utility functions |
| `commands/handler.py` | Clean command processing system |

</details>

## 📖 Usage

### Essential Chat Commands
```bash
/help          # Show help information with beautiful formatting
/clear         # Clear conversation history
/history       # Show conversation history in styled panels
/stream        # Toggle streaming mode
/quit          # Exit the chat
/exit          # Exit the chat
```

### Code Analysis
```bash
/analyze def hello(): print("Hello World")                    # Full code analysis
/highlight function greet(name) { return `Hello ${name}!`; }  # Syntax highlighting only
```

### Example Session
```
🚀 Starting chat with OpenAI (gpt-4)
💡 Type /help for available commands
💡 Type /stream to toggle streaming mode

👤 You: What can you help me with?

╭─ 🤖 Assistant ──────────────────────────────────────────────╮
│ I can help you with a wide variety of tasks including:     │
│                                                             │
│ • Programming and code review                               │
│ • Writing and editing                                       │
│ • Problem solving and analysis                              │
│ • Learning new concepts                                     │
│ • And much more!                                            │
╰─────────────────────────────────────────────────────────────╯
```

## 🎨 UI Highlights

The chatbot features a modern, clean interface inspired by leading CLI tools:

- **Rich Panels**: All messages displayed in beautifully styled panels
- **Color Coding**: User messages in blue, assistant in magenta, errors in red
- **Status Indicators**: Animated "Thinking..." spinner during processing
- **Markdown Support**: Full markdown rendering in responses
- **Consistent Styling**: Professional appearance throughout

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
