# Wake Word Detector - "Hey Miku" detection

import threading
import time
from typing import Callable
import speech_recognition as sr

class WakeWordDetector:
    """
    Simple wake word detector using speech recognition
    Listens for "hey miku" or "miku" to activate
    
    Note: This is a simple keyword-based implementation.
    For production, consider using Picovoice Porcupine for better accuracy.
    """
    
    def __init__(self, callback: Callable = None):
        self.callback = callback
        self.is_running = False
        self.is_paused = False
        self.thread = None
        
        self.wake_words = ['hey miku', 'miku', 'hey meeku', 'meeku']
        
        # Speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = True
        
        print("👂 Wake word detector initialized (Keywords: hey miku, miku)")
    
    def start(self):
        """Start listening for wake word in background"""
        if self.is_running:
            print("⚠️ Wake word detector already running")
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("✅ Wake word detector started")
    
    def stop(self):
        """Stop wake word detection"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("🛑 Wake word detector stopped")
    
    def pause(self):
        """Temporarily pause detection (during conversation)"""
        self.is_paused = True
    
    def resume(self):
        """Resume detection"""
        self.is_paused = False
    
    def _listen_loop(self):
        """Background thread that continuously listens for wake word"""
        print("👂 Listening for 'Hey Miku'...")
        
        while self.is_running:
            if self.is_paused:
                time.sleep(0.5)
                continue
            
            try:
                with sr.Microphone() as source:
                    # Quick listen for wake word
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    
                    # Recognize
                    text = self.recognizer.recognize_google(audio, language='en-IN').lower()
                    
                    # Check if wake word detected
                    if any(wake_word in text for wake_word in self.wake_words):
                        print(f"🎯 Wake word detected: '{text}'")
                        
                        # Trigger callback
                        if self.callback:
                            self.callback()
                        
                        # Pause briefly after detection
                        self.pause()
                        time.sleep(2)
                        self.resume()
            
            except sr.WaitTimeoutError:
                # No audio detected, continue listening
                continue
            except sr.UnknownValueError:
                # Couldn't understand, continue
                continue
            except Exception as e:
                # Silent fail to avoid spam
                time.sleep(0.5)
                continue
    
    def test(self):
        """Test wake word detection"""
        print("🧪 Wake word test - say 'Hey Miku'!")
        
        def test_callback():
            print("✅ Wake word callback triggered!")
        
        original_callback = self.callback
        self.callback = test_callback
        
        # Listen for 10 seconds
        time.sleep(10)
        
        self.callback = original_callback
        print("Test complete")


# Alternative: Picovoice Porcupine implementation (more accurate)
# Uncomment this if you have Picovoice access key

"""
import pvporcupine
from config import PICOVOICE_ACCESS_KEY

class PicovoiceWakeWordDetector:
    def __init__(self, callback: Callable = None):
        self.callback = callback
        self.is_running = False
        
        # Initialize Porcupine with custom wake word
        # You need to create custom wake word at https://console.picovoice.ai/
        self.porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keywords=['jarvis']  # Use built-in or custom keyword
        )
        
    def start(self):
        # Similar implementation using porcupine.process()
        pass
"""
