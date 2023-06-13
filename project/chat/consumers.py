import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Room, ChatUser


# Реализация consumer'а для взаимодействия с websocket'ами
class ChatConsumer(WebsocketConsumer):
    # метод получения последних 30 сообщений чата при входе в него
    def print_last_messages(self, data):
        messages = Message.last_30_messages(self.scope["url_route"]["kwargs"]["room_name"])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    # метод записи нового сообщения в базу данных
    def new_message(self, data):
        author = data['from']
        author_user = ChatUser.objects.filter(user__username=author)[0]
        room = Room.objects.get(name=self.scope["url_route"]["kwargs"]["room_name"])
        message = Message.objects.create(author=author_user,
                                         text=data['message'],
                                         room=room)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    # метод перевода 30 последних сообщений чата в json-формат
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    # метод перевода одного сообщения чата в json-формат
    def message_to_json(self, message):
        return {
            'author': message.author.user.username,
            'text': message.text,
            'add_date': str(message.add_date),
            'room': str(message.room)
        }

    # словарь команд, передаваемых при входе в чат или при передаче сообщения в чате
    commands = {
        'print_last_messages': print_last_messages,
        'new_message': new_message
    }

    # метод подключения к чату
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    # метод отключения от чата
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # метод получения сообщения из чата
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    # метод отправки сообщения в чат после написания сообщения
    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # метод отправки сообщения в чат из базы
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
