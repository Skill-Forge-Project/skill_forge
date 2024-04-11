// Function to handle CodeMirror field in the Quest editor form when user open a specific quest for submitings.

// Initialize CodeMirror editors
var editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    lineNumbers: true,
    theme: "dracula",
    indentUnit: 2,
    autoCloseBrackets: true,
    matchBrackets: true,
    scrollbars: true
});

// Function to update modes of CodeMirror editors
function updateModes(selectedLanguage) {
    var mode;
    switch (selectedLanguage) {
        case 'Python':
            mode = 'python';
            break;
        case 'JavaScript':
            mode = 'javascript';
            break;
        case 'Java':
            mode = 'text/x-java';
            break;
        case 'C#':
            mode = 'text/x-csharp';
            break;
    }
    editor.setOption("mode", mode);
    // Refresh the editors after updating the mode
    editor.refresh();
}

// Event listener for changes in select element
document.getElementById("quest_language").addEventListener("change", function () {
    var selectedLanguage = this.value;
    updateModes(selectedLanguage);
});

// Initialize modes based on the initial selected language
var initialSelectedLanguage = document.getElementById("quest_language").value;
updateModes(initialSelectedLanguage);