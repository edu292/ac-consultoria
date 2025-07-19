from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'main'
urlpatterns = [
    path('powerbi', views.powerbi, name='powerbi'),
    path('mapacalor', views.mapacalor, name='mapa_calor'),
    path('login', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('', views.index, name='index')
]