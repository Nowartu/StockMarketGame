import json

from channels.generic.websocket import AsyncWebsocketConsumer

class AsyncStockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #self.user = self.scope['user']
        self.groups_subscribed = set()

        await self.accept()

    async def disconnect(self, code):
        for group in self.groups_subscribed:
            await self.channel_layer.group_discard(group, self.channel_name)


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        action = data.get("action")
        companies = data.get("companies", [])

        if action == "subscribe":
            for company_key in companies:
                group_name = f"stock_{company_key.upper()}"
                await self.channel_layer.group_add(group_name, self.channel_name)
                self.groups_subscribed.add(group_name)
                print(f"subscrbed to {group_name}")

        elif action == "unsubscribe":
            for company_key in companies:
                group_name = f"stock_{company_key.upper()}"
                await self.channel_layer.group_discard(group_name, self.channel_name)
                self.groups_subscribed.discard(group_name)


    async def stock_update(self, event):
        print("Received")
        await self.send(text_data=json.dumps(event))


class AsyncOrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f'user_{self.user}'

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def order_update(self, event):
        pass