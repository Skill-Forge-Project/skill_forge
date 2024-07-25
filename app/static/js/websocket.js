// Establish a WebSocket connection

document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect("http://" + document.domain + ":" + location.port);

    // Handle the connection event
    socket.on('connect', function() {
        // console.log('WebSocket connected');
        // Notify the server that the user is online
        socket.emit('status_update_request', {status: 'Online'});
        startHeartbeat();
    });

    // Handle the status update event
    socket.on('status_update', function(data) {
        console.log('Status update:', data);
        updateOnlineStatus(data.status);
    });

    // Handle disconnect
    socket.on('disconnect', function() {
        // console.log('WebSocket disconnected');
        // Notify the server that the user is offline
        socket.emit('status_update_request', {status: 'Offline'});
    });

    function startHeartbeat() {
        setInterval(() => {
            socket.emit('status_update_request', {status: 'Online'});
        }, 5000);  // Send a heartbeat every 30 seconds
    }

    // Detect page visibility changes and send status update
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            socket.emit('status_update_request', {status: 'Offline'});
        } else {
            socket.emit('status_update_request', {status: 'Online'});
        }
    });
});




function updateOnlineStatus(status) {
    const onlineStatusDiv = document.getElementById('onlineStatusDiv');
    if (onlineStatusDiv) {
        if (status === 'Online') {
            onlineStatusDiv.innerHTML = `<p class="online_status title online">${status}</p>`;
        } else {
            fetchLastLoggedDate().then(lastLoggedDate => {
                onlineStatusDiv.innerHTML = `<p class="online_status title offline">Last seen</p>
                    <p class="online_status title offline">${lastLoggedDate}</p>`;
            }).catch(() => {
                onlineStatusDiv.innerHTML = `<p class="online_status title offline">${status}</p>`;
            });
        }
    }
}


function fetchLastLoggedDate() {
    return fetch('/get_last_logged_date')
        .then(response => response.json())
        .then(data => data.last_logged_date);
}



// Function to fetch and update the number of online users
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

// Update the count every second
setInterval(updateOnlineUsers, 1000); // 1000 milliseconds = 1 second