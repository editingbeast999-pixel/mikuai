// Miku AI Voice Assistant - Frontend JavaScript (Final Complete Version)

const socket = io();

// State
let isVoiceActive = false;
let currentStatus = 'idle';
let settings = {};
let chatHistory = [];
let currentChatId = generateChatId();
let voiceOrb = null;
let recognition = null; // Browser STT
let synth = window.speechSynthesis; // Browser TTS

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements - Fetch here to ensure they exist
    window.chatContainer = document.getElementById('chat-container');
    window.textInput = document.getElementById('text-input');
    window.voiceBtn = document.getElementById('voice-btn');
    window.statusText = document.getElementById('status-text');
    window.settingsPanel = document.getElementById('settings-panel');
    window.overlay = document.getElementById('overlay');
    window.historyList = document.getElementById('history-list');

    // Fallback for mikuOrb (Orbit)
    window.mikuOrb = document.getElementById('orbContainer');

    // Initialize Voice Orb
    voiceOrb = new VoiceOrb();

    // Event Listeners
    if (window.voiceBtn) {
        window.voiceBtn.addEventListener('click', startVoiceInput);
    }

    // Globals for onclick handlers
    window.sendMessage = sendMessage;
    window.toggleSettings = toggleSettings;
    window.resetConversation = resetConversation;
    window.startVoiceInput = startVoiceInput;
    window.handleKeyPress = handleKeyPress;
    window.updateSettings = updateSettings;
    window.updateSpeedLabel = updateSpeedLabel;
    window.loadChat = loadChat;
    window.newChat = newChat;

    // Load Data
    loadSettings();
    setupSocketListeners();
    loadChatHistory(); // Restore History Loading

    // Default status
    updateStatus('idle', 'Hey my name is miku');

    // Remove welcome message after first interaction
    setTimeout(() => {
        const welcome = document.querySelector('.welcome-message');
        if (welcome && chatContainer.children.length === 1) {
            // Keep it until first message
        }
    }, 1000);

    // Setup Browser Speech Recognition
    setupBrowserSpeech();
});

// Setup Browser Speech Recognition (Client-Side)
function setupBrowserSpeech() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false; // Stop after speaking
        recognition.lang = 'en-IN'; // Default to Indian English/Hinglish
        recognition.interimResults = false;

        recognition.onstart = function () {
            updateStatus('listening', 'Listening (Phone Mic)...');
            if (voiceOrb) voiceOrb.startListening();
        };

        recognition.onend = function () {
            // Wait slightly before stopping listening visual
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            console.log("🗣️ You said: ", transcript);
            sendMessage(transcript); // Send as text
        };

        recognition.onerror = function (event) {
            console.error("Speech Error:", event.error);
            if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
                alert("⚠️ Mic Access Denied!\nPhone pe Mic use karne ke liye HTTPS zaroori hai.\nTry localhost or enable 'Insecure origins treated as secure' in chrome://flags.");
                exitVoiceMode();
            } else {
                updateStatus('idle', 'Mic Error - Try Again');
                exitVoiceMode();
            }
        };
    } else {
        console.log("Browser Speech Recognition not supported.");
    }
}

// Speak using Browser TTS
function speakResponse(text) {
    if (synth && !document.hidden && settings.voice_mode_default !== false) {
        // Cancel previous
        synth.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = (settings.voice_speed || 170) / 170; // Map 170 to ~1.0
        utterance.pitch = 1.1; // Slightly fem/higher

        // Try to find a good female voice
        const voices = synth.getVoices();
        const preferred = voices.find(v => v.name.includes('Google') && v.name.includes('Female')) ||
            voices.find(v => v.name.includes('Zira')) ||
            voices.find(v => v.lang.includes('en'));

        if (preferred) utterance.voice = preferred;

        utterance.onend = function () {
            updateStatus('idle', 'Hey my name is miku');
        };

        synth.speak(utterance);
    }
}

// Voice-reactive orb animation
class VoiceOrb {
    constructor() {
        this.orbContainer = document.getElementById('orbContainer');
        this.innerLine = document.querySelector('.orb-inner-line');
        this.orb = document.querySelector('.orb');
        this.isListening = false;
        this.animationFrame = null;
        this.intensity = 0;
        this.targetIntensity = 0;
    }

    startListening() {
        this.isListening = true;
        this.animate();
        if (this.innerLine) this.innerLine.classList.add('listening');
    }

    stopListening() {
        this.isListening = false;
        this.targetIntensity = 0;
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
        }

