from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import aisuite
import os

load_dotenv()

app = Flask(__name__)

# Now you can access the environment variables using os.getenv
# app_name = os.getenv('APP_NAME')
# region = os.getenv('REGION')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send_prompt', methods=['POST'])
def send_prompt():
    data = request.json
    prompt = data.get('prompt')
    llm1 = data.get('llm1')
    llm2 = data.get('llm2')

    response1 = aisuite.call_llm_api(llm1, prompt)
    response2 = aisuite.call_llm_api(llm2, prompt)

    return jsonify({'response1': response1, 'response2': response2})

if __name__ == '__main__':
    app.run(debug=True)
