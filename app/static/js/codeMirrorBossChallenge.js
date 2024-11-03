// Function to handle CodeMirror editor custom fields.

// Initialize CodeMirror editors
var bossQuestion = CodeMirror.fromTextArea(document.getElementById("bossQuestion"), {
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
    bossQuestion.setOption("mode", mode);
    bossQuestion.refresh();
}

// Event listener for changes in select element
document.getElementById("boss_language").addEventListener("change", function () {
    var selectedLanguage = this.value;
    updateModes(selectedLanguage);
});

// Initialize modes based on the initial selected language
var initialSelectedLanguage = document.getElementById("boss_language").value;
updateModes(initialSelectedLanguage);