from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import aisuite
import os

load_dotenv()

app = Flask(__name__)

# Now you can access the environment variables using os.getenv
# app_name = os.getenv('APP_NAME')
# region = os.getenv('REGION')

# Initialize the AI client for accessing the language model
client = aisuite.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send_prompt', methods=['POST'])
def send_prompt():
    data = request.json
    prompt = data.get('prompt')
    llm1 = data.get('llm1')
    llm2 = data.get('llm2')
    
    # Define a conversation with a system message and a user message
    messages = [
        {"role": "system", "content": "You are a helpful agent, who answers with brevity. Provide all answers in markdown."},
        {"role": "user", "content": prompt},
    ]
    response1 = client.chat.completions.create(llm1, messages)
    response2 = client.chat.completions.create(llm2, messages)

    return jsonify({'response1': response1.choices[0].message.content, 'response2': response2.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)
