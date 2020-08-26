from rest_framework.routers import SimpleRouter
from medicine_app import views
from rest_framework import routers
from rest_framework.routers import SimpleRouter, DefaultRouter
from medicine_app import api_views as views
router = routers.DefaultRouter()

# router.register(r'superadmin', views.SuperAdminViewSet)
# router.register(r'admin_a', views.Admin_AViewSet)
# router.register(r'admin_b', views.Admin_BViewSet)
# router.register(r'admin_c', views.Admin_CViewSet)
# router.register(r'stocks', views.StocksViewSet)
# router.register(r'brands', views.BrandsViewSet)
# router.register(r'categories', views.CategoriesViewSet)
# router.register(r'subcategories', views.SubCategoriesViewSet)
router.register(r'medicines', views.MedicinesViewSet)
router.register(r'boxes', views.BoxesViewSet)
router.register(r'items', views.ItemsViewSet)

urlpatterns = router.urls
