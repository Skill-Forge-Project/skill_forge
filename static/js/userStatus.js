document.addEventListener('DOMContentLoaded', (event) => {
    const userId = "{{ current_user.user_id }}";  // Get the user ID dynamically
    const socket = io('http://192.168.0.169:5000/', {
        query: {
            user_id: userId
        }
    });

    socket.on('connect', () => {
        updateOnlineStatus('Online')
    });

    socket.on('disconnect', () => {
        updateOnlineStatus('Offline')
    });

    socket.on('status_update', (data) => {
        updateOnlineStatus(data.status);
    });
    function updateOnlineStatus(status) {
        const onlineStatusDiv = document.getElementById('onlineStatusDiv');
        if (onlineStatusDiv) {
            if (status === 'Online') {
                onlineStatusDiv.innerHTML = `<p class="online_status title">${status}</p>`;
            } else {
                // Make AJAX request to fetch last logged date
                fetch('/get_last_logged_date')
                    .then(response => response.json())
                    .then(data => {
                        const lastLoggedDate = data.last_logged_date;
                        onlineStatusDiv.innerHTML = `<p class="online_status title">${status}</p>
                            <p class="online_status title">Last seen: ${lastLoggedDate}</p>`;
                    })
                    .catch(error => {
                        onlineStatusDiv.innerHTML = `<p class="offline_status title">${status}</p>`;
                    });
            }
        } else {
            return;
        }
    }
});