from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('geoloc/', views.geoloc_list_view, name='geoloc_list')
]