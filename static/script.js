document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    darkModeToggle.addEventListener('change', function() {
        document.body.classList.toggle('dark-mode', this.checked);
    });

    // Chat functionality
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const kvkkConsent = document.getElementById('kvkkConsent');
    const faqButtons = document.querySelectorAll('.faq-btn');

    // Handle KVKK consent
    kvkkConsent.addEventListener('change', function() {
        const isConsented = this.checked;
        userInput.disabled = !isConsented;
        sendButton.disabled = !isConsented;
        faqButtons.forEach(btn => btn.disabled = !isConsented);

        if (isConsented) {
            addMessage("KVKK onayınız için teşekkür ederiz. Size nasıl yardımcı olabilirim?", false);
        }
    });

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        // Handle multiple paragraphs
        const paragraphs = message.split('\n');
        paragraphs.forEach(paragraph => {
            if (paragraph.trim()) {
                const p = document.createElement('p');
                p.textContent = paragraph;
                messageDiv.appendChild(p);
            }
        });
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage(message) {
        addMessage(message, true);
        userInput.value = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            addMessage(data.response);
        } catch (error) {
            addMessage('Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.');
        }
    }

    async function sendFAQ(question) {
        try {
            const response = await fetch('/api/faq', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });

            const data = await response.json();
            addMessage(data.response);
        } catch (error) {
            addMessage('Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.');
        }
    }

    // Event listeners
    sendButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            sendMessage(message);
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const message = userInput.value.trim();
            if (message) {
                sendMessage(message);
            }
        }
    });

    faqButtons.forEach(button => {
        button.addEventListener('click', () => {
            const question = button.dataset.question;
            sendFAQ(question);
        });
    });
}); 