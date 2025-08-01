from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('furtos/', views.furto_equipamento_list),
    path('furtos/latest-period', views.fetch_latest_period),
    path('furtos/<int:pk>', views.update_furto_equipamento)
]