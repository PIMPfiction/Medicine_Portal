from django.urls import path, include
from medicine_app import views


urlpatterns = [
    path('', views.index),
    path('login/', views.user_login),
    path('logout', views.user_logout),
    path('query/<str:code>', views.code_info),
    path('query/<str:code>/<str:id>', views.qrcode_setuser),
    path('dashboard/', views.dashboard),
    path('generate_codes/', views.generate_codes),

    path('print_codes/<str:code>', views.print_codes),
    path('download/<str:id>', views.download_file),
]