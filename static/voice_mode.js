// ChatGPT-Style Voice Mode Controller

let voiceModeActive = false;
let micMuted = false;

// Open voice mode
function openVoiceMode() {
    const overlay = document.getElementById('voice-mode-overlay');
    if (overlay) {
        overlay.classList.add('active');
        voiceModeActive = true;

        // Ensure status is "Hey my name is miku"
        updateVoiceStatus('idle', 'Hey my name is miku');
    }
}

// Close voice mode
function closeVoiceMode() {
    const overlay = document.getElementById('voice-mode-overlay');
    if (overlay) {
        overlay.classList.remove('active');
        voiceModeActive = false;

        // Show main UI
        document.querySelector('.main-container').style.display = 'flex';
        document.querySelector('.sidebar').style.display = 'flex';

        // Reset transcript
        document.getElementById('transcript-user').textContent = '';
        document.getElementById('transcript-miku').textContent = '';

        // Reset status
        updateVoiceStatus('idle', 'Hey my name is miku');
    }
}

// Toggle mic mute
function toggleMic() {
    micMuted = !micMuted;
    const micBtn = document.getElementById('voice-mic-btn');

    if (micMuted) {
        micBtn.classList.add('muted');
        micBtn.querySelector('.material-icons').textContent = 'mic_off';
    } else {
        micBtn.classList.remove('muted');
        micBtn.querySelector('.material-icons').textContent = 'mic';
    }
}

// Update voice mode status
function updateVoiceStatus(status, message) {
    const statusEl = document.getElementById('voice-status-indicator');

    // User requested specific welcome message
    let displayText = message;
    if (status === 'idle' || message === 'idle' || message === 'IDLE' || message === 'Ready' || message === 'Ready to chat!') {
        displayText = 'Hey my name is miku';
    }

    if (statusEl) {
        statusEl.textContent = displayText;
        statusEl.className = 'voice-status-indicator ' + status;
    }
}
