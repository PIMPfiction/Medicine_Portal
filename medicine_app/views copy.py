from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from medicine_app.models import *
import os
from django.core.files import File
from random import *
# Create your views here.
from django.conf import settings
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout





def code_generation():
    # 100018266872|0281133943854617
    first = randint(111111111111, 999999999999)
    second = randint(1111111111111111, 9999999999999999)
    return str(first)+"-"+str(second)



def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.get(username=username)
        user = authenticate(username=username, password=password)
        if user is not None: #login successfull
            if user.is_active:
                login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/")
    else:
        return render(request, "login.html", {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def index(request):
    if request.user.is_superuser:
        user = User.objects.get(username="root")
        items = Items.objects.filter(is_box=True)
        scanned_items = items.filter(box__received=True)
        unscanned_items = items.filter(box__received=False)
        return render(request, "index.html", {
            "scanned_items":scanned_items,
            "unscanned_items":unscanned_items,
            "medicine_count":Medicines.objects.all().count(),
            "code_count":Items.objects.all().count(),
            "importers_count":Admin_B.objects.all().count()
            }
        )
    else:
        user = request.user
        scanned = Items.objects.filter(is_box=True, owner=Admin_C.objects.get(user=request.user)).filter(box__received=True)
        unscanned = Items.objects.filter(is_box=True, owner=Admin_C.objects.get(user=request.user)).filter(box__received=False)
        return render(request, "index.html", {
            "scanned_items":scanned,
            "unscanned_items":unscanned,
            "medicine_count":Medicines.objects.all().count(),
            "code_count":scanned.count(),
            "importers_count":Admin_B.objects.all().count()
            }
        )
@login_required
def generate_codes(request):
    if request.user.is_superuser:
        if request.method == "GET":
            user = User.objects.all()[0]
            medicines = Medicines.objects.all()
            importers = Admin_B.objects.all()
            targets = Admin_C.objects.all()
            return render(request, "generate_codes.html", {
                "medicines":medicines,
                "importers":importers,
                "targets":targets,
                "medicine_count":Medicines.objects.all().count(),
                "code_count":Items.objects.all().count(),
                "importers_count":Admin_B.objects.all().count()

            })
        elif request.method == "POST":
            medicine_id = request.POST.get("medicine")
            importer_id = request.POST.get("importer")
            owner_id = request.POST.get("owner")
            target_id = request.POST.get("target")
            box_count = request.POST.get("box")
            packet_count = request.POST.get("packet")
            medicine = Medicines.objects.get(id=medicine_id)
            importer = Admin_B.objects.get(id=importer_id)
            target = Admin_C.objects.get(id=target_id)
            print(target_id, target)
            # loop_count = 0
            for i in range(1, int(box_count)+1):
                box = Boxes.objects.create(
                    medicine=medicine,
                    importer=importer,
                    quantity=int(packet_count),
                    target=target,
                    )
                item = Items.objects.create(box=box, medicine=box.medicine, code=box.code, is_box=True, owner=target)
                for i in range(1, box.quantity+1):
                    first, second = box.code.split("-")
                    item_code = str(int(first)+i)+"-"+second
                    item = Items.objects.create(box=box, medicine=box.medicine, code=item_code)
                    item.save()
                    # loop_count +=1
                    # print("{} loop   {} created".format(loop_count,item_code))
            # item = Items.objects.create(box=self, medicine=self.medicine, code=self.code, is_box=True)
            # for i in range(1, self.quantity+1):
            #     first, second = self.code.split("-")
            #     item_code = str(int(first)+i)+"-"+second
            #     item = Items.objects.create(box=self, medicine=self.medicine, code=item_code)
            #     item.save()
            return HttpResponseRedirect("/")


@login_required
def print_codes(request, code):
    user = User.objects.get(username="root")
    item = Items.objects.get(code=code)
    random_integer = str(randint(111111,9999999))
    f = open("static/media/{}.txt".format(random_integer), "w")
    for x in item.box.get_items():
        f.write("kebs:"+str(x.code)+",")
    f.close()
    file_instance = Files.objects.create(printed_by=user)
    f = open("static/media/{}.txt".format(random_integer), "r") #always open in read mode r
    random_integer2 = str(randint(111111,9999999))
    file_instance.exported_file.save("{}.txt".format(random_integer2), File(f))
    file_instance.save()
    box = item.box 
    box.downloaded = True 
    box.save()
    return HttpResponseRedirect("/download/{}".format(file_instance.id))

@login_required
def download_file(request, id):
    file_instance = Files.objects.get(id=id)
    txt_file = file_instance.exported_file
    filename = txt_file.name.split('/')[-1]
    response = HttpResponse(txt_file.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def code_info(request, code):
    item = Items.objects.get(code=code)
    return render(request, "code_info.html", {"item":item})


def qrcode_setuser(request, code, id):
    user = User.objects.get(id=id)
    item = Items.objects.get(code=code)
    if item.is_box:
        for packet in item.box.get_items():
            packet.owner = user
            packet.save()
    else:
        item.owner = user 
        item.save()

    return HttpResponse("Owners changed")


def dashboard(request):
    user = User.objects.all()[0]
    boxes = Items.objects.filter(owner=user, is_box=True)
    return render(request, "dashboard.html", {"boxes":boxes})