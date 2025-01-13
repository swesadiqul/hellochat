from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio


class SynchronousConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket connected...", event)
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        print(f"{event['text']}" + " " + "received from client.")
        for x in range(50):
            self.send({
                "type": "websocket.send",
                "text": str(x),
            })
            sleep(1)
        
    def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        raise StopConsumer()


class AsynchronousConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Async Websocket connected...", event)
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print(f"{event['text']}" + " " + "received from client.")
        for x in range(50):
           await self.send({
                "type": "websocket.send",
                "text": str(x),
            })
           await asyncio.sleep(1)

    async def websocket_disconnect(self, event):
        print("Async Websocket disconnected...")
        raise StopConsumer()