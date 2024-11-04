# classifier/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.classify_image, name='home'),
    path('history/', views.classification_history, name='classification_history'),
]
