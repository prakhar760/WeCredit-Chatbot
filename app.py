from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS  # ✅ Allows frontend to communicate with backend
import os

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS to allow frontend requests

# Load API key
api_key = "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"
if not api_key:
    raise ValueError("Missing API key. Set GROQ_API_KEY as an environment variable.")

client = Groq(api_key=api_key)

# Default Homepage Route
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the WeCredit Chatbot API! Use /chat for interactions."

# Chatbot Route
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # ✅ Make a request to Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a chatbot in a company, WeCredit. Services provided by WeCredit: Personal loan, Credit Card, Business loan. You have foundational knowledge of key financial concepts, specifically in areas such as loans, credit reports, interest rates in India"},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",  # ✅ Correct model
            # max_tokens=500
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
