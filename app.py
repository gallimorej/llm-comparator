from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import aisuite
import os
import json
import requests
from config_manager import ConfigManager

load_dotenv()

app = Flask(__name__)

# Initialize the config manager
try:
    config_manager = ConfigManager()
except ValueError as e:
    print(f"Error initializing config manager: {e}")
    raise

# Initialize the AI client for accessing the language model
client = aisuite.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/refresh_config', methods=['POST'])
def refresh_config():
    """Endpoint to manually refresh the config"""
    success, message = config_manager.refresh_config()
    return jsonify({
        'success': success,
        'message': message
    })

@app.route('/api/get_config')
def get_config():
    """Endpoint to get current config"""
    try:
        return jsonify(config_manager.get_config())
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

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

@app.route('/api/improve_prompt', methods=['POST'])
def improve_prompt():
    data = request.json
    prompt = data.get('prompt')
    
    # Get the improvePromptRecipeURL from the config
    config = config_manager.get_config()
    recipe_url = config.get('improvePromptRecipeURL')
    
    # Fetch the content from the improvePromptRecipeURL
    response = requests.get(recipe_url)
    if response.status_code == 200:
        improved_prompt = response.text + prompt
    else:
        improved_prompt = prompt  # Fallback to the original prompt if the fetch fails

    return jsonify({'improved_prompt': improved_prompt})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
