window.addEventListener("beforeunload", function(event) {
    // Send an AJAX request to update logout status when browser/tab is closed
    console.log("Sending logout-on-close request");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/logout-on-close", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({}));
});