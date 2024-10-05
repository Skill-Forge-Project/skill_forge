// Initialize CodeMirror editors for log-viewer
var logViewer = CodeMirror.fromTextArea(document.getElementById("submission"), {
    lineNumbers: true,
    theme: "dracula",
    indentUnit: 2,
    autoCloseBrackets: true,
    matchBrackets: true,
    scrollbars: true,
    readOnly: true,
    mode: 'application/ld+json',
    height: 'auto'
});