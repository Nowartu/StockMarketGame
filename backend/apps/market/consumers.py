import json

from channels.generic.websocket import AsyncWebsocketConsumer

class AsyncChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.connected_users = []
        self.users_config = {}

    async def connect(self):
        print(self.scope)
        #self.connected_users.append(self.scope['user'])
        await self.accept()

    async def disconnect(self, code):
        self.connected_users.remove(self.scope['user'])