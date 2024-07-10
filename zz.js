const WebSocket = require('ws');

const socket = new WebSocket('ws://localhost:8000/ws/chat/');

socket.on('open', function(event) {
    console.log('WebSocket connection established.');
    socket.send('Hello, WebSocket Server!');
});

socket.on('message', function(data) {
    console.log('Received:', data);
});
