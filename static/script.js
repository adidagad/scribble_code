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








