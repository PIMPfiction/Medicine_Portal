from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# Create your models here.


class SuperAdmin(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Admin_A(models.Model):  #THERE WILL BE ONly ONE ADMIN_A CREATED BY SUPERADMIN
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if not self.id:
            group = Group.objects.get(name="admin_a")
            group.user_set.add(self.user)
            
        super(Admin_A, self).save(*args, **kwargs)

class Admin_B(models.Model): #Distrubitors
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            group = Group.objects.get(name="admin_b")
            group.user_set.add(self.user)
        super(Admin_B, self).save(*args, **kwargs)


class Admin_C(models.Model):  # Pharmacy
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            group = Group.objects.get(name="admin_c")
            group.user_set.add(self.user)
        super(Admin_C, self).save(*args, **kwargs)



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

    def all_medicines(self):
        return Medicines.objects.filter(brand=self)

class Medicines(models.Model):
    chemical = models.TextField(max_length=200, default=None)
    generic = models.TextField(max_length=200, default=None)
    amount = models.TextField(max_length=200, default=None) # miligram or cLitre 
    brand = models.ForeignKey("Brands", on_delete=models.CASCADE)

    def __str__(self):
        return self.generic


class Boxes(models.Model):
    medicine = models.ForeignKey("Medicines", on_delete=models.CASCADE)
    code = models.TextField(max_length=100)
    quantity = models.IntegerField()
    # items = models.ManyToManyField("Items", on_delete=models.CASCADE)

    def __str__(self):
        return self.medicine.generic 

    def save(self, *args, **kwargs):
        if not self.id:
            first_creation = True
        else:
            first_creation = False
        super().save(*args, **kwargs)
        if first_creation:
            for i in range(1, self.quantity+1):
                item = Items.objects.create(box=self, medicine=self.medicine, code=int(self.code)+i)
                item.save()

class Items(models.Model):
    medicine = models.ForeignKey("Medicines", on_delete=models.CASCADE)
    code = models.TextField(max_length=100)
    box = models.ForeignKey("Boxes", on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "%s - %s" % (self.medicine.generic, self.code)
#TODO: autogenreate random key
