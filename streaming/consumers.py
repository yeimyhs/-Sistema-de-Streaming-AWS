import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "¡Conectado al servidor WebSocket!"}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        await self.send(text_data=json.dumps({"message": f"Servidor responde: {message}"}))

    async def disconnect(self, close_code):
        print("WebSocket desconectado", close_code)





import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatgrupalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sala = self.scope["url_route"]["kwargs"]["sala"]
        self.grupo = f"chat_{self.sala}"

        # Unir al grupo de WebSockets
        await self.channel_layer.group_add(self.grupo, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo WebSocket
        await self.channel_layer.group_discard(self.grupo, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]

        # Enviar mensaje al grupo
        await self.channel_layer.group_send(
            self.grupo,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):
        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))
