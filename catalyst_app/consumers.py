# yourapp/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs'].get('task_id', None)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    # This method will be called when progress data is received
    async def receive(self, text_data):
        data = json.loads(text_data)
        progress = data['progress']

        # Send the progress to the WebSocket client
        await self.send(text_data=json.dumps({
            'progress': progress
        }))

    # This is the method that can be called by Celery or elsewhere to send updates
    async def send_progress_update(self, event):
        progress = event['progress']

        # Send message to WebSocket client
        await self.send(text_data=json.dumps({
            'progress': progress
        }))


class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'progress_group'
        
        # Add this connection to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Remove this connection from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_progress_update(self, event):
        progress = event['progress']

        # Send progress to WebSocket client
        await self.send(text_data=json.dumps({
            'progress': progress
        }))
