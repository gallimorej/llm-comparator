from flask import Flask, render_template, request, jsonify
import aisuite

app = Flask(__name__)

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
