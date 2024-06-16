import os
import json
from django.conf import settings

from models.entitiesModel import Entities

from django.shortcuts import render,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NewSerilizer

from .models import New

# info demo 
from .data_demo.main import read_and_print_json

def index(request):
    return HttpResponse("Manager-server-TrueShiel")

@api_view(['GET'])
def get_news_rss(request):
    # Obtener el parámetro de la cantidad de noticias a devolver
    news_count = request.query_params.get('count', None)
    
    # Obtener todas las noticias si no se proporciona un valor para 'count'
    if news_count is None:
        rss_news = New.objects.all()
    else:
        # Obtener el número específico de noticias si se proporciona un valor para 'count'
        try:
            count = int(news_count)
            rss_news = New.objects.all()[:count]
        except ValueError:
            # En caso de que 'count' no sea un número válido, devolver un error
            return Response({'error': 'Invalid value for count parameter'}, status=400)

    # Serializar las noticias para devolver la respuesta
    serializer = NewSerilizer(rss_news, many=True)
    return Response({"news_rss": serializer.data})

@api_view(['POST'])
def valid_new(request):
    # obtener el prompt a validar desde el cuerpo de la solicitud
    prompt = request.data.get('prompt', None)
    print(prompt)
    characterisrics = Entities(prompt)
    print(characterisrics.generations[0].text)
    
    if prompt is None:
        return Response({'error': 'No se proporcionó un prompt'}, status=400)

    archivos = ['X.json', 'Reddit.json', 'Rss.json']
    combined_data = []

    for archivo in archivos:
        # Ruta al archivo JSON
        json_file_path = os.path.join(settings.BASE_DIR, 'main', 'data_demo', archivo)
        
        # Leer el archivo JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            combined_data.append(data)
    
    # Retornar el contenido combinado de los JSON en la respuesta
    return Response({"prompt": prompt, "news_reference": combined_data})





