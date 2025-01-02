// script.js

function populateSelectBoxes(config) {
    const llm1Select = document.getElementById('llm1');
    const llm2Select = document.getElementById('llm2');

    for (const provider in config.providers) {
        const optgroup = document.createElement('optgroup');
        optgroup.label = provider;

        config.providers[provider].forEach(model => {
            const option = document.createElement('option');
            option.value = `${provider.toLowerCase()}:${model}`;
            option.textContent = option.value
            optgroup.appendChild(option);
        });

        llm1Select.appendChild(optgroup.cloneNode(true));
        llm2Select.appendChild(optgroup.cloneNode(true));
    }
}

function updateCharacterCount() {
    const prompt = document.getElementById('prompt');
    const characterCounter = document.getElementById('characterCounter');
    characterCounter.innerText = `${prompt.value.length}/500`;
}

document.addEventListener('DOMContentLoaded', () => {
    fetch('/static/config.json')
        .then(response => response.json())
        .then(config => populateSelectBoxes(config))
        .catch(error => console.error('Error loading config:', error));

    // Add event listener to update character count
    const prompt = document.getElementById('prompt');
    prompt.addEventListener('input', updateCharacterCount);
});

function sendPrompt() {
    const prompt = document.getElementById('prompt').value;
    const llm1 = document.getElementById('llm1').value;
    const llm2 = document.getElementById('llm2').value;

    if (!prompt.trim()) {
        alert('Please enter a prompt.');
        document.getElementById('prompt').focus(); // Set focus to the prompt textarea
        return;
    }
    
    if (!llm1) {
        alert('Please select LLM 1.');
        document.getElementById('llm1').focus(); // Set focus to the LLM 1 select box
        return;
    }

    if (!llm2) {
        alert('Please select LLM 2.');
        document.getElementById('llm2').focus(); // Set focus to the LLM 2 select box
        return;
    }

    // Update the label for response1
    document.getElementById('response1-label').textContent = llm1;
    document.getElementById('response2-label').textContent = llm2;

    fetch('/api/send_prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt, llm1, llm2 })
    })
    .then(response => response.json())
    .then(data => {
        // Store the raw markdown responses in hidden fields
        document.getElementById('mdResponse1').value = data.response1;
        document.getElementById('mdResponse2').value = data.response2;

        document.getElementById('response1').innerHTML = marked.parse(data.response1);
        document.getElementById('response2').innerHTML = marked.parse(data.response2);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request.');
    });
}

function clearPrompt() {
    document.getElementById('prompt').value = '';
    document.getElementById('characterCounter').innerText = '0/500';
    updateCharacterCount();
}

function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).value;
    navigator.clipboard.writeText(text).then(() => {
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}