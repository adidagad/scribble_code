/*document.getElementById('slide-btn').addEventListener('click', function() {
    const ocrOutput = document.getElementById('ocr-output');
    // Toggle the 'open' class
    ocrOutput.classList.toggle('open');
    // Change the button symbol depending on the panel state
    this.innerHTML = ocrOutput.classList.contains('open') ? '&lt;' : '&gt;';
});

document.getElementById('capture-btn').addEventListener('click', function() {
    fetch('/capture_ocr')
        .then(response => response.json())
        .then(data => {
            const textArea = document.getElementById('text-area');
            if (data.extracted_text) {
                // Populate the text area with OCR output
                textArea.value = data.extracted_text;
                textArea.removeAttribute('readonly'); // Ensure it can be edited
            } else {
                textArea.value = 'Error capturing image or no text detected.';
            }
        })
        .catch(err => console.error(err));
});*/



// Switch between OCR and C++ Code editor
document.getElementById('ocr-tab').addEventListener('click', function() {
    const editorArea = document.getElementById('editor-area');
    this.classList.add('active');
    document.getElementById('code-tab').classList.remove('active');
    
    fetch('/capture_ocr')
        .then(response => response.json())
        .then(data => {
            editorArea.value = data.extracted_text || 'Error capturing image or no text detected.';
        })
        .catch(err => console.error(err));
});

document.getElementById('code-tab').addEventListener('click', function() {
    const editorArea = document.getElementById('editor-area');
    this.classList.add('active');
    document.getElementById('ocr-tab').classList.remove('active');
    editorArea.value = ''; // Clear the editor for writing code
    editorArea.placeholder = 'Enter C++ code here';
});

// Run the C++ code
document.getElementById('run-code-btn').addEventListener('click', function() {
    const code = document.getElementById('editor-area').value;
    fetch('/run_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code }),
    })
    .then(response => response.json())
    .then(data => {
        const outputArea = document.getElementById('output-area');
        outputArea.value = data.output || data.error;
    })
    .catch(err => console.error(err));
});








