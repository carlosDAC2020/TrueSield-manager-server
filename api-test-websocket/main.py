import uvicorn
from fastapi import FastAPI, WebSocket
import asyncio
import websockets
import json
import random
import os
import sys


# Obtén el puerto de los argumentos de la línea de comandos
if len(sys.argv) != 2:
    print("Uso: python main.py <puerto>")
    sys.exit(1)
puerto = int(sys.argv[1])  # Convierte el argumento del puerto a entero

# Configurar FastAPI
app = FastAPI()

def prueba_envio_items():
    archivos = ['X.json', 'Reddit.json', 'Rss.json']
    combined_data = []

    for archivo in archivos:
        # Ruta al archivo JSON
        json_file_path = os.path.join('data_demo', archivo)
        
        # Leer el archivo JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            combined_data.append(data)
    
    list_items=[]
    # Retornar el contenido combinado de los JSON en la respuesta
    for type_item in combined_data:
        for tipo, valor in type_item.items():
            for item in valor:
                if tipo=="tweets":
                    item["Type_item"]="x" 
                elif tipo=="reddit":
                    item["Type_item"]="reddit"
                else:
                    item["Type_item"]="rss"
                list_items.append(item)
    

    random.shuffle(list_items)
    
    return list_items

list_items={}

# Ruta para retornar un saludo
@app.get("/")
async def index():
    return {"message": "¡Hola, bienvenido a nuestra API!"}

@app.websocket("/contrasting")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established")
    try:
        data = await websocket.receive_text()
        message = json.loads(data)
        print("Message received:", message)

        list_items = prueba_envio_items()
        cant_items_send=0
        while cant_items_send<=100:
            item =random.choice(list_items)
            await websocket.send_text(json.dumps(item))
            print("\n mensaje enviado ",cant_items_send)
            cant_items_send+=1
        
        
        # Cerrar la conexión WebSocket después de enviar todos los mensajes
        await websocket.close()
        print("WebSocket connection closed")
        
    except Exception as e:
        print(f"Connection error: {e}")
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=puerto)
