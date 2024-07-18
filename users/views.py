
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerilizer, ValidationHistorySerializer, ValidationSerilizer

from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#modelos 
from django.contrib.auth.models import User
from main.models import Validation


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error":"invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerilizer(instance=user)
    print("logeado el ususrio",request.data['username'])
    return Response({"token":token.key}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    print("imprecion de los datos ")
    print(request.data)
    serializer = UserSerilizer(data=request.data)


    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        print("usuario creado")
        return Response({'token':token.key}, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    user_serializer = UserSerilizer(instance=user)
    print("datos serializados")
    return Response({"user": user_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def history_validations(request):
    # Obtener todas las validaciones del usuario autenticado, ordenadas por `last_viewed_at`
    validations = Validation.objects.filter(user=request.user).order_by('-last_viewed_at')
    
    # Serializar las validaciones con el serializador específico para el historial
    serializer = ValidationHistorySerializer(validations, many=True)
    
    # Devolver la respuesta con las validaciones serializadas
    return Response({"validations": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Validation_detail(request, id_validation):
    validation =  get_object_or_404(Validation, id=id_validation)
    serializer = ValidationSerilizer(instance=validation)
    return Response({"validation": serializer.data}, status=status.HTTP_200_OK)

