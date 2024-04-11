// Get the textarea element
var textarea = document.getElementById("markdown-textarea");
// Get the div element for HTML output
var htmlOutput = document.getElementById("html-output");

// Initialize Showdown converter
var converter = new showdown.Converter();

// Convert Markdown text to HTML and display in the HTML output div
function updateHtmlOutput() {
    var markdownText = textarea.value;
    var htmlText = converter.makeHtml(markdownText);
    htmlOutput.innerHTML = htmlText;
}

// Update HTML output when the textarea content changes
textarea.addEventListener("input", updateHtmlOutput);

// Initial update
updateHtmlOutput();