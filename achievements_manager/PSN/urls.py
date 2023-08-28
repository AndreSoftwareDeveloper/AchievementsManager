from django.urls import path
from . import views

urlpatterns = [
    path('platforms/', views.platforms, name='platforms'),
    path('platforms/PSN', views.PSN, name='PSN'),
]
