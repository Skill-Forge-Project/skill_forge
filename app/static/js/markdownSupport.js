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



// Get the textarea element
var textareaTwo = document.getElementById("markdown-content");
// Get the div element for HTML output
var htmlOutputTwo = document.getElementById("html-content-output");

// Initialize Showdown converter
var converterTwo = new showdown.Converter();

// Convert Markdown text to HTML and display in the HTML output div
function updateHtmlOutputTwo() {
    var markdownTextTwo = textareaTwo.value;
    var htmlTextTwo = converter.makeHtml(markdownTextTwo);
    htmlOutputTwo.innerHTML = htmlTextTwo;
}

// Update HTML output when the textarea content changes
textareaTwo.addEventListener("input", updateHtmlOutputTwo);

// Initial update
updateHtmlOutputTwo();