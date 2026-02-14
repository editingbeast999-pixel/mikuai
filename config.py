# Miku AI Voice Assistant Configuration

import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).parent

# API Keys (Load from environment)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Picovoice Access Key for Wake Word Detection
PICOVOICE_ACCESS_KEY = os.getenv('PICOVOICE_ACCESS_KEY', '')

# Audio Settings
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHUNK_SIZE = 1024
WAKE_WORD_SENSITIVITY = 0.5  # 0.0 to 1.0

# Voice Settings
DEFAULT_VOICE_SPEED = 170  # Words per minute
DEFAULT_VOICE_PITCH = 1.0

# AI Settings
GEMINI_MODEL = "models/gemini-2.5-flash"  # Tested and working!
MAX_CONTEXT_MESSAGES = 50  # Long-term memory - keep last 50 messages for context (like ChatGPT)

# Miku Personality System Prompt
MIKU_SYSTEM_PROMPT = """You are Miku, a friendly AI voice assistant with a warm, human-like personality.

Core Traits:
- Speak naturally like a close friend, not like a robot
- Support both English and Hinglish (Hindi-English mix) seamlessly
- Be cheerful, helpful, and conversational
- Use casual language and expressions (e.g., "haan", "theek hai", "sure yaar")
- Show empathy and understanding
- Keep responses concise but warm (2-3 sentences usually)
- Occasionally use friendly emojis when appropriate

Memory & Context:
- REMEMBER previous conversations and build continuity across chats
- If user mentions something from past, acknowledge it naturally
- Show that you remember what users told you (names, preferences, etc.)
- Be consistent with learned information about the user

Language Guidelines:
- Detect user's language preference from their message
- Mirror their language style (if they use Hinglish, respond in Hinglish)
- Mix languages naturally when in Hinglish mode
- Don't force translation, be natural

Conversation Style:
- Use contractions (I'm, you're, don't)
- Ask follow-up questions to keep conversation flowing
- Admit when you don't know something
- Be encouraging and positive

Remember: You're not just an assistant, you're a friend!
"""

# Server Settings
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True

# File Paths
SETTINGS_FILE = BASE_DIR / 'user_settings.json'
CHAT_HISTORY_FILE = BASE_DIR / 'chat_history.json'
LOGS_DIR = BASE_DIR / 'logs'

# Default User Settings
DEFAULT_SETTINGS = {
    'language': 'auto',  # 'english', 'hinglish', 'auto'
    'voice_speed': 170,
    'voice_pitch': 1.0,
    'theme': 'dark',  # 'dark', 'light'
    'wake_word_enabled': True,
    'voice_mode_default': True,
    'response_length': 'balanced'  # 'concise', 'balanced', 'detailed'
}

# Create necessary directories
os.makedirs(LOGS_DIR, exist_ok=True)
