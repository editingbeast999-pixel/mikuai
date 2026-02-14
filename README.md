# 🎀 Miku AI Voice Assistant

**Your friendly AI companion with voice and text support!**

Miku is an advanced AI voice assistant powered by Google Gemini 2.0 Flash that speaks both English and Hinglish naturally, just like a friend!

---

## ✨ Features

- 🎤 **Wake Word Detection** - Just say "Hey Miku" to activate
- 💬 **Dual Input Modes** - Type or speak your messages
- 🌏 **Bilingual Support** - Seamlessly speaks English and Hinglish
- 🤖 **Human-like Personality** - Friendly, conversational responses
- ⚙️ **Customizable Settings** - Adjust voice speed, theme, language preference
- 🎨 **Beautiful Modern UI** - Animated orb interface with smooth transitions
- 💾 **Conversation Memory** - Remembers your chat history
- 📱 **Responsive Design** - Works on desktop and mobile

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Microphone (for voice input)
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone/Download the project**
   ```powershell
   cd C:\Users\Production\.gemini\antigravity\scratch\miku_ai_assistant
   ```

2. **Create virtual environment** (recommended)
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up API keys**
   - Copy `.env.example` to `.env`:
     ```powershell
     copy .env.example .env
     ```
   - Edit `.env` and add your Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

5. **Run Miku!**
   ```powershell
   python main.py
   ```

6. **Open in browser**
   - Navigate to: `http://localhost:5000`
   - Enjoy chatting with Miku! 🎀

---

## 🎯 Usage

### Text Chat
1. Type your message in the input box
2. Press Enter or click the send button
3. Miku will respond in text

### Voice Chat
1. Click the microphone button (purple circle)
2. Speak your message
3. Miku will respond with voice

### Wake Word Activation
1. Make sure wake word detection is enabled in settings
2. Say "Hey Miku" anytime
3. Miku will start listening automatically
4. Speak your question/message

### Settings Panel
- Click the ⚙️ settings icon in the top right
- Customize:
  - **Language**: Auto-detect, English, or Hinglish
  - **Voice Speed**: Adjust speaking speed (120-220 wpm)
  - **Theme**: Dark or Light mode
  - **Wake Word**: Enable/disable wake word detection

---

## 🛠️ Troubleshooting

### "GEMINI_API_KEY not found" error
- Make sure you created a `.env` file from `.env.example`
- Add your actual API key in the `.env` file
- Restart the application

### Microphone not working
```python
# Test your microphone
python -c "from audio_handler import AudioHandler; a = AudioHandler(); a.test_microphone()"
```

### Wake word not detecting
- Check if your microphone is working
- Speak clearly: "Hey Miku"
- Try adjusting microphone volume
- Make sure wake word is enabled in settings

### Port 5000 already in use
- Edit `config.py` and change `FLASK_PORT` to another port (e.g., 5001)
- Or stop the application using port 5000

---

## 📁 Project Structure

```
miku_ai_assistant/
├── main.py                 # Flask application entry point
├── config.py              # Configuration and settings
├── miku_agent.py          # AI brain (Gemini integration)
├── audio_handler.py       # Voice input/output
├── wake_word_detector.py  # "Hey Miku" detection
├── settings_manager.py    # User preferences management
├── requirements.txt       # Python dependencies
├── .env                   # API keys (create from .env.example)
├── static/
│   ├── styles.css        # Beautiful UI styles
│   └── script.js         # Frontend logic & animations
└── templates/
    └── index.html        # Main web interface
```

---

## 🎨 Customization

### Change Miku's Personality
Edit `config.py` → `MIKU_SYSTEM_PROMPT` to customize how Miku responds.

### Modify Colors/Theme
Edit `static/styles.css` → `:root` variables to change colors.

### Add Custom Tools
Extend `miku_agent.py` to add custom capabilities (weather, news, etc.)

---

## 🧪 Technology Stack

- **Backend**: Python, Flask, Flask-SocketIO
- **AI**: Google Gemini 2.0 Flash
- **Voice**: SpeechRecognition, pyttsx3
- **Frontend**: HTML5, CSS3, JavaScript, Canvas API
- **Real-time**: Socket.IO

---

## 📝 Requirements

See `requirements.txt` for full list. Main dependencies:
- google-generativeai
- flask + flask-socketio
- SpeechRecognition
- pyttsx3
- python-dotenv

---

## ⚠️ Important Notes

- **Internet Required**: Needs internet for Gemini AI and speech recognition
- **Microphone Permission**: Browser will ask for microphone access
- **API Costs**: Gemini has free tier, monitor usage at [Google AI Studio](https://makersuite.google.com)
- **Wake Word**: Current implementation uses simple keyword detection. For production, consider Picovoice Porcupine.

---

## 🤝 Support

Having issues? 
1. Check the troubleshooting section above
2. Verify your `.env` file has the correct API key
3. Make sure all dependencies are installed
4. Check Python version (3.8+)

---

## 📜 License

This project is created for educational and personal use. 

**Enjoy chatting with Miku! 🎀**

---

*Made with ❤️ using Google Gemini 2.0 Flash*
