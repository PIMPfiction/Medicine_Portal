from django.urls import path, include
from medicine_app import views


urlpatterns = [
    path('', views.index),
    path('query/<str:code>', views.index),
    path('query/<str:code>/<str:id>', views.qrcode_setuser),
    path('dashboard/', views.dashboard),
]