# Inonetecx AI Voice Assistant

A web and voice assistant prototype for Inonetecx. The project combines a branded frontend with a Python assistant that can answer common company, service, pricing, process, and contact questions.

## Features

- Branded web interface for the assistant experience
- Quick command buttons for common user questions
- Python-based intent recognition for company FAQs
- Voice recognition and text-to-speech support
- Conversation history handling in the assistant runtime
- Inonetecx service, pricing, team, process, and contact knowledge base

## Tech Stack

- Python
- SpeechRecognition
- pyttsx3
- HTML5
- CSS3
- Vanilla JavaScript
- Font Awesome

## Project Structure

```text
.
|-- inonetecx backend.py   # Main Python voice assistant
|-- html.html              # Web interface
|-- style.css              # Frontend styling
|-- script.js              # Frontend interactions
`-- README.md
```

## Run Locally

Install the required Python packages:

```bash
pip install SpeechRecognition pyttsx3
```

Run the assistant:

```bash
python "inonetecx backend.py"
```

Open `html.html` in a browser to view the web interface.

## Notes

The current frontend demo uses scripted responses for quick commands, while the Python file contains the richer voice assistant logic. A good next step is connecting the frontend to a backend API so both modes share the same assistant responses.

## Suggested Next Improvements

- Add a `requirements.txt` file for repeatable setup.
- Rename `inonetecx backend.py` to `inonetecx_backend.py` to make command-line usage easier.
- Add a Flask/FastAPI backend if the web interface should call the Python assistant directly.
- Add screenshots or a short demo GIF.
