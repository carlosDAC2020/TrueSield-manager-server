from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Validation

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

class ValidationSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        fields = '__all__' 

# Serializador para la vista del historial
class ValidationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Validation
        exclude = ['characterisrics', 'inferences', 'cantitems', 'list_items']