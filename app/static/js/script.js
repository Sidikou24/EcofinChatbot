function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    const chatBox = document.getElementById('chat-box');
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'message user';
    userMessageDiv.textContent = userInput;
    chatBox.appendChild(userMessageDiv);

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Un problème est survenu');
        }
        return response.json();
    })
    .then(data => {
        const botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'message bot';
        botMessageDiv.textContent = data.response;
        chatBox.appendChild(botMessageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        const errorMessageDiv = document.createElement('div');
        errorMessageDiv.className = 'message error';
        errorMessageDiv.textContent = 'Désolé, une erreur s\'est produite.';
        chatBox.appendChild(errorMessageDiv);
    });

    document.getElementById('user-input').value = '';
}