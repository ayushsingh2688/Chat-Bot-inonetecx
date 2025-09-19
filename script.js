document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const clearChat = document.getElementById('clearChat');
    const conversationMessages = document.getElementById('conversationMessages');
    const commandButtons = document.querySelectorAll('.command-btn');

    startBtn.addEventListener('click', function() {
        startBtn.disabled = true;
        stopBtn.disabled = false;
        
        addMessage('user', 'Listening...');

        setTimeout(function() {
            addMessage('assistant', 'I heard you say something. How can I help you?');
        }, 2000);
    });

    stopBtn.addEventListener('click', function() {
        startBtn.disabled = false;
        stopBtn.disabled = true;

        addMessage('user', 'Stopped listening');
    });

    clearChat.addEventListener('click', function() {
        conversationMessages.innerHTML = '';
        addMessage('assistant', 'Hello! I\'m your Inonetecx AI assistant. How can I help you today?');
    });

    commandButtons.forEach(button => {
        button.addEventListener('click', function() {
            const command = this.getAttribute('data-command');

            addMessage('user', command);
            
            setTimeout(function() {
                let response = '';

                switch (command) {
                    case 'about company':
                        response = 'Inonetecx is a technology company specializing in AI solutions, web development, and digital services. We help businesses transform with cutting-edge technology.';
                        break;
                    case 'services':
                        response = 'We offer web development, AI voice assistants, cloud services, and digital marketing. Our solutions are tailored to meet your specific business needs.';
                        break;
                    case 'pricing':
                        response = 'Our pricing varies based on project requirements. Web development starts at Rs 50,000, AI voice assistants at Rs 40,000, cloud services at Rs 30,000/month, and digital marketing at Rs 25,000/month.';
                        break;
                    case 'contact information':
                        response = 'You can reach us at info@inonetecx.com or call us at +1 647-493-5614 (Canada). Our office is open from 9 AM to 5 PM, Monday through Friday.';
                        break;
                    default:
                        response = 'I\'m not sure how to help with that. Can you please rephrase your question?';
                }
                addMessage('assistant', response);
            }, 1500);
        });
    });

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';

        const icon = document.createElement('i');
        icon.className = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
        avatarDiv.appendChild(icon);

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const paragraph = document.createElement('p');
        paragraph.textContent = text;

        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = 'Just now';

        contentDiv.appendChild(paragraph);
        contentDiv.appendChild(timeSpan);

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        conversationMessages.appendChild(messageDiv);

        conversationMessages.scrollTop = conversationMessages.scrollHeight;
    }
});