from django.shortcuts import render
from django.http import HttpResponse
from medicine_app.models import *
# Create your views here.


def index(request, code):
    item = Items.objects.get(code=int(code))
    return render(request, "index.html", {"item":item})


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
    user = request.user
    boxes = Items.objects.filter(owner=user, is_box=True)
    return render(request, "dashboard.html", {"boxes":boxes})