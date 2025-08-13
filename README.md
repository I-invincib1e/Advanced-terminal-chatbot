# Advanced Terminal ChatBot

A sophisticated terminal-based chatbot with multi-provider support using OpenAI-compatible API from fast.typegpt.net.

## ✨ Features

- 🤖 **Interactive Terminal Interface** - Beautiful, user-friendly terminal UI
- 🏢 **Multi-Provider Support** - Choose between OpenAI, Anthropic, or API discovery
- 🔑 **Secure API Key Input** - Safe API key handling
- 🎯 **Smart Model Selection** - Predefined models for each provider
- 💬 **Conversation Memory** - Maintains chat history throughout session
- 🧹 **History Management** - Clear conversation history anytime
- ⚡ **Advanced Error Handling** - Comprehensive error detection and recovery
- 🎨 **Enhanced UI** - Clean, organized terminal interface with emojis
- 🚪 **Multiple Exit Options** - Flexible ways to end conversations

## 🚀 Installation

1. **Prerequisites**: Python 3.6+ installed
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

1. **Start the ChatBot**:
   ```bash
   python chatbot.py
   ```

2. **Follow the Setup Process**:
   - 🔑 Enter your API key
   - 🏢 Choose your provider:
     - **OpenAI** (3 premium models)
     - **Anthropic** (3 Claude models)
     - **API Discovery** (fetch available models)
   - 🤖 Select your preferred model
   - 💬 Start chatting!

## 🎯 Available Models

### OpenAI Provider
- `openai/chatgpt-4o-latest`
- `openai/gpt-4.1`
- `openai/o1-mini`

### Anthropic Provider
- `anthropic/claude-sonnet-4`
- `anthropic/claude-3.7-sonnet`
- `anthropic/claude-3.7-sonnet:thinking`

### API Discovery
- Fetches up to 5 available models from the API

## 💬 Chat Commands

| Command | Description |
|---------|-------------|
| `Type message` | Send message to AI |
| `clear` | Clear conversation history |
| `quit`, `exit`, `bye` | End conversation |
| `Ctrl+C` | Force quit anytime |

## 🔧 Error Handling

The chatbot includes comprehensive error handling for:
- ❌ **Authentication Errors** - Invalid API keys
- ⏱️ **Timeout Issues** - Network timeouts
- 🚫 **Rate Limiting** - API rate limit exceeded
- 🔍 **Model Availability** - Unavailable models
- 🌐 **Connection Problems** - Network connectivity issues
- 📝 **Invalid Responses** - Malformed API responses

## 🌐 API Provider

- **Base URL**: https://fast.typegpt.net/v1
- **Format**: OpenAI-compatible API
- **Authentication**: Bearer token
- **Timeout**: 30 seconds per request

## 📋 Requirements

- **Python**: 3.6 or higher
- **Dependencies**: requests library
- **API Key**: Valid key from fast.typegpt.net
- **Internet**: Stable connection required

## 🎨 Interface Preview

```
<img width="685" height="758" alt="image" src="https://github.com/user-attachments/assets/af66c44d-aff7-4b0f-8d1a-f05ab28c8a8a" />

```

## 🛠️ Troubleshooting

- **API Key Issues**: Ensure your key is valid and has sufficient credits
- **Model Errors**: Try selecting a different model or provider
- **Connection Problems**: Check your internet connection
- **Rate Limits**: Wait a moment before sending another message
