function getCSRFToken() {
    const csrfTokenElement = document.querySelector('input[name="csrf_token"]');
    if (csrfTokenElement) {
        const csrfToken = csrfTokenElement.value;
        console.log('CSRF Token:', csrfToken);  // Debug statement
        return csrfToken;
    } else {
        console.error('CSRF token not found!');
        return '';
    }
}

function sendHeartbeat() {
    const csrfToken = getCSRFToken();
    if (!csrfToken) {
        console.error('Cannot send heartbeat, CSRF token is missing');
        return;
    }

    fetch('/heartbeat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.text().then(text => { throw new Error(text) });
        }
    }).then(data => {
        console.log('Heartbeat success:', data);
    }).catch(error => {
        console.log('Heartbeat error:', error);
    });
}

window.addEventListener('focus', sendHeartbeat);  // Send heartbeat when the page gains focus
setInterval(sendHeartbeat, 1000);  // Send heartbeat every second