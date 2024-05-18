import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import PrivateMessage, PrivateChatRoom
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        
        # redis 創建聊天室
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        @sync_to_async
        def is_check_room_name(room_name):
            PrivateChatRoom.objects.get_or_create(room_name = room_name, defaults = {"room_name": room_name})

        await is_check_room_name(self.room_name)

        await self.accept()

    async def disconnect(self, close_code):

        # 離開離天室
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def get_room_id(self):
        return (PrivateChatRoom.objects.get(room_name = self.scope["url_route"]["kwargs"]["room_name"])).id

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.room_id = await self.get_room_id()

        @database_sync_to_async
        def create_message(self, data):
            PrivateMessage.objects.create(
                sender_id = data["senderId"],
                receiver_id = data["receiverId"],
                content = data["message"],
                room_id = self.room_id,
            )
        
        await create_message(self, text_data_json)

        # 將訊息存入 redis 
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))