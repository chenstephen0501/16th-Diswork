import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import PrivateMessage, PrivateChatRoom
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = 'chat_%s' % self.room_name
        print("connect")
        print(self.room_group_name )
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        @sync_to_async
        def get_room_name(room_name):
            PrivateChatRoom.objects.get_or_create(room_name = room_name, defaults = {"room_name": room_name})

        await get_room_name(self.room_name)

        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # pass

    @database_sync_to_async
    def get_private_room_id(self):
        return (PrivateChatRoom.objects.get(room_name = self.scope["url_route"]["kwargs"]["room_name"])).id

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.private_room_id = await self.get_private_room_id()

        print(message)
        print("receiver")

        @database_sync_to_async
        def create_message(self, data):
            PrivateMessage.objects.create(
                sender_id = data["senderId"],
                receiver_id = data["receiverId"],
                content = data["message"],
                private_room_id = self.private_room_id,
            )
        
        async def send_message_to_room(self, data):
            await self.channel_layer.group_send(
                    self.room_group_name,
                {
                    "type": "chat_message",
                    "sender_id" : data["senderId"],
                    "receiver_id" : data["receiverId"],
                    "content" : data["message"],
                    "private_room_id" : self.private_room_id,
                }
            )

        await create_message(self, text_data_json)
        await send_message_to_room(self, text_data_json)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({**event}))