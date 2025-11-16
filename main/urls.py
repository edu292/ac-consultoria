from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'main'
urlpatterns = [
path('', views.index, name='index'),
    path('powerbi', views.powerbi, name='powerbi'),
    path('mapacalor', views.mapacalor, name='mapa_calor'),
    path('login', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('double-checker', views.double_checker, name='double_checker'),
    path('ocorrencias-bairros-curitiba', views.ocorrencias_bairros_curitiba, name='ocorrencias_bairros_curitiba')
]