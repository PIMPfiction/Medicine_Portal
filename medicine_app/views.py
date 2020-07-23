from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from medicine_app.models import *
import os
from django.core.files import File
from random import *
# Create your views here.
from django.conf import settings

def index(request):
    user = User.objects.all()[0]
    items = Items.objects.filter(is_box=True)
    return render(request, "index.html", {"items":items})

def print_codes(request, code):
    user = User.objects.all()[0]
    item = Items.objects.get(code=code)
    random_integer = str(randint(111111,9999999))
    f = open("static/media/{}.txt".format(random_integer), "w")
    for x in item.box.get_items():
        f.write(settings.DOMAIN+"/api/items/"+str(x.code)+",")
    f.close()
    file_instance = Files.objects.create(printed_by=user)
    f = open("static/media/{}.txt".format(random_integer), "r") #always open in read mode r
    random_integer2 = str(randint(111111,9999999))
    file_instance.exported_file.save("{}.txt".format(random_integer2), File(f))
    file_instance.save()
    return HttpResponseRedirect("/download/{}".format(file_instance.id))


def download_file(request, id):
    file_instance = Files.objects.get(id=id)
    txt_file = file_instance.exported_file
    filename = txt_file.name.split('/')[-1]
    response = HttpResponse(txt_file.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response



def code_info(request, code):
    item = Items.objects.get(code=int(code))
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