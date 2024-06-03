from rest_framework import serializers
from django.contrib.auth.models import User
from .models import New

class NewSerilizer(serializers.ModelSerializer):
    media_url = serializers.URLField(source='media.web', read_only=True)
    type_item ="rss"
    class Meta:
        model = New
        fields = ['id', 'title', 'summary', 'publication_date', 'link_article', 'media_url']
