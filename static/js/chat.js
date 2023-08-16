const roomName = JSON.parse($('#room-name').text());
var prevMsgUser = '';
const socket = new ReconnectingWebSocket(
    'ws://'
    +window.location.host
    +'/ws/chat/'
    +roomName
    +'/'
);
socket.onopen = function(e){
    socket.send(JSON.stringify({'command': 'fetch_messages'}));
}
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
        'command':'send_message',
        'message': message,
        'from':username
    }));
    document.querySelector('#chat-message-input').value = '';
};
socket.onmessage = function(e){
    let dict = JSON.parse(e.data);
    var command_message = dict['message'];
    if(command_message['command'] == 'messages'){
        let messages = command_message['messages'];
        for(const i in messages){
            CreateMessage(messages[i]);
        }
    }
    else{
        let message = command_message['message'];
        CreateMessage(message);
    }
}
function CreateMessage(message){
    let div = document.createElement('div');
    let h4 = document.createElement('h4');
    let p = document.createElement('p');
    h4.textContent = message['author'];
    p.textContent = message['content'];
    if(message['author'] == username){
        div.appendChild(p);
        div.className = 'send';
        prevMsgUser = message['author'];
    }
    else{
        if(prevMsgUser == message['author']){
            div.appendChild(p);
        }
        else{
            div.appendChild(h4);
            div.appendChild(p);
            prevMsgUser = message['author'];
        }
        div.className= 'reply';
    }
    document.querySelector('#chat-log').appendChild(div);
    console.log(prevMsgUser)
}