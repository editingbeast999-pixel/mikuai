# Audio Handler - Voice Input/Output Management

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ SpeechRecognition not available - voice input disabled")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ pyttsx3 not available - voice output disabled")
import threading
import queue
from settings_manager import SettingsManager

class AudioHandler:
    """Handles all voice input and output operations"""
    
    def __init__(self):
        self.settings = SettingsManager()
        self.tts_available = TTS_AVAILABLE
        self.sr_available = SPEECH_RECOGNITION_AVAILABLE
        
        # Initialize Text-to-Speech engine only if available
        if self.tts_available:
            try:
                self.tts_engine = pyttsx3.init()
                self._configure_tts()
            except Exception as e:
                print(f"⚠️ TTS initialization failed: {e}")
                self.tts_available = False
        else:
            print("ℹ️ Text-to-speech not available - voice output disabled")
        
        # Initialize Speech Recognition only if available
        if self.sr_available:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.energy_threshold = 4000
                self.recognizer.dynamic_energy_threshold = True
            except Exception as e:
                print(f"⚠️ Speech recognition initialization failed: {e}")
                self.sr_available = False
        else:
            print("ℹ️ Speech recognition not available - voice input disabled")
        
        # Audio playback queue
        self.speak_queue = queue.Queue()
        self.is_speaking = False
        
        print("🎤 Audio handler initialized!")
    
    def _configure_tts(self):
        """Configure TTS with user settings"""
        speed = self.settings.get('voice_speed', 170)
        pitch = self.settings.get('voice_pitch', 1.0)
        
        self.tts_engine.setProperty('rate', speed)
        
        # Try to set a female voice if available
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
    
    def listen(self, timeout=5):
        """
        Listen for voice input from microphone
        Returns: recognized text or None
        """
        if not self.sr_available:
            print("⚠️ Speech recognition not available")
            return None
            
        try:
            with sr.Microphone() as source:
                print("🎧 Listening...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                print("🔄 Processing...")
                
                # Recognize using Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language='en-IN')
                
                return text
        
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("⚠️ Couldn't understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            return None
        except Exception as e:
            print(f"❌ Audio error: {e}")
            return None
    
    def speak(self, text, blocking=True):
        """
        Convert text to speech
        Args:
            text: Text to speak
            blocking: Wait for speech to complete
        """
        if not text:
            return
        
        if not self.tts_available:
            print(f"💬 Miku (text only): {text}")
            return
        
        try:
            self.is_speaking = True
            print(f"🔊 Miku: {text}")
            
            if blocking:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Non-blocking speech
                thread = threading.Thread(target=self._speak_thread, args=(text,))
                thread.daemon = True
                thread.start()
        
        except Exception as e:
            print(f"❌ TTS error: {e}")
        finally:
            self.is_speaking = False
    
    def _speak_thread(self, text):
        """Thread for non-blocking speech"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Speech thread error: {e}")
    
    def update_voice_settings(self):
        """Update TTS settings from user preferences"""
        self._configure_tts()
    
    def test_microphone(self):
        """Test if microphone is working"""
        try:
            with sr.Microphone() as source:
                print("🎤 Microphone test - say something!")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                print(f"✅ Heard: {text}")
                return True
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            return False
