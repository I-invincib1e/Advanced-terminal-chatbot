import requests
import json
import sys
import time

class TerminalChatBot:
    def __init__(self):
        self.api_base = "https://fast.typegpt.net/v1"
        self.api_key = None
        self.selected_model = None
        self.selected_provider = None
        self.conversation_history = []
        
        # Predefined models for each provider
        self.provider_models = {
            "OpenAI": [
                "openai/chatgpt-4o-latest",
                "openai/gpt-4.1",
                "openai/o1-mini"
            ],
            "Anthropic": [
                "anthropic/claude-sonnet-4",
                "anthropic/claude-3.7-sonnet",
                "anthropic/claude-3.7-sonnet:thinking"
            ]
        }
    
    def display_welcome(self):
        print("\n" + "═" * 70)
        print("🤖  ADVANCED TERMINAL CHATBOT  🤖".center(70))
        print("═" * 70)
        print("🌐 Powered by fast.typegpt.net API".center(70))
        print("🚀 Multi-Provider Support: OpenAI & Anthropic".center(70))
        print("💬 Intelligent Conversation with Memory".center(70))
        print("═" * 70)
        print()
    
    def get_api_key(self):
        print("🔑 API KEY SETUP")
        print("─" * 50)
        while True:
            api_key = input("📝 Enter your API key: ").strip()
            if api_key:
                self.api_key = api_key
                print("✅ API key saved successfully!")
                print()
                break
            else:
                print("❌ API key cannot be empty. Please try again.")
                print()
    
    def select_provider(self):
        print("🏢 PROVIDER SELECTION")
        print("─" * 50)
        providers = list(self.provider_models.keys())
        
        for i, provider in enumerate(providers, 1):
            model_count = len(self.provider_models[provider])
            print(f"  {i}. {provider} ({model_count} models available)")
        
        print("  3. Fetch from API (original method)")
        print("─" * 50)
        
        while True:
            try:
                choice = input("🎯 Select provider (1-3): ").strip()
                choice_num = int(choice)
                
                if choice_num == 3:
                    return "API"
                elif 1 <= choice_num <= len(providers):
                    selected_provider = providers[choice_num - 1]
                    self.selected_provider = selected_provider
                    print(f"✅ Selected provider: {selected_provider}")
                    print()
                    return selected_provider
                else:
                    print(f"❌ Please enter a number between 1 and {len(providers) + 1}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
    
    def fetch_models(self):
        print("🔍 Fetching available models...")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(f"{self.api_base}/models", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('data', [])
                
                if models:
                    # Limit to first 5 models as requested
                    limited_models = models[:5]
                    print(f"✅ Found {len(limited_models)} models:\n")
                    return limited_models
                else:
                    print("❌ No models found in the response.")
                    return []
            else:
                print(f"❌ Failed to fetch models. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching models: {e}")
            return []
    
    def select_provider_model(self, provider):
        print(f"🤖 {provider.upper()} MODELS")
        print("─" * 50)
        
        models = self.provider_models[provider]
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
        
        print("─" * 50)
        
        while True:
            try:
                choice = input(f"🎯 Select model (1-{len(models)}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(models):
                    self.selected_model = models[choice_num - 1]
                    print(f"✅ Selected model: {self.selected_model}")
                    print()
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(models)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
    
    def select_model(self, models):
        print("🤖 API MODELS")
        print("─" * 50)
        
        for i, model in enumerate(models, 1):
            model_id = model.get('id', 'Unknown')
            print(f"  {i}. {model_id}")
        
        print("─" * 50)
        
        while True:
            try:
                choice = input(f"🎯 Select model (1-{len(models)}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(models):
                    selected_model = models[choice_num - 1]
                    self.selected_model = selected_model.get('id')
                    print(f"✅ Selected model: {self.selected_model}")
                    print()
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(models)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
    
    def send_message(self, message):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        payload = {
            "model": self.selected_model,
            "messages": self.conversation_history,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            # Show thinking animation
            print("🤔 Thinking", end="", flush=True)
            for _ in range(3):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()
            
            response = requests.post(f"{self.api_base}/chat/completions", 
                                   headers=headers, 
                                   json=payload, 
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Better error handling for response structure
                if 'choices' in data and len(data['choices']) > 0:
                    assistant_message = data['choices'][0]['message']['content']
                    
                    # Add assistant response to conversation history
                    self.conversation_history.append({"role": "assistant", "content": assistant_message})
                    
                    return assistant_message
                else:
                    # Remove user message from history if response failed
                    self.conversation_history.pop()
                    return "❌ Invalid response format from API"
                    
            elif response.status_code == 401:
                self.conversation_history.pop()
                return "❌ Authentication failed. Please check your API key."
            elif response.status_code == 429:
                self.conversation_history.pop()
                return "❌ Rate limit exceeded. Please wait a moment and try again."
            elif response.status_code == 404:
                self.conversation_history.pop()
                return f"❌ Model '{self.selected_model}' not found or unavailable."
            else:
                self.conversation_history.pop()
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                    return f"❌ API Error ({response.status_code}): {error_msg}"
                except:
                    return f"❌ HTTP Error {response.status_code}: {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            self.conversation_history.pop()
            return "❌ Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            self.conversation_history.pop()
            return "❌ Connection failed. Please check your internet connection."
        except requests.exceptions.RequestException as e:
            self.conversation_history.pop()
            return f"❌ Request failed: {str(e)}"
        except Exception as e:
            self.conversation_history.pop()
            return f"❌ Unexpected error: {str(e)}"
    
    def start_chat(self):
        print("💬 CHAT SESSION")
        print("═" * 70)
        provider_info = f"Provider: {self.selected_provider}" if self.selected_provider else "Provider: API"
        model_info = f"Model: {self.selected_model}"
        print(f"🏢 {provider_info}")
        print(f"🤖 {model_info}")
        print("═" * 70)
        print("📝 Commands:")
        print("  • Type your message and press Enter to chat")
        print("  • 'clear' - Clear conversation history")
        print("  • 'quit', 'exit', 'bye' - End conversation")
        print("  • Ctrl+C - Force quit")
        print("═" * 70)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n" + "─" * 50)
                    print("👋 Thank you for using Terminal ChatBot!")
                    print("   Have a great day! 🌟")
                    print("─" * 50)
                    break
                
                if user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("\n🧹 Conversation history cleared!")
                    print("   Starting fresh conversation...")
                    continue
                
                if not user_input:
                    print("❌ Please enter a message.")
                    continue
                
                response = self.send_message(user_input)
                
                # Format the bot response nicely
                print(f"\n🤖 Bot:")
                print("─" * 50)
                print(response)
                print("─" * 50)
                
            except KeyboardInterrupt:
                print("\n\n" + "─" * 50)
                print("⚡ Chat interrupted by user")
                print("👋 Goodbye!")
                print("─" * 50)
                break
            except Exception as e:
                print(f"\n❌ Unexpected error in chat loop: {e}")
                print("   Please try again or restart the application.")
    
    def run(self):
        try:
            self.display_welcome()
            self.get_api_key()
            
            # Provider selection
            selected_provider = self.select_provider()
            
            if selected_provider == "API":
                # Original method - fetch from API
                models = self.fetch_models()
                if not models:
                    print("❌ Cannot proceed without available models.")
                    print("   Please check your API key and internet connection.")
                    sys.exit(1)
                self.select_model(models)
            else:
                # Use predefined models for selected provider
                self.select_provider_model(selected_provider)
            
            self.start_chat()
            
        except KeyboardInterrupt:
            print("\n\n" + "─" * 50)
            print("⚡ Setup interrupted by user")
            print("👋 Goodbye!")
            print("─" * 50)
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Fatal error during setup: {e}")
            print("   Please restart the application.")
            sys.exit(1)

def main():
    chatbot = TerminalChatBot()
    chatbot.run()

if __name__ == "__main__":
    main()
