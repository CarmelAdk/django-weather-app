
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cities', views.cities_list, name='cities_list'),
    path('cities/add/', views.add_city, name='add_city'),
]