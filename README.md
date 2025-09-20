# Inonetecx AI Voice Assistant

A modern web-based AI voice assistant for Inonetecx with both web interface and voice capabilities.

## Features

- 🤖 Intelligent AI responses using advanced NLP
- 🎤 Voice recognition and text-to-speech
- 🌐 Modern web interface
- 📱 Responsive design
- 🔄 Real-time communication between frontend and backend
- 💬 Interactive chat interface
- 🎯 Quick command buttons

## Quick Start (Recommended)

### Option 1: Easy Startup Script
```bash
python start_assistant.py
```
This will automatically:
- Check and install dependencies
- Start the backend server
- Open the web interface in your browser

### Option 2: Manual Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Test the setup:
```bash
python test_setup.py
```

3. Run the application:
```bash
python "inonetecx backend.py"
```

4. Choose mode:
   - **1. Web Interface (Recommended)**: Opens a web server at http://127.0.0.1:5000
   - **2. Voice Interface**: Direct voice interaction in terminal

5. Open `html.html` in your browser

## Usage

### Web Interface
1. Start the backend with option 1
2. Open your browser and go to http://127.0.0.1:5000
3. Use the quick command buttons or type messages
4. The assistant will respond with intelligent, contextual answers

### Voice Interface
1. Start the backend with option 2
2. Speak naturally to the assistant
3. The assistant will listen and respond with voice

## API Endpoints

- `GET /api/status` - Check backend status
- `POST /api/chat` - Send message to assistant
- `POST /api/clear` - Clear conversation history

## Technologies Used

- **Backend**: Python, Flask, Speech Recognition, Text-to-Speech
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI**: Natural Language Processing, Intent Recognition
- **Communication**: REST API, CORS enabled

## Project Structure

```
├── inonetecx backend.py    # Main Python backend
├── html.html              # Web interface
├── script.js              # Frontend JavaScript
├── style.css              # Styling
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Support

For any issues or questions, contact Inonetecx at:
- Email: contact@inonetecx.com
- Phone: +1 647-493-5614
- Website: https://inonetecx.com
