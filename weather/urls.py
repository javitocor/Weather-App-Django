from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('city_forecast/<city_name>', views.detail_city, name='forecast'),
    path('delete/<city_name>', views.delete_city, name='delete_city')
]