# Miku AI Voice Assistant - Main Flask Application

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
from datetime import datetime

from miku_agent import MikuAgent
from audio_handler import AudioHandler
from wake_word_detector import WakeWordDetector
from settings_manager import SettingsManager
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

# Initialize Flask app
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
app.config['SECRET_KEY'] = 'miku_secret_key_2024'
CORS(app)

# Initialize SocketIO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize components
miku = None
audio = None
wake_detector = None
settings = None
is_processing = False

def initialize_components():
    """Initialize all Miku components"""
    global miku, audio, wake_detector, settings
    
    try:
        print("🎀 Initializing Miku AI Assistant...")
        
        # Settings
        settings = SettingsManager()
        
        # AI Agent
        miku = MikuAgent()
        
        # Audio Handler
        audio = AudioHandler()
        
        # Wake Word Detector
        if settings.get('wake_word_enabled', True):
            wake_detector = WakeWordDetector(callback=on_wake_word_detected)
            wake_detector.start()
        
        print("✅ All components initialized!")
        return True
    
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def on_wake_word_detected():
    """Callback when wake word is detected"""
    print("🎯 Wake word detected! Starting voice conversation...")
    socketio.emit('wake_word_detected', {'message': 'Hey! Kya madad chahiye?'})
    
    # Start voice conversation
    threading.Thread(target=voice_conversation_flow, daemon=True).start()

def voice_conversation_flow():
    """Handle voice conversation after wake word"""
    global is_processing
    
    if is_processing:
        return
    
    is_processing = True
    wake_detector.pause()
    
    try:
        # Listen for user input
        socketio.emit('status_update', {'status': 'listening', 'message': 'Sun rahi hoon...'})
        
        user_input = audio.listen(timeout=8)
        
        if user_input:
            socketio.emit('user_message', {'text': user_input})
            
            # Get AI response
            socketio.emit('status_update', {'status': 'thinking', 'message': 'Soch rahi hoon...'})
            response = miku.send_message(user_input)
            
            # Speak response
            socketio.emit('miku_message', {'text': response})
            socketio.emit('status_update', {'status': 'speaking', 'message': 'Bol rahi hoon...'})
            
            audio.speak(response, blocking=True)
        
        socketio.emit('status_update', {'status': 'idle', 'message': 'Ready'})
    
    except Exception as e:
        print(f"Voice conversation error: {e}")
    
    finally:
        time.sleep(1)
        wake_detector.resume()
        is_processing = False

# Flask Routes
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'components': {
            'miku': miku is not None,
            'audio': audio is not None,
            'wake_detector': wake_detector is not None and wake_detector.is_running
        }
    })

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get current settings"""
    return jsonify(settings.get_all())

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update settings"""
    data = request.json
    success = settings.update_multiple(data)
    
    # Update audio settings if changed
    if 'voice_speed' in data or 'voice_pitch' in data:
        audio.update_voice_settings()
    
    # Toggle wake word detector
    if 'wake_word_enabled' in data:
        if data['wake_word_enabled'] and not wake_detector.is_running:
            wake_detector.start()
        elif not data['wake_word_enabled'] and wake_detector.is_running:
            wake_detector.stop()
    
    return jsonify({'success': success})

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history"""
    return jsonify(miku.get_history())

@app.route('/api/chat-history', methods=['GET'])
def get_chat_history_for_sidebar():
    """Get chat history formatted for sidebar"""
    try:
        history = miku.get_history() if miku else []
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'history': [], 'error': str(e)})

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation"""
    miku.reset_conversation()
    return jsonify({'success': True, 'message': 'Conversation reset!'})

# SocketIO Events
@socketio.on('connect')
def handle_connect():
    """Client connected"""
    print(f"✅ Client connected")
    emit('connected', {'message': 'Connected to Miku AI!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    print(f"👋 Client disconnected")

@socketio.on('send_message')
def handle_text_message(data):
    """Handle text message from user"""
    global is_processing
    
    user_message = data.get('message', '').strip()
    if not user_message:
        return
    
    if is_processing:
        emit('error', {'message': 'Ek minute, abhi busy hoon!'})
        return
    
    is_processing = True
    
    try:
        # Pause wake word detection
        if wake_detector:
            wake_detector.pause()
        
        # Get AI response
        emit('status_update', {'status': 'thinking', 'message': 'Soch rahi hoon...'})
        response = miku.send_message(user_message)
        
        # Send response
        emit('miku_message', {'text': response})
        emit('status_update', {'status': 'idle', 'message': 'Ready'})
    
    except Exception as e:
        print(f"Error: {e}")
        emit('error', {'message': 'Oops! Kuch galat ho gaya.'})
    
    finally:
        time.sleep(0.5)
        if wake_detector:
            wake_detector.resume()
        is_processing = False

@socketio.on('start_voice_input')
def handle_voice_input():
    """Handle voice input request"""
    threading.Thread(target=voice_conversation_flow, daemon=True).start()

# Main entry point
if __name__ == '__main__':
    # Initialize components
    if initialize_components():
        print(f"\n🎀 Miku AI Assistant starting...")
        print(f"🌐 Server: http://{FLASK_HOST}:{FLASK_PORT}")
        print(f"👂 Wake word: 'Hey Miku'\n")
        
        # Run server
        socketio.run(app, host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG, allow_unsafe_werkzeug=True)
    else:
        print("❌ Failed to initialize. Check your .env file!")
