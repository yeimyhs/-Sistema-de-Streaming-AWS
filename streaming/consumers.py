from cryptography.fernet import Fernet

FERNET_KEY = b'tVYtU0pLx49t4Zcq95R6BKH9p__q_v3Zyg3tn61AgJY='  # Usa Fernet.generate_key() para generar una y guárdala segura

fernet = Fernet(FERNET_KEY)

def encrypt_channel_name(channel_name):
    return fernet.encrypt(channel_name.encode()).decode()

def decrypt_channel_token(token):
    return fernet.decrypt(token.encode()).decode()

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            token = self.scope['url_route']['kwargs']['token']
            self.room_name = decrypt_channel_token(token)
            self.room_group_name = f'comments_{self.room_name}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))



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

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Comentario
from django.utils import timezone
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.db import database_sync_to_async

User = get_user_model()

class ComentarioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.idstreaming = self.scope["url_route"]["kwargs"]["idstreaming"]
        self.group_name = f"streaming_{self.idstreaming}"
        self.stream_groups = set()  # ✅ Esta línea es obligatoria
        self.stream_groups.add(self.group_name)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "stream_groups"):
            for group_name in self.stream_groups:
                await self.channel_layer.group_discard(group_name, self.channel_name)


    async def receive(self, text_data):
        data = json.loads(text_data)

        comentario = data.get("comentario")
        idusuario = data.get("idusuario")
        idstreaming = data.get("idstreaming")

        if not (comentario and idusuario and idstreaming):
            return  # datos incompletos, ignorar

        # Crear grupo según el streaming
        group_name = f"streaming_{idstreaming}"

        # Unirse si aún no está en ese grupo
        if group_name not in self.stream_groups:
            await self.channel_layer.group_add(group_name, self.channel_name)
            self.stream_groups.add(group_name)

        # Guardar el comentario en la base de datos
        usuario = await self.get_usuario(idusuario)
        if usuario is None:
            return  # Usuario inválido

        comentario_obj = await self.save_comentario(comentario, usuario, idstreaming)

        # Enviar el mensaje al grupo
        await self.channel_layer.group_send(
            group_name,
            {
                'type': 'chat_message',
                'comentario': comentario_obj.comentario,
                'usuario': f"{usuario.nombres} {usuario.apellidos}",
                'fecha': comentario_obj.fechacreacion.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'comentario': event['comentario'],
            'usuario': event['usuario'],
            'fecha': event['fecha'],
        }))

    @database_sync_to_async
    def get_usuario(self, idusuario):
        try:
            return User.objects.get(pk=idusuario)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def save_comentario(self, texto, usuario, idstreaming):
        return Comentario.objects.create(
            comentario=texto,
            idusuario=usuario,
            estado=1,
            idstreaming_id=idstreaming,
            fechacreacion=timezone.now()
        )
