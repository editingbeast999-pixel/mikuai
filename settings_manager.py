# Settings Manager for Miku AI Assistant

import json
import os
from pathlib import Path
from config import SETTINGS_FILE, DEFAULT_SETTINGS

class SettingsManager:
    """Manage user preferences and settings"""
    
    def __init__(self):
        self.settings_file = SETTINGS_FILE
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create default"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**DEFAULT_SETTINGS, **loaded}
            except Exception as e:
                print(f"Error loading settings: {e}")
                return DEFAULT_SETTINGS.copy()
        else:
            return DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value and save"""
        self.settings[key] = value
        return self.save_settings()
    
    def update_multiple(self, updates):
        """Update multiple settings at once"""
        self.settings.update(updates)
        return self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = DEFAULT_SETTINGS.copy()
        return self.save_settings()
    
    def get_all(self):
        """Get all settings"""
        return self.settings.copy()
