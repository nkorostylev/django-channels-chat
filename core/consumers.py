
# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user_id = self.scope["session"]["_auth_user_id"]
        self.all_users = 'all'
        self.group_name = "{}".format(user_id)
        # Join room group
        await self.channel_layer.group_add(
            self.all_users,
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        notification = {
            'type': 'user_status',
            'message': 'active'
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(self.all_users, notification)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.all_users,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        notification = {
            'type': 'user_status',
            'message': 'inactive',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(self.all_users, notification)

    async def receive_group_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'receive_group_message',
            'message_id': event['message']
        }))

    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'status': event['message'],
            'user_id': self.group_name
        }))

