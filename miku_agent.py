# Miku AI Agent - Friendly Voice Assistant Brain

import os
import json
import random
import time
import google.generativeai as genai
from datetime import datetime
from config import (
    GEMINI_API_KEY, 
    GEMINI_MODEL, 
    MIKU_SYSTEM_PROMPT, 
    CHAT_HISTORY_FILE,
    MAX_CONTEXT_MESSAGES
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MikuAgent:
    """Miku AI Assistant - Friendly and Human-like with Multi-Key Support"""
    
    def __init__(self):
        # Load API Keys for Rotation
        self.api_keys = []
        
        # Check environment for multiple keys
        key1 = os.getenv('GEMINI_API_KEY_1')
        key2 = os.getenv('GEMINI_API_KEY_2')
        default_key = os.getenv('GEMINI_API_KEY')
        
        if key1 and key1.strip(): self.api_keys.append(key1.strip())
        if key2 and key2.strip(): self.api_keys.append(key2.strip())
        if default_key and default_key.strip():
            if default_key.strip() not in self.api_keys:
                self.api_keys.append(default_key.strip())
        
        if not self.api_keys:
            raise ValueError("Koee bhi Valid API Key nahi mili! Please .env check karein.")
            
        print(f"🔑 Loaded {len(self.api_keys)} API Keys for rotation.")
        
        # Start with a random key or first one
        self.current_key_index = 0
        self.configure_api()
        
        # Initialize model with Miku's personality
        # Note: Model initialization relies on configured API key
        self.init_model()
        
        # Load conversation history
        self.load_history()
        
        print("✅ Miku AI brain initialized with Key Rotation!")
    
    def configure_api(self):
        """Configure GenAI with current key"""
        current_key = self.api_keys[self.current_key_index]
        genai.configure(api_key=current_key)
        # print(f"🔧 Configured API with Key #{self.current_key_index + 1}")

    def rotate_key(self):
        """Switch to next API key"""
        if len(self.api_keys) <= 1:
            print("⚠️ Only one key available, skipping rotation.")
            return False
            
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.configure_api()
        print(f"🔄 Switched to API Key #{self.current_key_index + 1}")
        return True

    def init_model(self):
        """Initialize generative model"""
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=MIKU_SYSTEM_PROMPT
        )
        self.chat = self.model.start_chat(history=[])

    def load_history(self):
        """Load previous chat history"""
        if os.path.exists(CHAT_HISTORY_FILE):
            try:
                with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    
                    if history and len(history) > 0:
                        recent = history[-MAX_CONTEXT_MESSAGES:]
                        formatted_history = []
                        
                        for msg in recent:
                            role = "user" if msg["role"] == "user" else "model"
                            formatted_history.append({
                                "role": role,
                                "parts": [msg["content"]]
                            })
                        
                        # Restart chat with history
                        self.chat = self.model.start_chat(history=formatted_history)
                        print(f"📜 Loaded {len(recent)} previous messages")
            except Exception as e:
                print(f"⚠️ History load error: {e}")
    
    def save_history(self):
        """Save conversation history"""
        try:
            history = []
            for msg in self.chat.history:
                history.append({
                    "role": "user" if msg.role == "user" else "miku",
                    "content": msg.parts[0].text,
                    "timestamp": datetime.now().isoformat()
                })
            
            with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ History save error: {e}")
    
    def send_message(self, user_message):
        """Send message to Miku and get response using Key Rotation"""
        max_retries = len(self.api_keys) + 1 # Try current, then all others if needed
        
        for attempt in range(max_retries):
            try:
                if attempt == 0:
                    print(f"📨 User message: {user_message[:50]}...")
                else:
                    print(f"🔄 Retry attempt {attempt}...")

                # Generate response
                response = self.chat.send_message(user_message)
                miku_response = response.text
                
                print(f"✅ Miku response generated (Success)")
                
                # Save updated history
                self.save_history()
                
                return miku_response
            
            except Exception as e:
                print(f"⚠️ API Error (Key #{self.current_key_index + 1}): {e}")
                
                # If error, try rotating key
                if attempt < max_retries - 1:
                    print("🔄 Switching API Key due to error...")
                    if self.rotate_key():
                        # Key changed, re-init model just in case, though config is global usually
                        self.init_model() 
                        # Need to reload history into new chat session for context!
                        self.load_history()
                        time.sleep(1) # Backoff
                        continue
                    else:
                        # No other keys
                        break
                
                import traceback
                traceback.print_exc()
                
        return "Sorry yaar, mujhe thoda technical issue ho raha hai. Phir se try karo? 😅"
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.chat = self.model.start_chat(history=[])
        if os.path.exists(CHAT_HISTORY_FILE):
            os.remove(CHAT_HISTORY_FILE)
        print("🔄 Conversation reset ho gaya!")
    
    def get_history(self):
        """Get chat history"""
        if os.path.exists(CHAT_HISTORY_FILE):
            try:
                with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
