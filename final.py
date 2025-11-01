from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Simple responses dictionary
responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I help?"],
    "how are you": ["I'm good! Thanks for asking!", "Doing great! How about you?"],
    "what is your name": ["I'm ChatBot!", "You can call me ChatBot!"],
    "bye": ["Goodbye!", "See you later!", "Bye! Have a great day!"],
    "thanks": ["You're welcome!", "Happy to help!", "Anytime!"],
    "joke": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!"
    ],
    "default": [
        "I'm not sure I understand. Can you rephrase?",
        "That's interesting! Tell me more.",
        "I'm still learning. Could you try saying that differently?"
    ]
}

def get_response(message):
    message = message.lower().strip()
    
    
    if any(word in message for word in ["hello", "hi", "hey"]):
        return random.choice(responses["hello"])
    elif any(word in message for word in ["how are you", "how do you feel"]):
        return random.choice(responses["how are you"])
    elif any(word in message for word in ["your name", "who are you"]):
        return random.choice(responses["what is your name"])
    elif any(word in message for word in ["bye", "goodbye", "see you"]):
        return random.choice(responses["bye"])
    elif any(word in message for word in ["thank", "thanks"]):
        return random.choice(responses["thanks"])
    elif any(word in message for word in ["joke", "funny", "laugh"]):
        return random.choice(responses["joke"])
    else:
        return random.choice(responses["default"])

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple ChatBot</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }

            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                width: 100%;
                max-width: 500px;
                animation: fadeIn 0.8s ease-out;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .header {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }

            .header h1 {
                font-size: 2.2em;
                margin-bottom: 8px;
                font-weight: 700;
            }

            .header p {
                opacity: 0.9;
                font-size: 1.1em;
            }

            .chat-container {
                padding: 25px;
            }

            .chat-box {
                height: 350px;
                border: 2px solid #e8f4f8;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                overflow-y: auto;
                background: #fafcff;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            .message {
                max-width: 80%;
                padding: 12px 18px;
                border-radius: 18px;
                line-height: 1.4;
                position: relative;
                animation: messageSlide 0.3s ease-out;
            }

            @keyframes messageSlide {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .user-message {
                align-self: flex-end;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                border-bottom-right-radius: 5px;
                box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
            }

            .bot-message {
                align-self: flex-start;
                background: white;
                color: #333;
                border: 1px solid #e1e8f0;
                border-bottom-left-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            }

            .input-container {
                display: flex;
                gap: 12px;
                align-items: center;
            }

            #userInput {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #e1e8f0;
                border-radius: 25px;
                font-size: 14px;
                outline: none;
                transition: all 0.3s ease;
                background: white;
            }

            #userInput:focus {
                border-color: #4facfe;
                box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
                transform: translateY(-1px);
            }

            #userInput::placeholder {
                color: #a0aec0;
            }

            #sendButton {
                padding: 15px 25px;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
            }

            #sendButton:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
            }

            #sendButton:active {
                transform: translateY(0);
            }

            .suggestions {
                margin-top: 20px;
                text-align: center;
            }

            .suggestions p {
                margin-bottom: 12px;
                color: #718096;
                font-size: 14px;
                font-weight: 500;
            }

            .suggestion-chips {
                display: flex;
                gap: 8px;
                justify-content: center;
                flex-wrap: wrap;
            }

            .suggestion-chip {
                padding: 8px 16px;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.3s ease;
                color: #4a5568;
            }

            .suggestion-chip:hover {
                background: #4facfe;
                color: white;
                transform: translateY(-2px);
                border-color: #4facfe;
                box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
            }

            /* Scrollbar styling */
            .chat-box::-webkit-scrollbar {
                width: 6px;
            }

            .chat-box::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 3px;
            }

            .chat-box::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 3px;
            }

            .chat-box::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8;
            }

            /* Typing indicator */
            .typing-indicator {
                display: inline-flex;
                align-items: center;
                padding: 12px 18px;
                background: white;
                border: 1px solid #e1e8f0;
                border-radius: 18px;
                border-bottom-left-radius: 5px;
            }

            .typing-dot {
                width: 8px;
                height: 8px;
                background: #a0aec0;
                border-radius: 50%;
                margin: 0 2px;
                animation: typing 1.4s infinite ease-in-out;
            }

            .typing-dot:nth-child(1) { animation-delay: -0.32s; }
            .typing-dot:nth-child(2) { animation-delay: -0.16s; }

            @keyframes typing {
                0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
                40% { transform: scale(1); opacity: 1; }
            }

            /* Responsive design */
            @media (max-width: 600px) {
                body {
                    padding: 10px;
                }
                
                .container {
                    border-radius: 15px;
                }
                
                .header {
                    padding: 25px 20px;
                }
                
                .header h1 {
                    font-size: 1.8em;
                }
                
                .chat-container {
                    padding: 20px;
                }
                
                .chat-box {
                    height: 300px;
                }
                
                .message {
                    max-width: 90%;
                }
                
                .input-container {
                    flex-direction: column;
                }
                
                #sendButton {
                    width: 100%;
                    justify-content: center;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 ChatBot</h1>
                <p>Your friendly AI assistant</p>
            </div>

            <div class="chat-container">
                <div class="chat-box" id="chatBox">
                    <div class="message bot-message">
                        Hello! I'm your friendly chatbot. How can I help you today? 😊
                    </div>
                </div>

                <div class="input-container">
                    <input type="text" id="userInput" placeholder="Type your message here..." autocomplete="off">
                    <button id="sendButton">
                        <span>Send</span>
                        <span>🚀</span>
                    </button>
                </div>

                <div class="suggestions">
                    <p>Try asking:</p>
                    <div class="suggestion-chips">
                        <button class="suggestion-chip" data-message="Hello">Hello 👋</button>
                        <button class="suggestion-chip" data-message="How are you?">How are you? 😊</button>
                        <button class="suggestion-chip" data-message="Tell me a joke">Tell a joke 😂</button>
                        <button class="suggestion-chip" data-message="What is your name?">Your name 🤖</button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function sendMessage() {
                const input = document.getElementById('userInput');
                const message = input.value;
                const chatBox = document.getElementById('chatBox');
                
                if (!message.trim()) return;
                
                // Add user message
                const userMessage = document.createElement('div');
                userMessage.className = 'message user-message';
                userMessage.textContent = message;
                chatBox.appendChild(userMessage);
                input.value = '';
                
                // Show typing indicator
                const typingIndicator = document.createElement('div');
                typingIndicator.className = 'message bot-message';
                typingIndicator.id = 'typingIndicator';
                typingIndicator.innerHTML = `
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                `;
                chatBox.appendChild(typingIndicator);
                chatBox.scrollTop = chatBox.scrollHeight;
                
                // Send to bot
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    // Remove typing indicator
                    const typing = document.getElementById('typingIndicator');
                    if (typing) typing.remove();
                    
                    // Add bot response
                    const botMessage = document.createElement('div');
                    botMessage.className = 'message bot-message';
                    botMessage.textContent = data.response;
                    chatBox.appendChild(botMessage);
                    chatBox.scrollTop = chatBox.scrollHeight;
                })
                .catch(error => {
                    console.error('Error:', error);
                    const typing = document.getElementById('typingIndicator');
                    if (typing) typing.remove();
                    
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'message bot-message';
                    errorMessage.textContent = 'Sorry, something went wrong. Please try again.';
                    chatBox.appendChild(errorMessage);
                    chatBox.scrollTop = chatBox.scrollHeight;
                });
            }
            
            // Send message on Enter key
            document.getElementById('userInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
            
            // Suggestion chips
            document.querySelectorAll('.suggestion-chip').forEach(chip => {
                chip.addEventListener('click', function() {
                    const message = this.getAttribute('data-message');
                    document.getElementById('userInput').value = message;
                    sendMessage();
                });
            });
            
            // Auto-focus input
            document.getElementById('userInput').focus();
        </script>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    bot_response = get_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    print("🚀 Starting Simple ChatBot...")
    print("📍 Open: http://localhost:5000")
    print("💬 Try: Hello, How are you?, What's your name?, Tell me a joke")
    app.run(debug=True)