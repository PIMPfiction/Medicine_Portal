from rest_framework.serializers import ModelSerializer
from medicine_app.models import *
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "is_superuser", "username", "first_name", "last_name", "email")


# class SuperAdminSerializer(ModelSerializer):

#     class Meta:
#         model = SuperAdmin
#         fields = '__all__'


# class Admin_ASerializer(ModelSerializer):

#     class Meta:
#         model = Admin_A
#         fields = '__all__'


# # class Admin_BSerializer(ModelSerializer):

# #     class Meta:
# #         model = Admin_B
# #         fields = '__all__'


# # class Admin_CSerializer(ModelSerializer):

# #     class Meta:
# #         model = Admin_C
# #         fields = '__all__'


# class StocksSerializer(ModelSerializer):

#     class Meta:
#         model = Stocks
#         fields = '__all__'


# class BrandsSerializer(ModelSerializer):

#     class Meta:
#         model = Brands
#         fields = '__all__'


# class CategoriesSerializer(ModelSerializer):

#     class Meta:
#         model = Categories
#         fields = '__all__'


# class SubCategoriesSerializer(ModelSerializer):
#     category = CategoriesSerializer(read_only=True)

#     class Meta:
#         model = SubCategories
#         fields = '__all__'


class MedicinesSerializer(ModelSerializer):
    # brand = BrandsSerializer(read_only=True)
    # category = SubCategoriesSerializer(read_only=True)

    class Meta:
        model = Medicines
        fields = '__all__'


class BoxesSerializer(ModelSerializer):
    # importer = Admin_BSerializer(read_only=True)

    class Meta:
        model = Boxes
        fields = '__all__'


class ItemsSerializer(ModelSerializer):
    lookup_field = 'code'
    box = BoxesSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    medicine = MedicinesSerializer(read_only=True)
    class Meta:
        model = Items
        fields = '__all__'

    
