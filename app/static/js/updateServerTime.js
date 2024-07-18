function updateServerTime() {
    var serverTimeElement = document.getElementById('server-time');
    setInterval(function() {
        var currentDate = new Date();
        
        var day = String(currentDate.getDate()).padStart(2, '0');
        var month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        var year = currentDate.getFullYear();
        
        var hours = String(currentDate.getHours()).padStart(2, '0');
        var minutes = String(currentDate.getMinutes()).padStart(2, '0');
        var seconds = String(currentDate.getSeconds()).padStart(2, '0');
        
        var formattedDate = `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
        
        serverTimeElement.textContent = formattedDate;
    }, 1000); // Update every second
}

// Call the updateServerTime function when the page loads
window.onload = updateServerTime;