from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('furtos/', views.furto_equipamento_list, name='furtos'),
    path('furtos/latest-period', views.fetch_latest_period, name='latest_period'),
    path('furtos/<int:pk>', views.update_furto_equipamento, name='update_furto')
]