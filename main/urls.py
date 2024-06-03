from django.urls import path
from . import views

app_name="main"

urlpatterns = [
    path('', views.index),
    path('get_news/', views.get_news_rss, name="get-news"),
]
