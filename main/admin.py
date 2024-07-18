from django.contrib import admin
from .models import Media, Rss_url, New, Validation

# Define el formulario en línea para Rss_url en el panel de administración de Media
class Rss_urlInline(admin.TabularInline):
    model = Rss_url
    extra = 1  # Número de formularios en línea adicionales que se mostrarán

# Define la configuración del panel de administración para el modelo Media
class MediaAdmin(admin.ModelAdmin):
    inlines = (Rss_urlInline,)  # Agrega el formulario en línea de Rss_url al modelo Media

# Define la configuración del panel de administración para el modelo Rss_url
class Rss_urlAdmin(admin.ModelAdmin):
    list_display = ('category', 'rss', 'media')
    list_filter = ('category',)  # Agrega un filtro de búsqueda por categoría

# Registra los modelos en el admin
admin.site.register(Media, MediaAdmin)  
admin.site.register(Rss_url, Rss_urlAdmin)  
admin.site.register(New)  
admin.site.register(Validation)  
