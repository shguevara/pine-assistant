from flask import Flask, request, jsonify
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize Pinecone client
api_key = os.environ.get('PINECONE_API_KEY')
if not api_key:
    raise ValueError("PINECONE_API_KEY environment variable is not set.")
pc = Pinecone(api_key=api_key)

# Create Assistant object
assistant_name = os.environ.get('ASSISTANT_NAME', 'DefaultAssistant')
assistant = pc.assistant.Assistant(assistant_name=assistant_name)

# Define helper function to interact with the assistant
def chat_with_assistant(question):
    chat_context = [Message(content=question)]
    response = assistant.chat_completions(messages=chat_context)
    return response.choices[0].message.content

# Define endpoint for POST requests
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    if not data or 'question' not in data:
        return jsonify({"error": "No question provided"}), 400

    question = data['question']
    answer = chat_with_assistant(question)
    return jsonify({"answer": answer})

# Main entry point
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Render provides the port as an environment variable
    app.run(host='0.0.0.0', port=port)
