document.addEventListener('DOMContentLoaded', (event) => {
    const userId = "{{ current_user.user_id }}";  // Get the user ID dynamically
    const socket = io('http://192.168.0.169:5000/', {
        query: {
            user_id: userId
        }
    });

    socket.on('connect', () => {
        updateOnlineStatus('Online')
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        updateOnlineStatus('Offline')
        console.log('Disconnected from server');
    });

    socket.on('status_update', (data) => {
        console.log('Status update:', data);
        updateOnlineStatus(data.status);
    });

    function updateOnlineStatus(status) {
        console.log('Updating online status:', status);
        const onlineStatusDiv = document.getElementById('onlineStatusDiv');
        if (onlineStatusDiv) {
            onlineStatusDiv.innerHTML = `<p class="online_status title">${status}</p>`;
            console.log('Online status updated successfully.');
        } else {
            console.error('OnlineStatusDiv not found.');
        }
    }
});