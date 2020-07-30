from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# Create your models here.
from random import randint

class SuperAdmin(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Admin_A(models.Model):  #THERE WILL BE ONly ONE ADMIN_A CREATED BY SUPERADMIN
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if not self.id:
            group = Group.objects.get(name="admin_a")
            group.user_set.add(self.user)
            
        super(Admin_A, self).save(*args, **kwargs)

    class META:
        verbose_name = "super admin"
        verbose_name_plural = "super admin"

class Admin_B(models.Model): #Distrubitors IMPORTERS
    #user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.TextField(max_length=60, default=None, null=True)
    address = models.TextField(max_length=350, default="P.O. Box 99376 - 80100, Mombasa. P.O. Box 2138 - 20100, Nakuru.", null=True)
    phone = models.TextField(max_length=60, default="+ 254 (20) 694 8000", null=True)
    email = models.TextField(max_length=60, default="info@kebs.org", null=True)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         group = Group.objects.get(name="admin_b")
    #         group.user_set.add(self.user)
    #     super(Admin_B, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    class META:
        verbose_name = "importers"
        verbose_name_plural = "importers"


class Admin_C(models.Model):  # Pharmacy
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=60, default=None, null=True)
    address = models.TextField(max_length=350, default=None, null=True)
    phone = models.TextField(max_length=60, default=None, null=True)
    email = models.TextField(max_length=60, default=None, null=True)

    class META:
        verbose_name = "pharmacies"
        verbose_name_plural = "pharmacies"


    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         group = Group.objects.get(name="admin_c")
    #         group.user_set.add(self.user)
    #     super(Admin_C, self).save(*args, **kwargs)



class Stocks(models.Model):
    medicine = models.ForeignKey("Medicines", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    super_admin = models.ForeignKey('SuperAdmin', on_delete=models.CASCADE, related_name="superadmin", blank=True, null=True)
    admin_a = models.ForeignKey('Admin_A', on_delete=models.CASCADE, related_name="admin_a", blank=True, null=True)
    admin_b = models.ForeignKey('Admin_B', on_delete=models.CASCADE, related_name="admin_b",blank=True,null=True)
    admin_c = models.ForeignKey('Admin_C', on_delete=models.CASCADE, related_name="admin_c", blank=True, null=True)
    def __str__(self):
        for owner in [self.super_admin, self.admin_a, self.admin_b, self.admin_c]:
            if owner:
                break
        return self.medicine.generic + " "  + str(self.quantity) + " " + str(owner.user.username) + " "

        
class Brands(models.Model):
    name = models.TextField(max_length=200, default=None)

    def __str__(self):
        return self.name

    def all_medicines(self):
        return Medicines.objects.filter(brand=self)


class Categories(models.Model):
    name = models.TextField(max_length=60)


class SubCategories(models.Model):
    name = models.TextField(max_length=60)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)

class Medicines(models.Model):
    item_no = models.IntegerField(null=True)
    importer = models.ForeignKey("admin_b", default=None, on_delete=models.CASCADE, null=True)
    chemical = models.CharField(max_length=200, default=None)
    generic = models.CharField(max_length=200, default=None)  # item name
    #amount = models.CharField(max_length=200, default=None) # miligram or cLitre 
    #brand = models.ForeignKey("Brands", on_delete=models.CASCADE)
    # drugs or surgical
    profile = models.CharField(max_length=50, default="drugs")

    itemTypeChoices = (("TABLETS", "TABLETS"), ("GEL", "GEL"), ("INJECTION", "INJECTION"), ("CAPSULES", "CAPSULES"), ("SYRUP", "SYRUP"), ("SUSPENSION", "SUSPENSION"))
    item_type = models.TextField(
        max_length=50, choices=itemTypeChoices, default=None, null=True)

    measureChoices = (("TABLETS", "TABLETS"), ("PIECE", "PIECE"), ("TUBE", "TUBE"), ("VIALS", "VIALS"), ("AMPOULES", "AMPOULES"), ("BOTTLE", "BOTTLE"))
    measure = models.TextField(
        max_length=50, choices=measureChoices, default=None, null=True)

    formulationChoices = (("TABLETS", "TABLETS"), ("CREAM", "CREAM"), ("INJECTION", "INJECTION"), ("SUSPENSION", "SUSPENSION"), ("SYRUP", "SYRUP"), ("ORAL SOLUTION", "ORAL SOLUTION"))
    formulation = models.TextField(
        max_length=50, choices=formulationChoices, default=None, null=True)

    routeChoices = (("PO", "PO"), ("IV", "IV"), ("PR", "PR"), ("IM", "IM"), ("TOPICAL", "TOPICAL"))
    route = models.TextField(max_length=50, choices=routeChoices, default=None, null=True)
    
    pbb_code = models.CharField(max_length=50, default=None, null=True)

    #category = models.ForeignKey("SubCategories", on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.generic


def code_generation():
    # 100018266872|0281133943854617
    first = randint(111111111111, 999999999999)
    second = randint(1111111111111111, 9999999999999999)
    return str(first)+"-"+str(second)

class Boxes(models.Model): #BOXES
    medicine = models.ForeignKey("Medicines", on_delete=models.CASCADE)
    importer = models.ForeignKey("admin_b", default=None, on_delete=models.CASCADE, null=True)
    code = models.TextField(max_length=100, blank=True, default=code_generation)
    quantity = models.IntegerField()
    received = models.BooleanField(default=False)
    target = models.ForeignKey("Admin_C", default=None, on_delete=models.CASCADE, null=True)

    # items = models.ManyToManyField("Items", on_delete=models.CASCADE)

    def __str__(self):
        return self.medicine.generic 

    def get_items(self):
        return Items.objects.filter(box=self)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         first_creation = True
    #     else:
    #         first_creation = False
    #     super().save(*args, **kwargs)
    #     if first_creation:
    #         item = Items.objects.create(box=self, medicine=self.medicine, code=self.code, is_box=True)
    #         for i in range(1, self.quantity+1):
    #             first, second = self.code.split("-")
    #             item_code = str(int(first)+i)+"-"+second
    #             item = Items.objects.create(box=self, medicine=self.medicine, code=item_code)
    #             item.save()
    

class Items(models.Model): #PACKETS # this will be the main code this will hold the GENERATED CODES
    medicine = models.ForeignKey("Medicines", on_delete=models.CASCADE)
    code = models.TextField(max_length=100, primary_key=True)
    box = models.ForeignKey("Boxes", on_delete=models.CASCADE, default=None)
    is_active = models.BooleanField(default=False)
    is_box = models.BooleanField(default=False) #defines 
    owner = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s - %s" % (self.medicine.generic, self.code)
#TODO: autogenreate random key
#TODO: eger codelar uretıldıyse ve daha stoklara eklenmedıyse is_active false kalicak_ kodlar qrdcodedan taratilip stoga alindiginda is_active alani true olarak degistirilecek


class Files(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    printed_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)
    exported_file = models.FileField(default=None, blank=True)