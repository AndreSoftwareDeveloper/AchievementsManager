from django.urls import path
from . import views

urlpatterns = [
    path('PSN/', views.PSN, name='PSN'),
]
