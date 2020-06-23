from django.urls import path, include
from medicine_app import views


urlpatterns = [
    path('', views.index),
]