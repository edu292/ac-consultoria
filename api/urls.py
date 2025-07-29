from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('furtos/', views.geoloc_list_view, name='lista_furtos'),
    path('furtos/latest-month', views.latest_month, name='latest_month')
]