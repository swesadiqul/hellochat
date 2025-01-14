from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync


class SynchronousConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket connected...", event)
        print("Channel Layer:", self.channel_layer)
        print("Channel Name:", self.channel_name)
        print(self.scope['url_route']['kwargs']['group_name'])
        async_to_sync(self.channel_layer.group_add)("Programmer", self.channel_name)
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        print("Message received from client:", event['text'])
        data = json.loads(event['text'])
        async_to_sync(self.channel_layer.group_send)("Programmer", {
            "type": "chat.message",
            "text": data['message'],
        })
        
    def chat_message(self, event):
        print("Received message from group:", event['text'])
        self.send({
            "type": "websocket.send",
            "text": json.dumps({"message": event['text']}),
        })
        
    def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        print("Channel Layer:", self.channel_layer)
        print("Channel Name:", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)("Programmer", self.channel_name)
        raise StopConsumer()


class AsynchronousConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print("Group Name... ", self.group_name)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("Async Websocket connected...", event)

        await self.send({
            "type": "websocket.accept",
        })
        
    async def websocket_receive(self, event):
        print("Message received from client:", event['text'])
        data = json.loads(event['text'])
        await self.channel_layer.group_send(self.group_name, {
            "type": "chat.message",
            "text": data['message'],
        })

    async def chat_message(self, event):
        print("Received message from group:", event['text'])
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({"message": event['text']}),
        })
    

    async def websocket_disconnect(self, event):
        print("Async Websocket disconnected...")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()