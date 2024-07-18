from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('user/', views.profile, name='logout'),
    path('register/',views.register, name='register'),
    path('history/',views.history_validations, name='history_valid'),
    path('validation/<int:id_validation>/',views.Validation_detail, name='valid_detail'),
]