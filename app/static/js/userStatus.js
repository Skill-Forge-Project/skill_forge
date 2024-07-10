import io from 'socket.io-client';

document.addEventListener('DOMContentLoaded', () => {
    const socketIp = process.env.SOCKET_IP || '0.0.0.0';
    const socketPort = process.env.SOCKET_PORT || '8000';
    const userId = "{{ user.user_id }}";  // Get the user ID dynamically
    const socket = io(`https://${socketIp}:${socketPort}/`, {
        query: { user_id: userId }
    });

    socket.on('connect', () => {
        console.log('Connected to server');
        requestUserStatus();
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        updateOnlineStatus('Offline');
    });

    socket.on('status_update', (data) => {
        if (data.user_id === userId) {
            updateOnlineStatus(data.status);
        }
    });

    socket.on('current_user_status', (data) => {
        updateOnlineStatus(data.status);
    });

    function requestUserStatus() {
        socket.emit('request_user_status', { user_id: userId });
    }

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
});