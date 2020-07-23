from rest_framework.viewsets import ModelViewSet
from medicine_app.serializers import SuperAdminSerializer, Admin_ASerializer, Admin_BSerializer, Admin_CSerializer, StocksSerializer, BrandsSerializer, CategoriesSerializer, SubCategoriesSerializer, MedicinesSerializer, BoxesSerializer, ItemsSerializer
from medicine_app.models import SuperAdmin, Admin_A, Admin_B, Admin_C, Stocks, Brands, Categories, SubCategories, Medicines, Boxes, Items
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

class SuperAdminViewSet(ModelViewSet):
    queryset = SuperAdmin.objects.order_by('pk')
    serializer_class = SuperAdminSerializer


class Admin_AViewSet(ModelViewSet):
    queryset = Admin_A.objects.order_by('pk')
    serializer_class = Admin_ASerializer


class Admin_BViewSet(ModelViewSet):
    queryset = Admin_B.objects.order_by('pk')
    serializer_class = Admin_BSerializer


class Admin_CViewSet(ModelViewSet):
    queryset = Admin_C.objects.order_by('pk')
    serializer_class = Admin_CSerializer


class StocksViewSet(ModelViewSet):
    queryset = Stocks.objects.order_by('pk')
    serializer_class = StocksSerializer


class BrandsViewSet(ModelViewSet):
    queryset = Brands.objects.order_by('pk')
    serializer_class = BrandsSerializer


class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.order_by('pk')
    serializer_class = CategoriesSerializer


class SubCategoriesViewSet(ModelViewSet):
    queryset = SubCategories.objects.order_by('pk')
    serializer_class = SubCategoriesSerializer


class MedicinesViewSet(ModelViewSet):
    queryset = Medicines.objects.order_by('pk')
    serializer_class = MedicinesSerializer


class BoxesViewSet(ModelViewSet):
    queryset = Boxes.objects.order_by('pk')
    serializer_class = BoxesSerializer


class ItemsViewSet(ModelViewSet):
    queryset = Items.objects.order_by('pk')
    serializer_class = ItemsSerializer
    # filterset_fields = ("medicine", "code", "box", "is_box")
    # filter_backends = [DjangoFilterBackend]
    def get_queryset(self):
        queryset = super(ItemsViewSet, self).get_queryset()

        box_index = self.request.query_params.get('box_code', '')
        if box_index:
            return queryset.filter(box__code=box_index)
        else:
            return queryset
        # order_by = self.request.query_params.get('order_by', '')
        # if order_by:
        #     order_by_name = order_by.split(' ')[1]
        #     order_by_sign = order_by.split(' ')[0]
        #     order_by_sign = '' if order_by_sign == 'asc' else '-'
        #     queryset = queryset.order_by(order_by_sign + order_by_name)
        # populer = self.request.query_params.get('populer', '')
        # if populer:
        #     queryset = queryset.order_by("-ziyaret_sayisi")[:3]
        # soneklenen = self.request.query_params.get("soneklenen", "")
        # if soneklenen:
        #     queryset = queryset.order_by("-id")[:3]

        
        # return queryset

