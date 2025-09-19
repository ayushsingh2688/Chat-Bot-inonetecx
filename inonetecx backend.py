import speech_recognition as sr #type:ignore
import pyttsx3  #type:ignore
import datetime
import webbrowser
import time
import sys
import json
import logging
from typing import Dict, List, Optional, Tuple
import threading
import queue
import re
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('assistant.log'),
        logging.StreamHandler()
    ]
)

class AssistantState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"

@dataclass
class ConversationContext:
    last_topic: Optional[str] = None
    follow_up_questions: List[str] = None
    user_preferences: Dict = None
    session_start: datetime.datetime = None

class AdvancedInonetecxAssistant:
    def __init__(self):
        self.state = AssistantState.IDLE
        self.conversation_history = []
        self.context = ConversationContext(
            session_start=datetime.datetime.now(),
            follow_up_questions=[],
            user_preferences={}
        )
        self.audio_queue = queue.Queue()
        self.initialize_tts()
        self.load_knowledge_base()
        
    def initialize_tts(self):
        """Initialize text-to-speech with error handling"""
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            
            # Try to set a female voice (usually index 1)
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            else:
                self.engine.setProperty('voice', voices[0].id)
                
            self.engine.setProperty('rate', 165)  # Slightly faster
            self.engine.setProperty('volume', 0.9)
            
            logging.info("TTS initialized successfully")
        except Exception as e:
            logging.error(f"TTS initialization error: {e}")
            sys.exit(1)

    def load_knowledge_base(self):
        """Enhanced knowledge base with more detailed information"""
        self.knowledge_base = {
            "company_info": {
                "name": "Inonetecx",
                "tagline": "Innovating Tomorrow's Technology Today",
                "about": "Inonetecx is a cutting-edge technology solutions provider specializing in digital transformation, AI integration, and innovative software development. We empower businesses to thrive in the digital age.",
                "services": {
                    "web_development": {
                        "name": "Web Development",
                        "description": "Custom websites, e-commerce platforms, and web applications using latest technologies",
                        "technologies": ["React", "Angular", "Node.js", "Python", "PHP"],
                        "timeline": "2-8 weeks depending on complexity"
                    },
                    "mobile_development": {
                        "name": "Mobile App Development",
                        "description": "Native and cross-platform mobile applications for iOS and Android",
                        "technologies": ["React Native", "Flutter", "Swift", "Kotlin"],
                        "timeline": "6-16 weeks depending on features"
                    },
                    "cloud_solutions": {
                        "name": "Cloud Computing Solutions",
                        "description": "Cloud migration, infrastructure setup, and management services",
                        "technologies": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes"],
                        "timeline": "4-12 weeks depending on scale"
                    },
                    "ai_ml": {
                        "name": "AI/ML Integration",
                        "description": "Artificial intelligence and machine learning solutions for business automation",
                        "technologies": ["TensorFlow", "PyTorch", "OpenAI", "Hugging Face"],
                        "timeline": "8-20 weeks depending on complexity"
                    },
                    "digital_marketing": {
                        "name": "Digital Marketing Services",
                        "description": "SEO, social media marketing, content marketing, and PPC campaigns",
                        "technologies": ["Google Ads", "Facebook Ads", "Analytics", "SEO Tools"],
                        "timeline": "Ongoing monthly services"
                    },
                    "ui_ux": {
                        "name": "UI/UX Design",
                        "description": "User-centered design for websites and applications",
                        "technologies": ["Figma", "Adobe XD", "Sketch", "Photoshop"],
                        "timeline": "3-6 weeks depending on scope"
                    }
                },
                "clients": "78+ satisfied clients globally",
                "foundation": "2023",
                "mission": "To democratize technology and make it accessible for businesses of all sizes"
            },
            "pricing": {
                "web_development": {"start": 15000, "currency": "₹", "description": "Basic website starts from"},
                "mobile_development": {"start": 50000, "currency": "₹", "description": "Mobile app starts from"},
                "cloud_solutions": {"start": 40000, "currency": "₹", "description": "Cloud setup starts from"},
                "digital_marketing": {"start": 10000, "currency": "₹/month", "description": "Monthly marketing package starts from"},
                "ai_ml": {"start": 75000, "currency": "₹", "description": "AI/ML solution starts from"},
                "ui_ux": {"start": 20000, "currency": "₹", "description": "Design project starts from"},
                "enterprise_solutions": "Contact for custom enterprise pricing"
            },
            "contact": {
                "email": "contact@inonetecx.com",
                "phone": "+1 647-493-5614 (Canada)",
                "address": "180 Northfield Dr. W, unit 4 Waterloo, ON N2L 0C7, Canada",
                "website": "https://inonetecx.com",
                "business_hours": "Monday to Friday, 9:00 AM to 6:00 PM IST"
            },
            "team": {
                "size": "25+ skilled professionals",
                "expertise": ["Full-stack developers", "AI specialists", "Cloud architects", "UI/UX designers", "Digital marketing experts"],
                "experience": "Average 3+ years industry experience",
                "certifications": ["AWS Certified", "Google Cloud Professional", "Microsoft Azure Certified"]
            },
            "process": {
                "consultation": "Free initial consultation to understand your requirements",
                "planning": "Detailed project planning and timeline creation",
                "development": "Agile development with regular updates",
                "testing": "Comprehensive testing and quality assurance",
                "deployment": "Smooth deployment and go-live support",
                "maintenance": "Ongoing support and maintenance services"
            }
        }

    def speak(self, text: str, priority: bool = False):
        """Enhanced text-to-speech with queue management"""
        if priority:
            # Clear queue for priority messages
            while not self.audio_queue.empty():
                try:
                    self.audio_queue.get_nowait()
                except queue.Empty:
                    break
                    
        self.audio_queue.put(text)
        self._process_audio_queue()

    def _process_audio_queue(self):
        """Process audio queue in separate thread"""
        def speak_text():
            while not self.audio_queue.empty():
                try:
                    text = self.audio_queue.get_nowait()
                    self.state = AssistantState.SPEAKING
                    print(f"🤖 Assistant: {text}")
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.state = AssistantState.IDLE
                except queue.Empty:
                    break
                except Exception as e:
                    logging.error(f"Speech error: {e}")
                    
        thread = threading.Thread(target=speak_text, daemon=True)
        thread.start()

    def listen_with_wake_word(self, wake_words: List[str] = ["hey assistant", "computer"]) -> str:
        """Enhanced voice recognition with wake word detection"""
        recognizer = sr.Recognizer()
        
        # Improved settings for better recognition
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8
        recognizer.operation_timeout = 5
        
        for attempt in range(3):
            try:
                with sr.Microphone() as source:
                    if attempt == 0:
                        print(f"🎤 Calibrating microphone... (Attempt {attempt + 1}/3)")
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                    
                    print(f"🎤 Listening... (Attempt {attempt + 1}/3)")
                    print("💡 Tip: Speak clearly and pause briefly between words")
                    
                    self.state = AssistantState.LISTENING
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
                    self.state = AssistantState.PROCESSING
                    
                # Try multiple recognition methods
                command = None
                try:
                    command = recognizer.recognize_google(audio, language='en-IN')
                except sr.UnknownValueError:
                    try:
                        command = recognizer.recognize_google(audio, language='en-US')
                    except sr.UnknownValueError:
                        pass
                
                if command:
                    print(f"👤 You: {command}")
                    self.conversation_history.append(("user", command))
                    return command.lower()
                    
            except sr.WaitTimeoutError:
                if attempt < 2:
                    self.speak("I didn't hear anything. Please speak now.", priority=True)
                    time.sleep(1)
                continue
                
            except sr.RequestError as e:
                logging.error(f"Speech recognition service error: {e}")
                if attempt < 2:
                    self.speak("Network issue with speech service. Trying again.", priority=True)
                    time.sleep(2)
                continue
                
            except Exception as e:
                logging.error(f"Unexpected audio error: {e}")
                if attempt < 2:
                    self.speak("Technical issue detected. Please try again.", priority=True)
                    time.sleep(1)
                continue
        
        self.speak("Voice recognition failed. Let me switch to text input.", priority=True)
        try:
            return input("👤 You (type): ").lower()
        except KeyboardInterrupt:
            return "exit"

    def extract_intent_and_entities(self, command: str) -> Tuple[str, Dict]:
        """Advanced intent recognition and entity extraction"""
        command = command.lower().strip()
        intent = "unknown"
        entities = {}
        
        # Intent patterns with regex
        intent_patterns = {
            "greeting": r'\b(hello|hi|hey|namaste|good morning|good afternoon|good evening|hlo)\b',
            "about_company": r'\b(about|company|introduction|tell me about|what do you do|who are you)\b',
            "services": r'\b(services|offer|provide|work|what can you do|capabilities)\b',
            "pricing": r'\b(price|cost|charge|how much|pricing|expensive|cheap|budget)\b',
            "contact": r'\b(contact|reach|phone|email|address|location|get in touch)\b',
            "team": r'\b(team|people|employees|staff|developers|how many)\b',
            "process": r'\b(process|how do you work|methodology|approach|steps)\b',
            "technology": r'\b(technology|tech stack|tools|programming|languages)\b',
            "timeline": r'\b(timeline|how long|duration|time|when|deadline)\b',
            "portfolio": r'\b(portfolio|projects|work done|examples|case studies)\b',
            "website": r'\b(website|site|webpage|open site|show website)\b',
            "goodbye": r'\b(bye|exit|stop|quit|thank you|thanks|goodbye|see you)\b'
        }
        
        # Extract intent
        for intent_name, pattern in intent_patterns.items():
            if re.search(pattern, command):
                intent = intent_name
                break
        
        # Extract service entities
        service_patterns = {
            "web": r'\b(web|website|site)\b',
            "mobile": r'\b(mobile|app|application|android|ios)\b',
            "cloud": r'\b(cloud|aws|azure|server)\b',
            "ai": r'\b(ai|artificial intelligence|machine learning|ml)\b',
            "marketing": r'\b(marketing|seo|digital|social media)\b',
            "design": r'\b(design|ui|ux|user interface)\b'
        }
        
        for service, pattern in service_patterns.items():
            if re.search(pattern, command):
                entities["service"] = service
                break
        
        return intent, entities

    def generate_contextual_response(self, intent: str, entities: Dict, command: str) -> str:
        """Generate intelligent, contextual responses"""
        self.context.last_topic = intent
        
        if intent == "greeting":
            current_time = datetime.datetime.now()
            if current_time.hour < 12:
                greeting = "Good morning!"
            elif current_time.hour < 17:
                greeting = "Good afternoon!"
            else:
                greeting = "Good evening!"
            
            return f"{greeting} Welcome to Inonetecx. I'm your AI assistant. How can I help you transform your business with technology today?"

        elif intent == "about_company":
            company = self.knowledge_base["company_info"]
            return f"{company['about']} {company['tagline']}. We're founded in {company['foundation']} with a mission: {company['mission']}. Would you like to know about our specific services?"

        elif intent == "services":
            if "service" in entities:
                service_key = f"{entities['service']}_development" if entities['service'] in ["web", "mobile"] else f"{entities['service']}_solutions" if entities['service'] == "cloud" else f"{entities['service']}_ml" if entities['service'] == "ai" else f"digital_{entities['service']}" if entities['service'] == "marketing" else f"ui_ux" if entities['service'] == "design" else entities['service']
                
                if service_key in self.knowledge_base["company_info"]["services"]:
                    service = self.knowledge_base["company_info"]["services"][service_key]
                    return f"{service['description']}. We use technologies like {', '.join(service['technologies'])}. Typical timeline is {service['timeline']}. Would you like to know about pricing?"
                    
            services_list = [service["name"] for service in self.knowledge_base["company_info"]["services"].values()]
            return f"We offer comprehensive technology solutions: {', '.join(services_list)}. Which service interests you most? I can provide detailed information about any of them."

        elif intent == "pricing":
            if "service" in entities:
                service = entities["service"]
                if service == "web":
                    price = self.knowledge_base["pricing"]["web_development"]
                    return f"Our web development {price['description']} {price['currency']}{price['start']:,}. This includes responsive design, basic SEO, and 3 months free support. Shall I connect you with our team for a detailed quote?"
                elif service == "mobile":
                    price = self.knowledge_base["pricing"]["mobile_development"]
                    return f"Our mobile app development {price['description']} {price['currency']}{price['start']:,}. This covers both Android and iOS with basic features. Complex apps may cost more. Would you like a free consultation?"
                # Add more service-specific pricing...
                    
            pricing = self.knowledge_base["pricing"]
            return f"Here's our starting pricing: Web Development from ₹{pricing['web_development']['start']:,}, Mobile Apps from ₹{pricing['mobile_development']['start']:,}, Cloud Solutions from ₹{pricing['cloud_solutions']['start']:,}. All projects include free consultation and post-launch support. Which service interests you?"

        elif intent == "contact":
            contact = self.knowledge_base["contact"]
            return f"You can reach us at: 📧 Email: {contact['email']}, 📞 Phone: {contact['phone']}, 📍 Address: {contact['address']}. Our business hours are {contact['business_hours']}. Would you like me to open our website for more information?"

        elif intent == "team":
            team = self.knowledge_base["team"]
            return f"We have {team['size']} with expertise in {', '.join(team['expertise'])}. Our team has {team['experience']} and holds certifications like {', '.join(team['certifications'])}. We follow agile methodologies and maintain high code quality standards."

        elif intent == "process":
            process = self.knowledge_base["process"]
            steps = [f"{i+1}. {step.capitalize()}: {desc}" for i, (step, desc) in enumerate(process.items())]
            return f"Our development process follows these steps: {' → '.join([f'{i+1}. {step.capitalize()}' for i, step in enumerate(process.keys())])}. We ensure transparency and regular communication throughout. Would you like details about any specific phase?"

        elif intent == "timeline":
            if "service" in entities:
                service_key = f"{entities['service']}_development" if entities['service'] in ["web", "mobile"] else f"{entities['service']}_solutions"
                if service_key in self.knowledge_base["company_info"]["services"]:
                    timeline = self.knowledge_base["company_info"]["services"][service_key]["timeline"]
                    return f"For {entities['service']} projects, typical timeline is {timeline}. However, exact timeline depends on your specific requirements. Shall I schedule a free consultation to give you a precise estimate?"
                    
            return "Project timelines vary by complexity: Web Development (2-8 weeks), Mobile Apps (6-16 weeks), Cloud Solutions (4-12 weeks), AI/ML Projects (8-20 weeks). We always provide detailed timelines after understanding your requirements."

        elif intent == "website":
            try:
                webbrowser.open(self.knowledge_base["contact"]["website"], new=2)
                return f"Opening our website {self.knowledge_base['contact']['website']} in your browser. You can explore our portfolio, read client testimonials, and get in touch directly through the contact form."
            except Exception as e:
                logging.error(f"Browser error: {e}")
                return f"Please visit our website: {self.knowledge_base['contact']['website']} to see our portfolio and get detailed information about our services."

        elif intent == "goodbye":
            session_duration = datetime.datetime.now() - self.context.session_start
            return f"Thank you for spending {session_duration.seconds//60} minutes with me! It was great helping you learn about Inonetecx. Feel free to contact us anytime for your technology needs. Have a wonderful day! 🚀"

        else:
            # Intelligent fallback with suggestions
            suggestions = [
                "our services and pricing",
                "our development process",
                "our team and expertise",
                "contact information",
                "project timelines"
            ]
            return f"I'd love to help you with that! I specialize in information about {', '.join(suggestions)}. You can also ask me to 'open our website' or say 'goodbye' when you're done. What would you like to know more about?"

    def run_assistant(self):
        """Main assistant loop with enhanced features"""
        print("🚀 Initializing Advanced Inonetecx Assistant...")
        self.speak("Initializing advanced systems...", priority=True)
        time.sleep(1)
        
        print("🎤 Audio systems calibrated")
        self.speak("Audio systems calibrated. All systems ready.", priority=True)
        time.sleep(1)
        
        welcome_msg = f"Hello! I'm your intelligent Inonetecx assistant. Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}. I'm here to help you discover how we can transform your business with cutting-edge technology solutions."
        print(f"🤖 {welcome_msg}")
        self.speak(welcome_msg)
        
        print("""
🎯 What I can help you with:
   • Company information and our mission
   • Detailed service descriptions and technologies
   • Transparent pricing and project timelines  
   • Team expertise and certifications
   • Our proven development process
   • Contact information and business hours
   • Portfolio examples and client success stories
   • Technical specifications and requirements

💡 Pro tips:
   • Speak clearly and naturally
   • You can ask follow-up questions
   • Say 'open website' to visit our site
   • Say 'goodbye' when you're ready to leave

🎤 Ready to listen! How can I help you today?
        """)
        
        consecutive_errors = 0
        max_errors = 3
        
        while True:
            try:
                command = self.listen_with_wake_word()
                
                if not command or command.strip() == "":
                    consecutive_errors += 1
                    if consecutive_errors >= max_errors:
                        self.speak("I'm experiencing persistent audio issues. Please restart the assistant for the best experience.", priority=True)
                        break
                    self.speak("I didn't catch that. Could you please try again?", priority=True)
                    continue
                else:
                    consecutive_errors = 0
                
                # Process command with advanced NLP
                intent, entities = self.extract_intent_and_entities(command)
                response = self.generate_contextual_response(intent, entities, command)
                
                # Add to conversation history
                self.conversation_history.append(("assistant", response))
                
                # Speak response
                self.speak(response)
                
                # Check for exit conditions
                if intent == "goodbye":
                    time.sleep(2)
                    self.speak("Assistant shutting down. Thank you for choosing Inonetecx!", priority=True)
                    break
                    
                # Suggest follow-up based on context
                if intent in ["services", "pricing"] and len(self.conversation_history) < 10:
                    time.sleep(1)
                    follow_up = "Is there anything specific about this service you'd like to know more about?"
                    self.speak(follow_up)
                
            except KeyboardInterrupt:
                print("\n🛑 Assistant interrupted by user")
                self.speak("Assistant interrupted. Goodbye!", priority=True)
                break
            except Exception as e:
                logging.error(f"Unexpected error in main loop: {e}")
                self.speak("I encountered a technical issue. Please try again or restart the assistant.", priority=True)
                consecutive_errors += 1
                if consecutive_errors >= max_errors:
                    break

def main():
    """Initialize and run the advanced assistant"""
    try:
        assistant = AdvancedInonetecxAssistant()
        assistant.run_assistant()
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Goodbye! 👋")
    except Exception as e:
        logging.critical(f"Critical error: {e}")
        print(f"Critical error occurred: {e}")
        print("Please check the logs and restart the application.")

if __name__ == "__main__":
    main()