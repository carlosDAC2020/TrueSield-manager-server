from django.db import models
from django.contrib.auth.models import User


# modelos para el manejo periodico de las RSS
class Media(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    country = models.CharField(max_length=50)
    web =  models.URLField(max_length=200, blank=True)
    logo = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Rss_url(models.Model):
    CATEGORY_CHOICES = [
        ('politica', 'política'),
        ('deporte', 'deporte'),
        ('tecnologia', 'tecnologia'),
        ('economia', 'economia'),
        ('entretenimiento', 'entretenimiento'),
        ('espectaculos', 'espectaculos'),
        ('salud', 'salud'),
        ('ciencia', 'ciencia'),
        ('mundo', 'mundo'),
        ('cultura', 'cultura'),
        ('opinion', 'opinion'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    rss = models.URLField()
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.rss}"

class New(models.Model):
    """
    ## item RSS
    noticias obtenidas por medios RSS
    """
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    publication_date = models.DateTimeField()
    link_article = models.URLField()
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Validation(models.Model):
    """
    ## valicaciones 
    este modelo maneja el registro de las validaciones de noticias echas por los usuarios
    """
    prompt = models.TextField()
    characterisrics=models.JSONField(default=list)
    veracity = models.FloatField()
    inferences = models.JSONField(default=dict)
    cantitems = models.JSONField(default=dict)
    list_items = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)  
    last_viewed_at = models.DateTimeField(auto_now=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validations')

    def __str__(self):
        return self.prompt