// Establish a WebSocket connection
var socket = io.connect('http://192.168.0.169:5000/');

// Handle the connection event
socket.on('connect', function() {
    console.log('WebSocket connected');
});

// Handle the status update event
socket.on('status_update', function(data) {
    console.log('Status update:', data);
});