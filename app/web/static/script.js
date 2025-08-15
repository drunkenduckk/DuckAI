document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const userMessage = input.value.trim();
        if (!userMessage) return;

        addMessage(userMessage, 'user-message');
        input.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage })
            });
            const data = await response.json();
            addMessage(data.reply, 'ai-message');
        } catch (error) {
            addMessage('Error: Could not reach the server.', 'ai-message');
        }
    });

    function addMessage(text, className) {
        const msg = document.createElement('div');
        msg.classList.add('message', className);
        msg.textContent = text;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
