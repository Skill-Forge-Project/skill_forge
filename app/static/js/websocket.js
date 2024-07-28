document.addEventListener('DOMContentLoaded', () => {
    const statusUpdateInterval = 5000; // 5 seconds
    const onlineUsersUpdateInterval = 5000; // 5 seconds

    // Function to send status updates to the server
    function sendStatusUpdate(status) {
        fetch('/update_user_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Include CSRF token if you are using CSRF protection
            },
            body: JSON.stringify({status: status})
        }).catch(error => console.error('Error updating status:', error));
    }

    // Detect page visibility changes and send status update
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            sendStatusUpdate('Offline');
        } else {
            sendStatusUpdate('Online');
        }
    });

    // Set initial status to Online on page load
    sendStatusUpdate('Online');

    // Poll for online users count periodically
    function updateOnlineUsers() {
        fetch('/get_online_users')
            .then(response => response.json())
            .then(data => {
                const onlineUsersDiv = document.getElementById('onlineUsersNumber');
                if (onlineUsersDiv) {
                    onlineUsersDiv.innerHTML = `Online users: ${data.online_users}`;
                }
            })
            .catch(error => console.error('Error fetching online users:', error));
    }

    // Initial call to update the count
    updateOnlineUsers();

    // Update the count periodically
    setInterval(updateOnlineUsers, onlineUsersUpdateInterval);
});

// Function to get CSRF token
function getCsrfToken() {
    // Adjust according to how you are storing the CSRF token in your app
    const tokenElement = document.querySelector('meta[name="csrf-token"]');
    return tokenElement ? tokenElement.getAttribute('content') : '';
}