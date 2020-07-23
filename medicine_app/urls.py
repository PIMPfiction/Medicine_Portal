from django.urls import path, include
from medicine_app import views


urlpatterns = [
    path('', views.index),
    path('query/<str:code>', views.code_info),
    path('query/<str:code>/<str:id>', views.qrcode_setuser),
    path('dashboard/', views.dashboard),

    path('print_codes/<str:code>', views.print_codes),
    path('download/<str:id>', views.download_file),
]