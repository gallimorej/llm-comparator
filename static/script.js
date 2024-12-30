// script.js
function sendPrompt() {
    const prompt = document.getElementById('prompt').value;
    const llm1 = document.getElementById('llm1').value;
    const llm2 = document.getElementById('llm2').value;

    fetch('/api/send_prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt, llm1, llm2 })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response1').textContent = data.response1;
        document.getElementById('response2').textContent = data.response2;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request.');
    });
}

function clearPrompt() {
    document.getElementById('prompt').value = '';
    document.getElementById('characterCounter').innerText = '0/500';
}