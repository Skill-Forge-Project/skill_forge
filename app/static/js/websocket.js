// Establish a WebSocket connection

document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect("http://" + document.domain + ":" + location.port);

    // Handle the connection event
    socket.on('connect', function() {
        console.log('WebSocket connected');
        // Notify the server that the user is online
        socket.emit('status_update_request', {status: 'Online'});
    });

    // Handle the status update event
    socket.on('status_update', function(data) {
        console.log('Status update:', data);
        updateOnlineStatus(data.status);
    });

    // Handle disconnect
    socket.on('disconnect', function() {
        console.log('WebSocket disconnected');
        // Notify the server that the user is offline
        socket.emit('status_update_request', {status: 'Offline'});
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