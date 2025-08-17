"""
Chat session management for the terminal chatbot.
"""

import requests
import time
import json
from typing import Dict, List, Any, Optional, Generator
from .utils import ConfigManager
from .code_analyzer import CodeAnalyzer
from .context_manager import ContextManager
from .conversation_brancher import ConversationBrancher


class ChatSession:
    """Manages a chat session with conversation history and API communication."""
    
    def __init__(self, config: ConfigManager, model: str, provider: str):
        """Initialize the chat session."""
        self.config = config
        self.model = model
        self.provider = provider
        self.conversation_history: List[Dict[str, str]] = []
        self.max_tokens = int(config.get("MAX_TOKENS", "1000"))
        self.temperature = float(config.get("TEMPERATURE", "0.7"))
        
        # Initialize new features
        self.code_analyzer = CodeAnalyzer()
        self.context_manager = ContextManager()
        self.conversation_brancher = ConversationBrancher(self.context_manager)

        if provider == "OpenAI":
            self.api_base = config.get_openai_base_url()
            self.api_key = config.get_openai_api_key()
        elif provider == "Anthropic":
            self.api_base = config.get_anthropic_base_url()
            self.api_key = config.get_anthropic_api_key()
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})
        
        # Also add to current branch if exists
        if self.conversation_brancher.get_current_branch():
            self.conversation_brancher.add_message_to_branch(role, content)

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()

    def get_history(self) -> List[Dict[str, str]]:
        """Get a copy of the conversation history."""
        return self.conversation_history.copy()

    def _format_openai_payload(self, message: str, stream: bool = False) -> Dict[str, Any]:
        """Format the payload for OpenAI API."""
        messages = self.conversation_history + [{"role": "user", "content": message}]
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": stream
        }
        
        return payload

    def _format_anthropic_payload(self, message: str, stream: bool = False) -> Dict[str, Any]:
        """Format the payload for Anthropic API."""
        # Convert conversation history to Anthropic format
        messages = []
        for msg in self.conversation_history:
            if msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                messages.append({"role": "assistant", "content": msg["content"]})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": stream
        }
        
        return payload

    def _handle_openai_response(self, response: requests.Response) -> str:
        """Handle OpenAI API response."""
        if response.status_code == 200:
            try:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    content = data['choices'][0]['message']['content']
                    return content
                else:
                    return "❌ Invalid response format from OpenAI API"
            except json.JSONDecodeError:
                return "❌ Invalid JSON response from OpenAI API"
        else:
            return self._handle_error_response(response, "OpenAI")

    def _handle_anthropic_response(self, response: requests.Response) -> str:
        """Handle Anthropic API response."""
        if response.status_code == 200:
            try:
                data = response.json()
                if 'content' in data and len(data['content']) > 0:
                    content = data['content'][0]['text']
                    return content
                else:
                    return "❌ Invalid response format from Anthropic API"
            except json.JSONDecodeError:
                return "❌ Invalid JSON response from Anthropic API"
        else:
            return self._handle_error_response(response, "Anthropic")

    def _handle_error_response(self, response: requests.Response, provider: str) -> str:
        """Handle error responses from API."""
        if response.status_code == 401:
            return f"❌ Authentication failed for {provider}. Please check your API key."
        elif response.status_code == 429:
            return f"❌ Rate limit exceeded for {provider}. Please try again later."
        elif response.status_code == 404:
            return f"❌ Model not found or unavailable for {provider}."
        elif response.status_code >= 500:
            return f"❌ {provider} server error. Please try again later."
        else:
            try:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                return f"❌ {provider} API error: {error_msg}"
            except:
                return f"❌ {provider} API error (status {response.status_code})"

    def send_message(self, message: str) -> str:
        """Send a message and get a response (non-streaming)."""
        if not self.api_key:
            return f"❌ {self.provider} API key not configured"
        
        self.add_message("user", message)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if self.provider == "OpenAI":
            payload = self._format_openai_payload(message, stream=False)
            endpoint = f"{self.api_base}/chat/completions"
        elif self.provider == "Anthropic":
            payload = self._format_anthropic_payload(message, stream=False)
            endpoint = f"{self.api_base}/messages"
            headers["x-api-key"] = self.api_key
            headers["anthropic-version"] = "2023-06-01"
        else:
            return f"❌ Unknown provider: {self.provider}"

        try:
            print("🤔 Thinking...", end="", flush=True)
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            print("\r", end="", flush=True)  # Clear the thinking message
            
            if self.provider == "OpenAI":
                result = self._handle_openai_response(response)
            elif self.provider == "Anthropic":
                result = self._handle_anthropic_response(response)
            
            if not result.startswith("❌"):
                self.add_message("assistant", result)
            else:
                # Remove the user message if there was an error
                self.conversation_history.pop()
            
            return result
            
        except requests.exceptions.Timeout:
            print("\r", end="", flush=True)
            self.conversation_history.pop()
            return f"❌ Request to {self.provider} timed out. Please try again."
        except requests.exceptions.ConnectionError as e:
            print("\r", end="", flush=True)
            self.conversation_history.pop()
            return f"❌ Connection error: {str(e)}"
        except Exception as e:
            print("\r", end="", flush=True)
            self.conversation_history.pop()
            return f"❌ Unexpected error: {str(e)}"

    def stream_response(self, message: str) -> Generator[str, None, None]:
        """Stream a response from the API."""
        if not self.api_key:
            yield f"❌ {self.provider} API key not configured"
            return
        
        self.add_message("user", message)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        if self.provider == "OpenAI":
            payload = self._format_openai_payload(message, stream=True)
            endpoint = f"{self.api_base}/chat/completions"
        elif self.provider == "Anthropic":
            payload = self._format_anthropic_payload(message, stream=True)
            endpoint = f"{self.api_base}/messages"
            headers["x-api-key"] = self.api_key
            headers["anthropic-version"] = "2023-06-01"
        else:
            yield f"❌ Unknown provider: {self.provider}"
            return

        try:
            print("🤔 Thinking...", end="", flush=True)
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30, stream=True)
            print("\r", end="", flush=True)  # Clear the thinking message
            
            if response.status_code != 200:
                error_msg = self._handle_error_response(response, self.provider)
                self.conversation_history.pop()
                yield error_msg
                return
            
            full_response = ""
            
            if self.provider == "OpenAI":
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]  # Remove 'data: ' prefix
                            if data == '[DONE]':
                                break
                            try:
                                json_data = json.loads(data)
                                if 'choices' in json_data and len(json_data['choices']) > 0:
                                    delta = json_data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        content = delta['content']
                                        full_response += content
                                        yield content
                            except json.JSONDecodeError:
                                continue
                                
            elif self.provider == "Anthropic":
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]  # Remove 'data: ' prefix
                            if data == '[DONE]':
                                break
                            try:
                                json_data = json.loads(data)
                                if json_data.get('type') == 'content_block_delta' and 'delta' in json_data:
                                    delta = json_data['delta']
                                    if 'text' in delta:
                                        text = delta['text']
                                        full_response += text
                                        yield text
                            except json.JSONDecodeError:
                                continue
            
            # Add the complete response to conversation history
            if full_response:
                self.add_message("assistant", full_response)
            
        except requests.exceptions.Timeout:
            print("\r", end="", flush=True)
            self.conversation_history.pop()
            yield f"❌ Request to {self.provider} timed out. Please try again."
        except requests.exceptions.ConnectionError as e:
            print("\r", end="", flush=True)
            self.conversation_history.pop()
            yield f"❌ Connection error: {str(e)}"
        except Exception as e:
            print("\r", end="", flush=True)
            self.conversation_history.pop()
            yield f"❌ Unexpected error: {str(e)}"

    def analyze_code(self, code: str, language: str = "auto", show_analysis: bool = True) -> str:
        """Analyze code with syntax highlighting and explanation."""
        try:
            return self.code_analyzer.format_code_block(code, language, show_analysis)
        except Exception as e:
            return f"❌ Code analysis failed: {str(e)}"

    def create_context(self, name: str, description: str = "", tags: List[str] = None) -> str:
        """Create a new conversation context."""
        try:
            context_id = self.context_manager.create_context(name, description, tags)
            return f"✅ Created context: {name} (ID: {context_id})"
        except Exception as e:
            return f"❌ Failed to create context: {str(e)}"

    def switch_context(self, context_id: str) -> str:
        """Switch to a different conversation context."""
        try:
            if self.context_manager.switch_context(context_id):
                context = self.context_manager.get_current_context()
                return f"✅ Switched to context: {context.name}"
            else:
                return f"❌ Context {context_id} not found"
        except Exception as e:
            return f"❌ Failed to switch context: {str(e)}"

    def create_branch(self, name: str, tags: List[str] = None) -> str:
        """Create a new conversation branch."""
        try:
            branch_id = self.conversation_brancher.create_branch(name, tags=tags)
            return f"✅ Created branch: {name} (ID: {branch_id})"
        except Exception as e:
            return f"❌ Failed to create branch: {str(e)}"

    def switch_branch(self, branch_id: str) -> str:
        """Switch to a different conversation branch."""
        try:
            if self.conversation_brancher.switch_branch(branch_id):
                branch = self.conversation_brancher.get_current_branch()
                return f"✅ Switched to branch: {branch.name}"
            else:
                return f"❌ Branch {branch_id} not found"
        except Exception as e:
            return f"❌ Failed to switch branch: {str(e)}"

    def fork_branch(self, name: str, include_history: bool = True) -> str:
        """Fork the current branch."""
        try:
            branch_id = self.conversation_brancher.fork_branch(name, include_history=include_history)
            return f"✅ Forked branch: {name} (ID: {branch_id})"
        except Exception as e:
            return f"❌ Failed to fork branch: {str(e)}"

    def get_context_info(self) -> str:
        """Get information about current context and branch."""
        info = []
        
        # Current context info
        current_context = self.context_manager.get_current_context()
        if current_context:
            info.append(f"📋 **Current Context**: {current_context.name}")
            info.append(f"   Description: {current_context.description}")
            if current_context.tags:
                info.append(f"   Tags: {', '.join(current_context.tags)}")
        else:
            info.append("📋 **Current Context**: None")
        
        # Current branch info
        current_branch = self.conversation_brancher.get_current_branch()
        if current_branch:
            info.append(f"🌿 **Current Branch**: {current_branch.name}")
            info.append(f"   Messages: {len(current_branch.messages)}")
            if current_branch.tags:
                info.append(f"   Tags: {', '.join(current_branch.tags)}")
        else:
            info.append("🌿 **Current Branch**: None")
        
        return "\n".join(info)

    def get_branch_tree(self) -> str:
        """Get a tree representation of all branches."""
        try:
            tree = self.conversation_brancher.get_branch_tree()
            if not tree:
                return "🌿 No branches found"
            
            def format_tree(node, level=0):
                indent = "  " * level
                status = "🟢" if node['is_active'] else "🔴"
                result = f"{indent}{status} {node['name']} ({node['message_count']} messages)"
                
                for child in node['children']:
                    result += "\n" + format_tree(child, level + 1)
                
                return result
            
            result = "🌿 **Branch Tree**:\n"
            for branch_id, branch_data in tree.items():
                result += format_tree(branch_data) + "\n"
            
            return result
        except Exception as e:
            return f"❌ Failed to get branch tree: {str(e)}"

    def search_memories(self, query: str) -> str:
        """Search memories for relevant information."""
        try:
            memories = self.context_manager.search_memories(query)
            if not memories:
                return f"🔍 No memories found for: {query}"
            
            result = f"🔍 **Memories for '{query}'**:\n\n"
            for memory in memories:
                result += f"📝 **{memory.type.title()}** (importance: {memory.importance})\n"
                result += f"   {memory.content}\n"
                if memory.tags:
                    result += f"   Tags: {', '.join(memory.tags)}\n"
                result += "\n"
            
            return result
        except Exception as e:
            return f"❌ Memory search failed: {str(e)}"

    def add_memory(self, content: str, importance: float = 0.5, tags: List[str] = None, memory_type: str = "fact") -> str:
        """Add a new memory item."""
        try:
            memory_id = self.context_manager.add_memory(content, importance, tags, memory_type)
            return f"✅ Added memory: {content[:50]}{'...' if len(content) > 50 else ''} (ID: {memory_id})"
        except Exception as e:
            return f"❌ Failed to add memory: {str(e)}"

    def display_help(self) -> None:
        """Display help information."""
        print("\n📚 Chat Commands:")
        print("  /help     - Show this help message")
        print("  /clear    - Clear conversation history")
        print("  /history  - Show conversation history")
        print("  /stream   - Toggle streaming mode")
        print("  /quit     - Exit the chat")
        print("  /exit     - Exit the chat")
        print("\n🔍 Code Analysis:")
        print("  /analyze <code> - Analyze code with syntax highlighting")
        print("  /highlight <code> - Apply syntax highlighting only")
        print("\n🌿 Context & Branching:")
        print("  /context create <name> [description] [tags] - Create new context")
        print("  /context switch <id> - Switch to context")
        print("  /context info - Show current context info")
        print("  /branch create <name> [tags] - Create new branch")
        print("  /branch switch <id> - Switch to branch")
        print("  /branch fork <name> - Fork current branch")
        print("  /branch tree - Show branch tree")
        print("  /branch info - Show current branch info")
        print("\n🧠 Memory Management:")
        print("  /memory add <content> [importance] [tags] [type] - Add memory")
        print("  /memory search <query> - Search memories")
        print("\n📊 Statistics:")
        print("  /stats - Show system statistics")
        print()

    def start_chat(self) -> None:
        """Start the interactive chat loop."""
        print(f"\n🚀 Starting chat with {self.provider} ({self.model})")
        print("💡 Type /help for available commands")
        print("💡 Type /stream to toggle streaming mode")
        print()
        
        streaming_mode = False
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == '/help':
                    self.display_help()
                    continue
                elif user_input.lower() == '/clear':
                    self.clear_history()
                    print("🧹 Conversation history cleared!")
                    continue
                elif user_input.lower() == '/history':
                    if not self.conversation_history:
                        print("📝 No conversation history yet.")
                    else:
                        print("\n📝 Conversation History:")
                        for i, msg in enumerate(self.conversation_history, 1):
                            role_emoji = "👤" if msg["role"] == "user" else "🤖"
                            print(f"  {i}. {role_emoji} {msg['role'].title()}: {msg['content']}")
                        print()
                    continue
                elif user_input.lower() == '/stream':
                    streaming_mode = not streaming_mode
                    mode = "ON" if streaming_mode else "OFF"
                    print(f"🔄 Streaming mode: {mode}")
                    continue
                
                # Code analysis commands
                elif user_input.startswith('/analyze '):
                    code = user_input[9:].strip()
                    if code:
                        result = self.analyze_code(code)
                        print(f"🔍 Code Analysis:\n{result}")
                    else:
                        print("❌ Please provide code to analyze")
                    continue
                elif user_input.startswith('/highlight '):
                    code = user_input[11:].strip()
                    if code:
                        try:
                            highlighted = self.code_analyzer.highlight_syntax(code)
                            print(f"🎨 Syntax Highlighting:\n```\n{highlighted}\n```")
                        except Exception as e:
                            print(f"❌ Highlighting failed: {str(e)}")
                    else:
                        print("❌ Please provide code to highlight")
                    continue
                
                # Context management commands
                elif user_input.startswith('/context create '):
                    parts = user_input[16:].split(' ', 1)
                    name = parts[0]
                    description = parts[1] if len(parts) > 1 else ""
                    result = self.create_context(name, description)
                    print(result)
                    continue
                elif user_input.startswith('/context switch '):
                    context_id = user_input[16:].strip()
                    result = self.switch_context(context_id)
                    print(result)
                    continue
                elif user_input.lower() == '/context info':
                    result = self.get_context_info()
                    print(result)
                    continue
                
                # Branch management commands
                elif user_input.startswith('/branch create '):
                    parts = user_input[15:].split(' ', 1)
                    name = parts[0]
                    tags = parts[1].split(',') if len(parts) > 1 else None
                    if tags:
                        tags = [tag.strip() for tag in tags]
                    result = self.create_branch(name, tags)
                    print(result)
                    continue
                elif user_input.startswith('/branch switch '):
                    branch_id = user_input[15:].strip()
                    result = self.switch_branch(branch_id)
                    print(result)
                    continue
                elif user_input.startswith('/branch fork '):
                    name = user_input[13:].strip()
                    result = self.fork_branch(name)
                    print(result)
                    continue
                elif user_input.lower() == '/branch tree':
                    result = self.get_branch_tree()
                    print(result)
                    continue
                elif user_input.lower() == '/branch info':
                    result = self.get_context_info()
                    print(result)
                    continue
                
                # Memory management commands
                elif user_input.startswith('/memory add '):
                    parts = user_input[12:].split(' ', 2)
                    content = parts[0]
                    importance = float(parts[1]) if len(parts) > 1 and parts[1].replace('.', '').isdigit() else 0.5
                    tags = parts[2].split(',') if len(parts) > 2 else None
                    if tags:
                        tags = [tag.strip() for tag in tags]
                    result = self.add_memory(content, importance, tags)
                    print(result)
                    continue
                elif user_input.startswith('/memory search '):
                    query = user_input[15:].strip()
                    result = self.search_memories(query)
                    print(result)
                    continue
                
                # Statistics command
                elif user_input.lower() == '/stats':
                    context_stats = self.context_manager.get_stats()
                    branch_stats = self.conversation_brancher.get_stats()
                    
                    print("\n📊 **System Statistics**:")
                    print(f"   Contexts: {context_stats['total_contexts']}")
                    print(f"   Memories: {context_stats['total_memories']}")
                    print(f"   Branches: {branch_stats['total_branches']}")
                    print(f"   Active Branches: {branch_stats['active_branches']}")
                    print(f"   Total Messages: {branch_stats['total_messages']}")
                    print()
                    continue
                
                # Regular chat message
                if streaming_mode:
                    print("🤖 Assistant: ", end="", flush=True)
                    response_parts = []
                    for part in self.stream_response(user_input):
                        if part.startswith("❌"):
                            print(f"\n{part}")
                            break
                        response_parts.append(part)
                        print(part, end="", flush=True)
                    print()  # New line after response
                else:
                    response = self.send_message(user_input)
                    print(f"🤖 Assistant: {response}")
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 End of input. Goodbye!")
                break
