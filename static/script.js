// script.js

function populateSelectBoxes(config) {
    const llm1Select = document.getElementById('llm1');
    const llm2Select = document.getElementById('llm2');

    // Clear existing options
    llm1Select.innerHTML = '<option value="" disabled selected>Select an LLM</option>';
    llm2Select.innerHTML = '<option value="" disabled selected>Select an LLM</option>';

    for (const provider in config.providers) {
        const optgroup = document.createElement('optgroup');
        optgroup.label = provider;

        config.providers[provider].forEach(model => {
            const option = document.createElement('option');
            option.value = `${provider.toLowerCase()}:${model}`;
            option.textContent = option.value;
            optgroup.appendChild(option);
        });

        llm1Select.appendChild(optgroup.cloneNode(true));
        llm2Select.appendChild(optgroup.cloneNode(true));
    }
}

function updateCharacterCount() {
    const prompt = document.getElementById('prompt');
    const characterCounter = document.getElementById('characterCounter');
    characterCounter.innerText = `${prompt.value.length}/524288`;
}

async function refreshConfig() {
    try {
        const response = await fetch('/api/refresh_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        
        if (data.success) {
            // After successful refresh, get the new config
            const configResponse = await fetch('/api/get_config');
            const config = await configResponse.json();
            populateSelectBoxes(config);
            alert('Config refreshed successfully');
        } else {
            alert('Failed to refresh config: ' + data.message);
        }
    } catch (error) {
        console.error('Error refreshing config:', error);
        alert('Error refreshing config. See console for details.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Initial config load
    fetch('/api/get_config')
        .then(response => response.json())
        .then(config => populateSelectBoxes(config))
        .catch(error => {
            console.error('Error loading config:', error);
            alert('Error loading config. See console for details.');
        });

    // Add event listener to update character count
    const prompt = document.getElementById('prompt');
    prompt.addEventListener('input', updateCharacterCount);

    // Add refresh config button if it doesn't exist
    if (!document.getElementById('refreshConfigBtn')) {
        const buttonContainer = document.querySelector('.button-container');
        const refreshButton = document.createElement('button');
        refreshButton.id = 'refreshConfigBtn';
        refreshButton.onclick = refreshConfig;
        refreshButton.textContent = 'Refresh Config';
        buttonContainer.appendChild(refreshButton);
    }
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

function improvePrompt() {
    const prompt = document.getElementById('prompt').value;

    fetch('/api/improve_prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('prompt').value = data.improved_prompt;
        updateCharacterCount();
    })
    .catch(error => {
        console.error('Error improving prompt:', error);
    });
}

function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).value;
    navigator.clipboard.writeText(text).then(() => {
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}