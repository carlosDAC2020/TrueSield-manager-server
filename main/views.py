from django.shortcuts import render,HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NewSerilizer

from .models import New

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