const roomName = JSON.parse($('#room-name').text());

const socket = new ReconnectingWebSocket(
    'ws://'
    +window.location.host
    +'/ws/chat/'
    +roomName
    +'/'
);
socket.onclose = function(e){
    console.log("Socket closed unexpectedly");
}
document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};
document.querySelector('#chat-message-submit').onclick = function(e) {
    const message = document.querySelector('#chat-message-input').value;
    socket.send(JSON.stringify({
        'message': message
    }));
    document.querySelector('#chat-message-input').value = '';
};
socket.onmessage = function(e){
    const msg = JSON.parse(e.data);
    const message = msg['message'];
    let el = document.createElement('div');
    el.innerHTML = message;
    document.querySelector('#chat-log').appendChild(el);
}