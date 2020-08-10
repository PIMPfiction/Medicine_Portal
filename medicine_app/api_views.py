# from rest_framework.viewsets import ModelViewSet
# from medicine_app.serializers import *
# from medicine_app.models import *
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import generics
# from rest_framework import filters
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.generics import *

# class SuperAdminViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = SuperAdmin.objects.order_by('pk')
#     serializer_class = SuperAdminSerializer


# class Admin_AViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Admin_A.objects.order_by('pk')
#     serializer_class = Admin_ASerializer


# # class Admin_BViewSet(ModelViewSet):
# #     permission_classes = (IsAuthenticated,)
# #     queryset = Admin_B.objects.order_by('pk')
# #     serializer_class = Admin_BSerializer


# # class Admin_CViewSet(ModelViewSet):
# #     permission_classes = (IsAuthenticated,)
# #     queryset = Admin_C.objects.order_by('pk')
# #     serializer_class = Admin_CSerializer


# class StocksViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Stocks.objects.order_by('pk')
#     serializer_class = StocksSerializer


# class BrandsViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Brands.objects.order_by('pk')
#     serializer_class = BrandsSerializer


# class CategoriesViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Categories.objects.order_by('pk')
#     serializer_class = CategoriesSerializer


# class SubCategoriesViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = SubCategories.objects.order_by('pk')
#     serializer_class = SubCategoriesSerializer


# class MedicinesViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Medicines.objects.order_by('pk')
#     serializer_class = MedicinesSerializer


# # class BoxesViewSet(ModelViewSet):
# #     permission_classes = (IsAuthenticated,)
# #     queryset = Boxes.objects.order_by('pk')
# #     serializer_class = BoxesSerializer


# class ItemsViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Items.objects.order_by('pk')
#     serializer_class = ItemsSerializer
#     # filterset_fields = ("medicine", "code", "box", "is_box")
#     # filter_backends = [DjangoFilterBackend]
#     def get_queryset(self):
#         queryset = super(ItemsViewSet, self).get_queryset()
#         box_index = self.request.query_params.get('box_code', '')
#         receive = self.request.query_params.get('receive', '')
#         if box_index:
#             return queryset.filter(box__code=box_index)
#         elif receive:
#             current_code = self.kwargs["pk"]
#             item = Items.objects.get(code=current_code)
#             if item.is_box:
#                 box = item.box
#                 if box.target.user == self.request.user:
#                     box.received = True
#                     box.save()
#             return queryset
#         else:
#             return queryset
#         # order_by = self.request.query_params.get('order_by', '')
#         # if order_by:
#         #     order_by_name = order_by.split(' ')[1]
#         #     order_by_sign = order_by.split(' ')[0]
#         #     order_by_sign = '' if order_by_sign == 'asc' else '-'
#         #     queryset = queryset.order_by(order_by_sign + order_by_name)
#         # populer = self.request.query_params.get('populer', '')
#         # if populer:
#         #     queryset = queryset.order_by("-ziyaret_sayisi")[:3]
#         # soneklenen = self.request.query_params.get("soneklenen", "")
#         # if soneklenen:
#         #     queryset = queryset.order_by("-id")[:3]

        
#         # return queryset

