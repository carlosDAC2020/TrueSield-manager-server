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
from config.settings import APIS_ITEMS, API_MODELS

import time

# obtencion de items por http
import aiohttp


class ValidateConsumer(AsyncWebsocketConsumer):
    capas = "caracterizacion"
    prompt = ""
    characterisrics=""
    veracidad = 0
    inferences = {
        "affirmation": 0,
        "assumption": 0,
        "denial": 0
    }
    cantitems = {
        "Rss": 0,
        "Reddit": 0,
        "X": 0
    }
    list_items = []
    user=0

    pesos = {
        'Rss': {'w_C': 0.4, 'w_F': 0.4, 'w_I': 0.2},
        'X': {'w_C': 0.3, 'w_F': 0.3, 'w_I': 0.4},
        'Reddit': {'w_C': 0.35, 'w_F': 0.35, 'w_I': 0.3}
    }

    def item_rating(self, item):

        w_C = self.pesos[item["Type_item"]]['w_C']
        w_F = self.pesos[item["Type_item"]]['w_F']
        w_I = self.pesos[item["Type_item"]]['w_I']
        
        contexto_normalizado = item["ContextLevel"] 
        confianza_normalizada = item["TrueLevel"] 
        if item["Inference"] == "affirmation":
            inferencia = 1
        elif item["Inference"] == "assumption":
            inferencia = 0.5
        else:
            inferencia = 0
        item["rating"] = (w_C * contexto_normalizado) + (w_F * confianza_normalizada) + (w_I * inferencia)
        
        return item

    def veracity(self):
        # Contadores para los ítems por tipo
        conteo_tipo = {tipo: 0 for tipo in list(self.pesos.keys())}

        puntuacion_total = 0

        for item in self.list_items:
            puntuacion_total += item["rating"]
            conteo_tipo[item["Type_item"]] += 1
          
        # Calcular la puntuación máxima y mínima posible
        puntuacion_maxima = 0
        puntuacion_minima = 0
        for tipo, pesos in self.pesos.items():
            puntuacion_maxima+= ((pesos["w_C"]*1) + (pesos["w_F"]*1) + (pesos["w_I"]*1)) * conteo_tipo[tipo] 
            puntuacion_minima+= ((pesos["w_C"]*0) + (pesos["w_F"]*0) + (pesos["w_I"]*-1)) * conteo_tipo[tipo] 
            
        
        # Normalización de la veracidad
        veracidad = ((puntuacion_total - puntuacion_minima) / (puntuacion_maxima - puntuacion_minima)) * 100
        self.veracidad = round(veracidad, 2)

    def generate_report(self, item):
        
        self.inferences[item["Inference"]] += 1
        self.cantitems[item["Type_item"]] += 1
        print("generacion de reporte ")
        self.veracity()
        return {
            "report": {
                "veracity": self.veracidad,
                "inference": {
                    "affirmation": self.inferences["affirmation"],
                    "assumption": self.inferences["assumption"],
                    "denial": self.inferences["denial"]
                }
            },
            "item": item,
            "cant_items": {
                "rss": self.cantitems["Rss"],
                "reddit": self.cantitems["Reddit"],
                "x": self.cantitems["X"]
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
                veracity=round(self.veracidad, 2),
                inferences=self.inferences,
                cantitems=self.cantitems,
                list_items=self.list_items,
                characterisrics=self.characterisrics
            )
            new_validation.save()
            print("validacion guardada")

    async def get_items(self, keywords):

        # edios de informacion a buscar 
        uris = APIS_ITEMS
    
        # resultrados de contrastacion 
        results = {
            "Rss" : [],
            "X" : [],
            "Reddit" : []
        }
        async with aiohttp.ClientSession() as session:
            print("conectando ...")
            for medio, url in uris.items():
                print(url)
                async with session.post(f"{url}/contrasting_{medio}", json=keywords) as response:
                    print("realizando peticion")
                    if response.status == 200:
                        data = await response.json()
                        print(data)
                        print("guardando resultados ")
                        results[medio] = data
                        results[medio] = results[medio][medio]
                        print(results[medio])
                        print("guardado")
                    else:
                        print(f"Failed to get data from {url}: {response.status}")
        
        # guardamnos ,os resultados 
        items=[]
        for media, result in results.items():
            print("media: ",media)
            for item in result:
                print(item)
                items.append(item)
        
        print(len(items))
        return items
    
    async def get_keywords(self, text):
        print("palabras clave enviada ")
        url = f"{API_MODELS}/classify"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=text) as response:
                print("palabras clave recividad ")
                if response.status == 200:
                    data = await response.json()
                    print(data)
                else:
                    print(f"Failed to get data from {url}: {response.status}")
        return data 
    
    async def connect(self):
         # Aceptar la conexión
        await self.accept()
        
        # Enviar un mensaje de texto en formato JSON
        message = {"message": "ok"}
        await self.send(text_data=json.dumps(message))
        
        print("Conexión aceptada")

    async def disconnect(self, close_code):
        self.cantitems = {
        "rss": 0,
        "reddit": 0,
        "x": 0
        }
        self.list_items = []
        print("Desconectado del WebSocket")
        print("terminado")
        self.send_messages_task.cancel()

    async def receive(self, text_data):
        message = json.loads(text_data)

        if message.get('prompt') and message.get('token'):
            prompt = message.get('prompt')
            token = message.get('token')

            # Obtener el usuario desde el token
            self.user = await self.get_user_from_token(token)
            if not self.user:
                await self.close()
                
        
            self.prompt = prompt
            print(f"Usuario conectado: {self.user}")
            print(f"Prompt recibido: {self.prompt}")
            # Iniciar una tarea asíncrona para enviar mensajes constantemente
            self.send_messages_task = asyncio.create_task(self.validate_mew())
        else:
            message = json.loads(text_data)
            print("Mensaje recibido en Django:", message)

    async def validate_mew(self):
        # Inicia el contador de tiempo
        inicio = time.perf_counter()
        # Fase de caracterización -------------------------------------------------
        if self.capas == "caracterizacion":
            
            text = {
                "prompt": self.prompt,
            }

            characterisrics = await self.get_keywords(text)
            
            # Convertir el texto a JSON
            self.characterisrics = characterisrics
            # Enviar caracterización al cliente 
            message = {
                "capa": self.capas,
                "characterisrics": self.characterisrics
            }
            await self.send(text_data=json.dumps(message))
            print("caracterizacion enviada  ")
            
                
        # Fase de contrastación y validación en paralelo ------------------------------------
        self.capas = "contrastacion"

        stat=False
        # tes con apis de embuste
        if stat:
            # Conexiones con las APIs 
            uris = [
                "ws://127.0.0.1:8001/contrasting",
                "ws://127.0.0.1:8002/contrasting",
                "ws://127.0.0.1:8003/contrasting",
            ]

            # Mantener las conexiones abiertas
            websockets_connections = []
            for uri in uris:
                try:
                    websocket = await websockets.connect(uri)
                    print("conectado")
                    websockets_connections.append(websocket)
                    await websocket.send(json.dumps(message))
                except:
                    print("coneccion no establecida")
            # Conexión con la API de RSS
            rss_socket = websockets_connections[0]
            reddit_socket = websockets_connections[1]
            x_socket = websockets_connections[2]

            print("coneccion con apis aestablecida ")
            while True:
                print("recepcion de items")
                try:
                    # recepcion de items
                    rss_item = await rss_socket.recv()
                    print("rss")
                    reddit_item = await reddit_socket.recv()
                    print("reddit")
                    x_item = await x_socket.recv()
                    print("tweet")
                    
                    # comvercion de los items a json 
                    rss_item = json.loads(rss_item)
                    reddit_item = json.loads(reddit_item)
                    x_item = json.loads(x_item)

                    #asignamos la puntuacion al item en cuestion
                    print("obteniendo puntuacion de item ")
                    rss_item = self.item_rating(rss_item)
                    reddit_item = self.item_rating(reddit_item)
                    x_item = self.item_rating(x_item)

                    # Guardar los ítems de referencia
                    print("guardando item en referencias ")
                    self.list_items.append(rss_item)
                    self.list_items.append(reddit_item)
                    self.list_items.append(x_item)
                    
                    # envio de items al cliente
                    print("enviando reporte al cliente ")
                    await self.send(text_data=json.dumps(self.generate_report(rss_item)))
                    await self.send(text_data=json.dumps(self.generate_report(reddit_item)))
                    await self.send(text_data=json.dumps(self.generate_report(x_item)))
                    
                except websockets.exceptions.ConnectionClosedOK:
                    print("La conexión ha sido cerrada por el servidor.")
                    break
                except websockets.exceptions.ConnectionClosedError:
                    print("Error en la conexión. Reintentando...")
                    break
        # test con apis reales
        else:
            # obtenemos los items de referencia 
            items = await self.get_items(self.characterisrics)

            # realizamos la evaluacion 
            print("realizando evaluacion")
            print(len(items))
            for item in items:
                try:
                    # obtenemos la puntuacion para el item 
                    item = self.item_rating(item)

                    # guardamos el items 
                    self.list_items.append(item)

                    # enviamos el item al cliente
                    print("enviando reporte al cliente ")
                    await self.send(text_data=json.dumps(self.generate_report(item)))

                except websockets.exceptions.ConnectionClosedOK:
                    print("La conexión ha sido cerrada por el servidor.")
                    break
                except websockets.exceptions.ConnectionClosedError:
                    print("Error en la conexión. Reintentando...")
                    break

        # Guardar la validación en la base de datos
        await self.save_validation()

        # terminar coneccion 
        message = {
            "capa": "terminar",
            "mensaje": ""
        }
        await self.send(text_data=json.dumps(message))
        print("mensaje de cancelacion de coneccion enviado")

        # Detiene el contador de tiempo
        fin = time.perf_counter()
        # Calcula el tiempo transcurrido
        tiempo_transcurrido = fin - inicio
        print(f"El método tomó {tiempo_transcurrido:.4f} segundos en ejecutarse.")
        await self.disconnect()
