// Function to handle CodeMirror editor custom fields.

// Initialize CodeMirror editors
var template = CodeMirror.fromTextArea(document.getElementById("template_input"), {
    lineNumbers: true,
    theme: "dracula",
    indentUnit: 2,
    autoCloseBrackets: true,
    matchBrackets: true,
    scrollbars: true
});

var unit_tests = CodeMirror.fromTextArea(document.getElementById("unit_tests_input"), {
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
    template.setOption("mode", mode);
    unit_tests.setOption("mode", mode);
    // Refresh the editors after updating the mode
    template.refresh();
    unit_tests.refresh();
}

// Event listener for changes in select element
document.getElementById("quest_language_input").addEventListener("change", function () {
    var selectedLanguage = this.value;
    updateModes(selectedLanguage);
});

// Initialize modes based on the initial selected language
var initialSelectedLanguage = document.getElementById("quest_language_input").value;
updateModes(initialSelectedLanguage);