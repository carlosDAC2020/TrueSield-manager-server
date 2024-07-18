from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import json
import websockets
import random
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from .models import Validation
from models.entitiesModel import Entities
from django.shortcuts import get_object_or_404
import time

class ValidateConsumer(AsyncWebsocketConsumer):
    capas = "caracterizacion"
    prompt = ""
    characterisrics=""
    veracidad = 0
    inferences = {
        "assertion": 0,
        "assumption": 0,
        "denial": 0
    }
    cantitems = {
        "rss": 0,
        "reddit": 0,
        "x": 0
    }
    list_items = []
    user=0

    def generate_report(self, item):
        self.veracidad += 3.33
        infr = random.choice(list(self.inferences.keys()))
        self.inferences[infr] += 1
        self.cantitems[item["Type_item"]] += 1
        return {
            "report": {
                "veracity": round(self.veracidad, 2),
                "inference": {
                    "assertion": self.inferences["assertion"],
                    "assumption": self.inferences["assumption"],
                    "denial": self.inferences["denial"]
                }
            },
            "item": item,
            "cant_items": {
                "rss": self.cantitems["rss"],
                "reddit": self.cantitems["reddit"],
                "x": self.cantitems["x"]
            }
        }

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            user_token = Token.objects.get(key=token)
            user = user_token.user
            return User.objects.get(username=user.username)
        except Token.DoesNotExist:
            return None
    
    @database_sync_to_async
    def save_validation(self):
        if self.user:
            new_validation = Validation.objects.create(
                user=self.user,
                prompt=self.prompt,
                veracity=self.veracidad,
                inferences=self.inferences,
                cantitems=self.cantitems,
                list_items=self.list_items,
                characterisrics=self.characterisrics
            )
            new_validation.save()
            print("validacion guardada")

    async def connect(self):
        # Capturar parámetros de la URL
        self.prompt = self.scope['url_route']['kwargs']['param1']

        # Obtener el token del encabezado de la conexión WebSocket
        token = self.scope['query_string'].decode().split('=')[1]
        
        # Obtener el usuario desde el token
        self.user = await self.get_user_from_token(token)
        

        print(self.user)
        print(type(self.user))
        if not self.user:
            await self.close()
            return
        
        await self.accept()

        print(f"Conectado al WebSocket por {self.user}")

        # Iniciar una tarea asíncrona para enviar mensajes constantemente
        self.send_messages_task = asyncio.create_task(self.validate_mew())

    async def disconnect(self, close_code):
        self.cantitems = {
        "rss": 0,
        "reddit": 0,
        "x": 0
        }
        self.list_items = []
        print("Desconectado del WebSocket")
        self.send_messages_task.cancel()

    async def receive(self, text_data):
        message = json.loads(text_data)
        print("Mensaje recibido en Django:", message)

    async def validate_mew(self):
        # Inicia el contador de tiempo
        inicio = time.perf_counter()
        # Fase de caracterización -------------------------------------------------
        if self.capas == "caracterizacion":
            characterisrics = Entities(self.prompt)
            print(characterisrics.generations[0].text)
            
            # Convertir el texto a JSON
            try:
                self.characterisrics = json.loads(characterisrics.generations[0].text)
                # Enviar caracterización al cliente 
                message = {
                    "capa": self.capas,
                    "characterisrics": self.characterisrics
                }
                await self.send(text_data=json.dumps(message))
            except json.JSONDecodeError as e:
                message = {
                    "capa": "terminar",
                    "mensaje": characterisrics.generations[0].text
                }
                await self.send(text_data=json.dumps(message))
                
        # Fase de contrastación y validación en paralelo ------------------------------------
        self.capas = "contrastacion"
        
        # Conexiones con las APIs 
        uris = [
            "ws://127.0.0.1:8001/contrasting",
            "ws://127.0.0.1:8002/contrasting",
            "ws://127.0.0.1:8003/contrasting"
        ]

        """async def connect_and_receive(uri, message):
            try:
                async with websockets.connect(uri) as websocket:
                    await websocket.send(json.dumps(message))
                    while True:
                        item = await websocket.recv()
                        print(f"item enviado desde {uri}")
                        item = json.loads(item)
                        self.list_items.append(item)
                        await self.send(text_data=json.dumps(self.generate_report(item)))
            except websockets.exceptions.ConnectionClosedOK:
                print(f"La conexión a {uri} ha sido cerrada por el servidor.")
            except websockets.exceptions.ConnectionClosedError:
                print(f"Error en la conexión a {uri}. Reintentando...")

        await asyncio.gather(
            *[connect_and_receive(uri, self.prompt) for uri in uris]
        )"""


        # Mantener las conexiones abiertas
        websockets_connections = []
        for uri in uris:
            websocket = await websockets.connect(uri)
            websockets_connections.append(websocket)
            await websocket.send(json.dumps(message))
        
        # Conexión con la API de RSS
        rss_socket = websockets_connections[0]
        reddit_socket = websockets_connections[1]
        x_socket = websockets_connections[2]

        while True:
            try:
                rss_item = await rss_socket.recv()
                reddit_item = await reddit_socket.recv()
                x_item = await x_socket.recv()
                #quiro que cada mensaje se procese comoun item a continuacion 
                rss_item = json.loads(rss_item)
                reddit_item = json.loads(reddit_item)
                x_item = json.loads(x_item)
                # Guardar los ítems de referencia
                self.list_items.append(rss_item)
                self.list_items.append(reddit_item)
                self.list_items.append(x_item)
                # envio de items
                await self.send(text_data=json.dumps(self.generate_report(rss_item)))
                await self.send(text_data=json.dumps(self.generate_report(reddit_item)))
                await self.send(text_data=json.dumps(self.generate_report(x_item)))
                
            except websockets.exceptions.ConnectionClosedOK:
                print("La conexión ha sido cerrada por el servidor.")
                break
            except websockets.exceptions.ConnectionClosedError:
                print("Error en la conexión. Reintentando...")
                break

        # Terminar conexiones con las APIs de ítems
        for websocket in websockets_connections:
            await websocket.close()
        
        
        # Guardar la validación en la base de datos
        await self.save_validation()

        # terminar coneccion 
        message = {
            "capa": "terminar",
            "mensaje": characterisrics.generations[0].text
        }
        await self.send(text_data=json.dumps(message))
        print("mensaje de cancelacion de coneccion enviado")

        # Detiene el contador de tiempo
        fin = time.perf_counter()
        # Calcula el tiempo transcurrido
        tiempo_transcurrido = fin - inicio
        print(f"El método tomó {tiempo_transcurrido:.4f} segundos en ejecutarse.")
        self.disconnect()
