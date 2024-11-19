from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from html import escape
import re  # For pattern matching

app = Flask(__name__)

# MongoDB Connection (Optional: Uncomment if you want to use MongoDB)
# mongo_client = MongoClient('mongo')  # Connect to the MongoDB container
# db = mongo_client["message_db"]
# faqs_collection = db["faqs"]


# Bot Message Logic
def bot_message_handler(user_message):
    """
    Handles user input and generates a bot response based on predefined logic.
    """
    # Example Rule-Based Responses
    if "hello" in user_message.lower():
        return "Hi there! How can I assist you today?"
    elif re.search(r'\b(help|support|issue)\b', user_message.lower()):
        return "Sure, let me know what issue you're facing, and I'll try to help."
    elif "docker" in user_message.lower():
        return "Docker is a platform to develop, ship, and run applications inside containers."
    elif "flask" in user_message.lower():
        return "Flask is a lightweight Python web framework. You can start by running `python server.py`."
    elif "mongo" in user_message.lower():
        return "I see you're asking about MongoDB. Are you facing a specific issue with it?"
    elif "bye" in user_message.lower():
        return "Goodbye! Have a great day."
    else:
        # Placeholder for MongoDB dynamic response (Optional)
        # faq = faqs_collection.find_one({"question": {"$regex": user_message, "$options": "i"}})
        # if faq:
        #     return faq["answer"]
        return "I'm sorry, I don't understand that. Could you rephrase?"


# Flask Routes
@app.route('/')
def index():
    """
    Serves the main HTML interface (e.g., chatbot UI).
    """
    return render_template("index.html")  # Ensure index.html is present in the 'templates' folder


@app.route('/message_sent', methods=['POST'])
def message_handler():
    """
    Handles user messages sent to the bot and generates responses.
    """
    if request.method == 'POST':
        # Get user message from the request payload
        user_message = request.get_json().get("message", "").strip()

        # Process the user's message through the bot logic
        bot_response = bot_message_handler(user_message)

        # Return the conversation as a JSON array
        return jsonify([
            {"name": "user", "message": escape(user_message)},
            {"name": "bot", "message": bot_response}
        ])
    else:
        # Return a 403 Forbidden response for non-POST requests
        return '', 403


if __name__ == "__main__":
    # Run the Flask app
    # Accessible via http://localhost:8080/ when running locally
    app.run(host="0.0.0.0", port=8080, debug=True)
b