        if (this.innerLine) {
            this.innerLine.style.transform = '';
            this.innerLine.style.boxShadow = '';
            this.innerLine.classList.remove('listening');
        }
        if (this.orb) {
            this.orb.style.boxShadow = '';
        }
    }

    animate() {
        if (!this.isListening) return;

        this.targetIntensity = 0.2 + Math.random() * 0.6;
        this.intensity += (this.targetIntensity - this.intensity) * 0.15;

        const lineScale = 1 + (this.intensity * 0.4);
        const glowOpacity = 0.5 + (this.intensity * 0.5);

        if (this.innerLine) {
            this.innerLine.style.transform = `scale(${lineScale})`;
            this.innerLine.style.boxShadow = `0 0 ${20 + this.intensity * 30}px rgba(0, 212, 255, ${glowOpacity})`;
        }

        if (this.orb) {
            this.orb.style.boxShadow = `0 0 ${25 + this.intensity * 10}px rgba(0, 191, 255, 0.3)`;
        }

        this.animationFrame = requestAnimationFrame(() => this.animate());
    }
}

// Socket Event Listeners
function setupSocketListeners() {
    socket.on('connect', () => {
        console.log('✅ Connected to Miku AI');
        updateStatus('idle', 'Hey my name is miku');
    });

    socket.on('user_message', (data) => {
        addMessage('user', data.text);
    });

    socket.on('miku_message', (data) => {
        addMessage('miku', data.text);

        // If Voice Mode is Active, Speak it!
        if (isVoiceActive) {
            speakResponse(data.text);
            updateStatus('speaking', 'Speaking...');
        }
    });

    socket.on('status_update', (data) => {
        // Ignroe 'listening' from server if we are using Client Mic
        if (recognition && data.status === 'listening' && isVoiceActive) return;

        updateStatus(data.status, data.message);
        if (data.status === 'idle' && isVoiceActive && !synth.speaking) {
            // Don't exit immediately if speaking
        }
    });

    socket.on('error', (data) => {
        alert(data.message);
        updateStatus('idle', 'Hey my name is miku');
        if (isVoiceActive) exitVoiceMode();
    });
}

// Send Text Message
function sendMessage(text) {
    const message = text || (window.textInput ? window.textInput.value.trim() : '');
    if (!message) return;

    if (window.textInput) window.textInput.value = '';

    // Optimistic Update: Show message immediately
    addMessage('user', message);

    socket.emit('send_message', { message });
    updateStatus('thinking', 'Soch rahi hoon...');
}

function handleKeyPress(event) {
    if (event.key === 'Enter') sendMessage();
}

// Voice Input Switcher
function startVoiceInput() {
    if (isVoiceActive) return;
    isVoiceActive = true;
    enterVoiceMode();

    if (recognition) {
        // Use Browser Mic (Phone Mode)
        try {
            recognition.start();
        } catch (e) {
            console.error("Recog Start Error", e);
            recognition.stop();
            setTimeout(() => recognition.start(), 200);
        }
    } else {
        // Fallback to Server Mic (PC Mode)
        socket.emit('start_voice_input');
    }
}

// Voice Mode UI
function enterVoiceMode() {
    if (window.chatContainer) window.chatContainer.style.display = 'none';

    if (window.mikuOrb) {
        window.mikuOrb.classList.add('voice-mode');
    }

    if (window.voiceBtn) window.voiceBtn.classList.add('active');
    updateStatus('listening', 'Listening...');
}

function exitVoiceMode() {
    if (window.chatContainer) window.chatContainer.style.display = 'flex';
    const inputArea = document.querySelector('.input-area');
    if (inputArea) inputArea.style.display = 'flex';

    if (window.mikuOrb) {
        window.mikuOrb.classList.remove('voice-mode');
    }

    isVoiceActive = false;
    if (window.voiceBtn) window.voiceBtn.classList.remove('active');
    updateStatus('idle', 'Hey my name is miku');

    if (recognition) recognition.stop();
    if (synth) synth.cancel();
}

// Add Message to Chat
function addMessage(role, text) {
    if (!window.chatContainer) return;

    const welcome = window.chatContainer.querySelector('.welcome-message');
    if (welcome) welcome.remove();

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    if (role === 'system') {
        messageDiv.innerHTML = `
            <div class="message-bubble" style="background: var(--bg-tertiary); text-align: center; max-width: 100%;">
                ${text}
            </div>
        `;
    } else {
        const icon = role === 'user' ? '👤' : '🎀';
        messageDiv.innerHTML = `
            <div class="message-icon">${icon}</div>
            <div class="message-bubble">${text}</div>
        `;
    }

    window.chatContainer.appendChild(messageDiv);
    window.chatContainer.scrollTop = window.chatContainer.scrollHeight;
}

// Update Status
function updateStatus(status, message) {
    currentStatus = status;
    const s = status ? status.toLowerCase() : 'idle';
    let displayText = message;

    if (s === 'idle' || message === 'idle' || message === 'IDLE' || message === 'Ready' || message === 'Ready to chat!' || message === 'READY') {
        displayText = 'Hey my name is miku';
    } else if (!message) {
        displayText = status.toUpperCase();
    }

    if (window.statusText) {
        window.statusText.textContent = displayText;
        window.statusText.className = `status-text ${s}`;
    }

    if (voiceOrb) {
        if (s === 'listening') voiceOrb.startListening();
        else voiceOrb.stopListening();
    }

    if (s === 'idle' && !isVoiceActive) {
        if (window.voiceBtn) window.voiceBtn.classList.remove('active');
    }
}

