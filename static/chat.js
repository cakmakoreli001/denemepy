let messageCount = 0;

function newChat() {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">🤖</div>
            <h2>Merhaba! Ben Grok 👋</h2>
            <p>Size nasıl yardımcı olabilirim? Herhangi bir şey sorun!</p>
            <div class="suggestions">
                <button class="suggestion" onclick="sendSuggestion('Python hakkında bilgi ver')">
                    💻 Python nedir?
                </button>
                <button class="suggestion" onclick="sendSuggestion('Komik bir şaka anlat')">
                    😄 Şaka anlat
                </button>
                <button class="suggestion" onclick="sendSuggestion('Yapay zeka hakkında bilgi ver')">
                    🤖 AI nedir?
                </button>
                <button class="suggestion" onclick="sendSuggestion('Bugün hava nasıl?')">
                    🌤️ Hava durumu
                </button>
            </div>
        </div>
    `;
    messageCount = 0;
    updateMessageCount();
}

function sendSuggestion(text) {
    document.getElementById('userInput').value = text;
    sendMessage();
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Hide welcome message
    const welcome = document.querySelector('.welcome-message');
    if (welcome) {
        welcome.remove();
    }
    
    // Add user message
    addMessage(message, 'user');
    input.value = '';
    
    // Disable send button
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;
    
    // Show typing indicator
    const typingDiv = addTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        typingDiv.remove();
        
        if (data.success) {
            addMessage(data.message, 'ai');
        } else {
            addMessage(`❌ Hata: ${data.message}`, 'ai');
        }
    } catch (error) {
        typingDiv.remove();
        addMessage(`❌ Bağlantı hatası: ${error.message}`, 'ai');
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

function addMessage(text, type) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = type === 'user' ? '👤' : '🤖';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">${formatMessage(text)}</div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    messageCount++;
    updateMessageCount();
}

function formatMessage(text) {
    // Convert markdown-like formatting
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    text = text.replace(/`(.*?)`/g, '<code>$1</code>');
    text = text.replace(/\n/g, '<br>');
    return text;
}

function addTypingIndicator() {
    const messagesDiv = document.getElementById('messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    return typingDiv;
}

function updateMessageCount() {
    document.getElementById('messageCount').textContent = messageCount;
}

function toggleTheme() {
    // Theme toggle functionality can be added here
    alert('Tema değiştirme özelliği yakında eklenecek!');
}

// Auto-resize textarea
const textarea = document.getElementById('userInput');
textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});
