from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import json
from chat.models import Chat, Group


class SynchronousConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket connected...", event)

        # Extract group name from URL route
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        # Add the current channel to the group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        print("Message received from client:", event['text'])
        try:
            data = json.loads(event['text'])

            # ORM operation (sync-safe)
            group, created = Group.objects.get_or_create(name=self.group_name)

            chat = Chat(
                content=data['message'],
                group=group,
            )
            chat.save()

            # Send the message to the group
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chat.message",
                    "text": data['message'],
                }
            )
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        except Exception as e:
            print("Error processing message:", e)

    def chat_message(self, event):
        print("Received message from group:", event['text'])

        # Send the message to the WebSocket client
        self.send({
            "type": "websocket.send",
            "text": json.dumps({"message": event['text']}),
        })

    def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)

        # Remove the channel from the group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

        # Stop the consumer
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

        # Use async-safe methods for ORM operations
        group = await self.get_group()
        await self.create_chat(data['message'], group)

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

    # Wrap synchronous ORM methods with @database_sync_to_async
    @database_sync_to_async
    def get_group(self):
        return Group.objects.get(name=self.group_name)

    @database_sync_to_async
    def create_chat(self, content, group):
        return Chat.objects.create(content=content, group=group)
