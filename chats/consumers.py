import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import PrivateMessage, PrivateChatRoom
from channels.db import database_sync_to_async
from datetime import datetime

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.async_get_or_create_room(self.room_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def async_get_or_create_room(self, room_name):
        PrivateChatRoom.objects.get_or_create(room_name=room_name, defaults={"room_name": room_name})

    @database_sync_to_async
    def async_get_private_room_id(self):
        return PrivateChatRoom.objects.get(room_name=self.room_name).id

    @database_sync_to_async
    def async_create_message(self, data):
        PrivateMessage.objects.create(
            sender_id=data["senderId"],
            receiver_id=data["receiverId"],
            content=data["message"],
            private_room_id=self.private_room_id,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.private_room_id = await self.async_get_private_room_id()

        await self.async_create_message(text_data_json)
        await self.async_send_message_to_room(text_data_json)

    async def async_send_message_to_room(self, data):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender_id": data["senderId"],
                "receiver_id": data["receiverId"],
                "content": data["message"],
                "private_room_id": self.private_room_id,
                "created_at": created_at,
                "sender_img": data["senderImg"],
                "sender_name": data["senderName"],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({**event}))
