// Helper Functions for Settings and Voice Controls

// Toggle Settings Panel
function toggleSettings() {
    const settingsPanel = document.getElementById('settings-panel');
    const overlay = document.getElementById('overlay');

    if (settingsPanel && overlay) {
        settingsPanel.classList.toggle('active');
        overlay.classList.toggle('active');
    }
}

// Toggle Voice Mute
let isMuted = false;
function toggleVoiceMute() {
    isMuted = !isMuted;
    const muteBtn = document.getElementById('voice-mute-btn');

    if (muteBtn) {
        const muteIcon = muteBtn.querySelector('.material-icons');

        if (isMuted) {
            muteIcon.textContent = 'volume_off';
            muteBtn.style.color = '#EF4444'; // Red when muted
        } else {
            muteIcon.textContent = 'volume_up';
            muteBtn.style.color = ''; // Default color
        }
    }
}

// Make functions globally accessible
window.toggleSettings = toggleSettings;
window.toggleVoiceMute = toggleVoiceMute;
window.toggleSidebar = toggleSidebar;