// Settings 
function toggleSettings() {
    if (window.settingsPanel) window.settingsPanel.classList.toggle('active');
    if (window.overlay) window.overlay.classList.toggle('active');
}

function loadSettings() {
    fetch('/api/settings').then(r => r.json()).then(data => {
        settings = data;
        const langEl = document.getElementById('language-setting');
        if (langEl) langEl.value = data.language;
        if (data.theme === 'light') document.body.classList.add('light-theme');
    });
}

function updateSettings() { console.log("Settings update triggered"); }
function updateSpeedLabel(value) {
    const el = document.getElementById('speed-value');
    if (el) el.textContent = value;
}

// Chat History Functions (RESTORED)
function generateChatId() { return 'chat_' + Date.now(); }

function newChat() {
    if (isVoiceActive) exitVoiceMode();
    // Frontend-only new chat (Clears view, backend keeps global history potentially unless reset)
    // Ideally user wants clear slate
    currentChatId = generateChatId();
    if (window.chatContainer) window.chatContainer.innerHTML = '';
    // Reload history list
    loadChatHistory();
}

function resetConversation() {
    if (!confirm('Clear all chat history?')) return;
    fetch('/api/reset', { method: 'POST' }).then(() => {
        if (window.chatContainer) window.chatContainer.innerHTML = '<div class="welcome-message"><h2>Namaste! Main Miku hoon 👋</h2><p>Voice ya text - jaise bhi chahiye, baat karo!</p></div>';
        chatHistory = [];
        renderChatHistory();
        currentChatId = generateChatId();
    });
}

function loadChatHistory() {
    fetch('/api/chat-history')
        .then(r => r.json())
        .then(data => {
            if (data.success && data.history && data.history.length > 0) {
                // Group messages into sessions based on time gaps (e.g., 30 mins)
                const sessions = [];
                let currentSession = null;
                const TIME_THRESHOLD = 30 * 60 * 1000; // 30 minutes

                data.history.forEach((msg, idx) => {
                    const msgTime = new Date(msg.timestamp).getTime();

                    // Start new session if:
                    // 1. No current session
                    // 2. Time gap > threshold
                    if (!currentSession || (idx > 0 && (msgTime - new Date(data.history[idx - 1].timestamp).getTime() > TIME_THRESHOLD))) {

                        // Save previous session if exists
                        if (currentSession) sessions.push(currentSession);

                        // Create new session
                        currentSession = {
                            id: 'session_' + idx,
                            title: 'New Chat', // Will update below
                            timestamp: msgTime,
                            messages: []
                        };
                    }

                    currentSession.messages.push({
                        role: msg.role === 'model' ? 'miku' : msg.role,
                        text: msg.content
                    });
                });

                // Push last session
                if (currentSession) sessions.push(currentSession);

                // Generate Titles for each session based on first user message
                sessions.forEach(session => {
                    const firstUserMsg = session.messages.find(m => m.role === 'user');
                    if (firstUserMsg) {
                        session.title = firstUserMsg.text.substring(0, 25) + (firstUserMsg.text.length > 25 ? '...' : '');
                    } else if (session.messages.length > 0) {
                        session.title = session.messages[0].text.substring(0, 25) + '...';
                    } else {
                        session.title = 'Empty Chat';
                    }
                });

                // Reverse to show newest on top
                chatHistory = sessions.reverse();
                renderChatHistory();
            } else {
                chatHistory = []; // Clear if no history
                renderChatHistory();
            }
        })
        .catch(err => {
            console.log('Error loading history:', err);
            renderChatHistory();
        });
}

function renderChatHistory() {
    if (!window.historyList) return;
    window.historyList.innerHTML = '';

    if (chatHistory.length === 0) {
        window.historyList.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-secondary); font-size: 0.85rem;">No chats yet</div>';
        return;
    }

    chatHistory.forEach(chat => {
        const item = document.createElement('div');
        item.className = 'history-item';
        // Check if active (assuming main session is always active on reload for now)
        if (chat.id === 'session_main') item.classList.add('active');

        // Show timestamp or title
        const date = new Date(chat.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        item.innerHTML = `<div style="font-weight:500;">${chat.title}</div><div style="font-size:0.7em; opacity:0.7;">${date}</div>`;

        item.onclick = () => loadChat(chat.id);
        window.historyList.appendChild(item);
    });
}

function loadChat(chatId) {
    const chat = chatHistory.find(c => c.id === chatId);
    if (!chat) return;

    if (window.chatContainer) window.chatContainer.innerHTML = '';

    chat.messages.forEach(msg => {
        addMessage(msg.role, msg.text);
    });
}
