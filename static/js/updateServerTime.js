// Function to update the server time every second
function updateServerTime() {
    var serverTimeElement = document.getElementById('server-time');
    setInterval(function() {
        var currentDate = new Date();
        serverTimeElement.textContent = currentDate.toLocaleString();
    }, 1000); // Update every second
}

// Call the updateServerTime function when the page loads
window.onload = updateServerTime;