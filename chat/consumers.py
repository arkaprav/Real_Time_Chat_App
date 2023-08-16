import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Rooms
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = Message.last_10_messages(self.room_group_name)
        content = {
            'command':'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
    
    def send_message(self, data):
        room = Rooms.objects.get(slug = self.room_group_name)
        author = User.objects.get(username = data['from'])
        message = data['message']
        msg = Message.objects.create(author = author, content = message, room = room)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(msg)
        }
        return self.send_group_events(content)
    
    def messages_to_json(self, messages):
        results = []
        for message in messages:
            results.append(self.message_to_json(message))
        return results
    
    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }
    
    # accepts incoming connections of websocket
    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["room_name"]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        
    # disconnects the connection
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    
    commands = {
        'fetch_messages': fetch_messages,
        'send_message': send_message
    }
    # receive messages from socket and route them to groups
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.commands[text_data_json['command']](self, text_data_json)
    
    def send_group_events(self, message):
        # Send event to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
    
    # handles the event coming from group as chat.message type and route it to socket 
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
    
    #sends the message directly through websocket
    def send_message(self, message):
        self.send(text_data=json.dumps({"message": message}))