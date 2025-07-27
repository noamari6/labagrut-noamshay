import os
from flask import Flask, request, jsonify
import openai

"""
Simple Flask application that proxies requests to OpenAI's ChatCompletion API.
The OpenAI API key should be provided via the OPENAI_API_KEY environment variable
on the hosting platform. This keeps the secret out of client-side code.

Endpoint:
POST /chat
Body JSON: { "messages": [ {"role": "user"|"assistant"|"system", "content": "..."} ] }
Returns: { "reply": "..." }
"""

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get('messages', [])
    if not isinstance(messages, list):
        return jsonify({'error': 'Invalid messages format'}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except Exception:
        return jsonify({'error': 'Failed to generate response'}), 500

if __name__ == '__main__':
    # When running locally for testing
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
