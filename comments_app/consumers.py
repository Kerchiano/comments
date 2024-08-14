from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'comments_{self.post_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_message',
                'message': message
            }
        )

    async def comment_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
