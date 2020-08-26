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
        logo = SystemLogo.objects.all()[0]
        return render(request, "login.html", {"logo":logo})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        user = User.objects.get(username="root")
        items = Items.objects.filter(is_box=True)
        scanned_items = items.filter(box__received=True)
        unscanned_items = items.filter(box__received=False)
        return render(request, "index.html", {
            "scanned_items":scanned_items,
            "unscanned_items":unscanned_items,
            "medicine_count":Medicines.objects.all().count(),
            "code_count":Items.objects.all().count(),
            "importers_count":Importers.objects.all().count(),
            "downloaded_code":Items.objects.filter(downloaded=True).count(),
            }
        )
    elif PBB.objects.filter(user=user):
        return HttpResponseRedirect("/dashboard")
    elif Importers.objects.filter(user=user):
        items = Items.objects.filter(importer=Importers.objects.get(user=user)).order_by("first_column")
        print(items.count())
        print(items.values("code"))
        return render(request, "users_index.html", {
            "code_count":items.count(),
            "used":items.filter(used=True).count(),
            "items":items,
            }
        )
    elif Manufacturers.objects.filter(user=user):
        items = Items.objects.filter(importer=Importers.objects.get(user=user))
        return render(request, "users_index.html", {
            "code_count":items.count(),
            "used":items.filter(used=True).count(),
            "items":items.order_by("code"),
            }
        )
    elif Pharmacies.objects.filter(user=user) or Chemists.objects.filter(user=user):
        items = Items.objects.filter(box__receiver=user, is_box=True).order_by("first_column")
        scanned = items.filter(box__received=True)
        unscanned = items.filter(box__received=False)
        return render(request, "table.html", {
            "code_count":items.count(),
            #"used":items,
            "unscanned_items":unscanned,
            "items":scanned.order_by("code"),
            }
        )
    elif Chemists.objects.filter(user=user) or Chemists.objects.filter(user=user):
        items = Items.objects.filter(box__receiver=user, is_box=True).order_by("first_column")
        scanned = items.filter(box__received=True)
        unscanned = items.filter(box__received=False)
        return render(request, "table.html", {
            "code_count":items.count(),
            #"used":items,
            "unscanned_items":unscanned,
            "items":scanned.order_by("code"),
            }
        )
        


# def code_generation(): # first sequential code
#     # 100018266872|0281133943854617
#     first = randint(111111111111, 999999999999)
#     second = randint(1111111111111111, 9999999999999999)
#     return str(first)+"-"+str(second)

def second_code_generate():
    return randint(1111111111111111, 9999999999999999)


@login_required
def generate_codes(request):
    if request.user.is_superuser:
        if request.method == "GET":
            user = User.objects.all()[0]
            medicines = Medicines.objects.all()
            importers = Importers.objects.all()
            targets = Pharmacies.objects.all()
            return render(request, "generate_codes.html", {
                "medicines":medicines,
                "importers":importers,
                "targets":targets,
                "medicine_count":Medicines.objects.all().count(),
                "code_count":Items.objects.all().count(),

            })
        elif request.method == "POST":
            # medicine_id = request.POST.get("medicine")
            # importer_id = request.POST.get("importer")
            # owner_id = request.POST.get("owner")
            # target_id = request.POST.get("target")
            box_count = request.POST.get("box")
            download_count = request.POST.get("download_count")
            # packet_count = request.POST.get("packet")
            # medicine = Medicines.objects.get(id=medicine_id)
            # importer = Admin_B.objects.get(id=importer_id)
            # target = Admin_C.objects.get(id=target_id)
            #print(target_id, target)
            # loop_count = 0
            if box_count:
                system_code  = SystemCodeCount.objects.all()[0]
                first = system_code.count
                system_code.count = str(int(first) + int(box_count))
                system_code.save()
                for i in range(1, int(box_count)+1):
                    # box = Boxes.objects.create(
                    #     medicine=medicine,
                    #     importer=importer,
                    #     quantity=int(packet_count),
                    #     target=target,
                    #     )
                    second = second_code_generate()
                    item_code = str(int(first)+i)+"-"+str(second)
                    item = Items.objects.create(code=item_code, first_column=str(int(first)+i))
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
def download_codes(request):
    user = request.user
    if request.user.is_superuser:
        if request.method == "GET":
            user = User.objects.all()[0]
            medicines = Medicines.objects.all()
            importers = Importers.objects.all()
            targets = Pharmacies.objects.all()
            items = Items.objects.all()
            return render(request, "download_codes.html", {
                "medicines":medicines,
                "importers":importers,
                "targets":targets,
                "medicine_count":Medicines.objects.all().count(),
                "code_count":items.count(),
                "available_codes":items.filter(downloaded=False).count(),
                "importers_count":importers.count()

            })
        elif request.method == "POST":
            download_count = request.POST.get("download_count")
            print(download_count)
            system_code  = SystemCodeCount.objects.all()[0]
            last_download = system_code.download
            system_code.download = str(int(last_download) + int(download_count))
            system_code.save()
            #print process
            random_integer = str(randint(111111,9999999))
            f = open("static/media/{}.txt".format(random_integer), "w")
            for x in range(int(last_download)+1, int(last_download)+int(download_count)+1):
                print(x)
                item = Items.objects.get(first_column=x)
                item.downloaded = True
                item.save()
                f.write("PBB:"+str(item.code)+"\n")
            f.close()
            file_instance = Files.objects.create(printed_by=user)
            f = open("static/media/{}.txt".format(random_integer), "r") #always open in read mode r
            random_integer2 = str(randint(111111,9999999))
            file_instance.exported_file.save("{}.txt".format(random_integer2), File(f))
            file_instance.save()
            return HttpResponseRedirect("/download/{}".format(file_instance.id))









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


# def qrcode_setuser(request, code, id):
#     user = User.objects.get(id=id)
#     item = Items.objects.get(code=code)
#     if item.is_box:
#         for packet in item.box.get_items():
#             packet.owner = user
#             packet.save()
#     else:
#         item.owner = user 
#         item.save()

#     return HttpResponse("Owners changed")

@login_required
def receive_codes(request):
    items = Items.objects.all()
    ##scanned_items = items.filter(box__received=True)
    ##unscanned_items = items.filter(box__received=False)
    generated = items.filter(downloaded=False).order_by("code")
    downloaded = items.filter(downloaded=True).order_by("code")
    if request.method == "GET":
        try:
            pharmacy = Pharmacies.objects.get(user=request.user)
        except:
            pharmacy = False
        try:
            chemist = Chemists.objects.get(user=request.user)
        except:
            chemist = False
        if chemist or pharmacy:
            page = "eczaci_receive.html"
        else:
            page = "pbb_receive.html"
        return render(request, page,  {
                ##"scanned_items":scanned_items,
                ##"unscanned_items":unscanned_items,
                "manufacturers":Manufacturers.objects.all().count(),
                "importers":Importers.objects.all().count(),
                "distributors":Distributors.objects.all().count(),
                "pharmacies":Pharmacies.objects.all().count(),
                "generated":generated,
                "downloaded_items": downloaded,
                "medicine_count":Medicines.objects.all().count(),
                "code_count":items.count(),
                "downloaded_count":downloaded.count(),
                "importers_count":Importers.objects.all().count(),
                "downloaded_rate": str(int(items.count()) - int(downloaded.count())),
                "pbb_approved":items.filter(is_active=True).count()
                })
    elif request.method == "POST":
        first = request.POST.get("first")
        last = request.POST.get("last")
        for x in range(int(first), int(last)+1):
            try:
                item = Items.objects.get(first_column=x)
            except:
                alert = "Codes Are Not Available"
                return render(request, "pbb_receive.html",  {
                    ##"scanned_items":scanned_items,
                    ##"unscanned_items":unscanned_items,
                    "manufacturers":Manufacturers.objects.all().count(),
                    "importers":Importers.objects.all().count(),
                    "distributors":Distributors.objects.all().count(),
                    "pharmacies":Pharmacies.objects.all().count(),
                    "generated":generated,
                    "downloaded_items": downloaded,
                    "medicine_count":Medicines.objects.all().count(),
                    "code_count":items.count(),
                    "downloaded_count":downloaded.count(),
                    "importers_count":Importers.objects.all().count(),
                    "downloaded_rate": str(int(items.count()) - int(downloaded.count())),
                    "pbb_approved":items.filter(is_active=True).count(),
                    "alert":alert,
                    }
                )
            if item.is_active:
                alert = "Already Registered"
                return render(request, "pbb_receive.html",  {
                    ##"scanned_items":scanned_items,
                    ##"unscanned_items":unscanned_items,
                    "manufacturers":Manufacturers.objects.all().count(),
                    "importers":Importers.objects.all().count(),
                    "distributors":Distributors.objects.all().count(),
                    "pharmacies":Pharmacies.objects.all().count(),
                    "generated":generated,
                    "downloaded_items": downloaded,
                    "medicine_count":Medicines.objects.all().count(),
                    "code_count":items.count(),
                    "downloaded_count":downloaded.count(),
                    "importers_count":Importers.objects.all().count(),
                    "downloaded_rate": str(int(items.count()) - int(downloaded.count())),
                    "pbb_approved":items.filter(is_active=True).count(),
                    "alert":alert,
                    }
                )
            if item.box:
                try:
                    pharmacy = Pharmacies.objects.get(user=request.user)
                except:
                    pharmacy = False
                try:
                    chemist = Chemists.objects.get(user=request.user)
                except:
                    chemist = False
                if chemist or pharmacy:
                    box = item.box
                    box.receiver = request.user
                    box.received = True
                    box.save()        
            item.is_active = True
            item.save()
        return HttpResponseRedirect("/receive_codes")
@login_required
def dashboard(request):
    if request.user.is_superuser:
        user = User.objects.get(username="root")
        items = Items.objects.all()
        ##scanned_items = items.filter(box__received=True)
        ##unscanned_items = items.filter(box__received=False)
        generated = items.filter(downloaded=False).order_by("code")
        downloaded = items.filter(downloaded=True).order_by("code")

        return render(request, "dashboard.html", {
            ##"scanned_items":scanned_items,
            ##"unscanned_items":unscanned_items,
            "generated":generated,
            "downloaded_items": downloaded,
            "medicine_count":Medicines.objects.all().count(),
            "code_count":items.count(),
            "downloaded_count":downloaded.count(),
            "importers_count":Admin_B.objects.all().count(),
            "downloaded_rate": str(int(items.count()) - int(downloaded.count()))
            }
        )
    elif PBB.objects.filter(user=request.user):
        items = Items.objects.all()
        ##scanned_items = items.filter(box__received=True)
        ##unscanned_items = items.filter(box__received=False)
        generated = items.filter(downloaded=False).order_by("code")
        downloaded = items.filter(downloaded=True).order_by("code")

        return render(request, "pbb_dashboard.html", {
            ##"scanned_items":scanned_items,
            ##"unscanned_items":unscanned_items,
            "manufacturers":Manufacturers.objects.all().count(),
            "importers":Importers.objects.all().count(),
            "distributors":Distributors.objects.all().count(),
            "pharmacies":Pharmacies.objects.all().count(),
            "chemists":Chemists.objects.all().count(),
            "generated":generated,
            "downloaded_items": downloaded,
            "medicine_count":Medicines.objects.all().count(),
            "code_count":items.count(),
            "downloaded_count":downloaded.count(),
            "importers_count":Importers.objects.all().count(),
            "downloaded_rate": str(int(items.count()) - int(downloaded.count()))
            }
        )


@login_required
def issue_codes(request):
    user = request.user
    check_pbb = PBB.objects.filter(user=user)
    if check_pbb: # if user is PBB
        if request.method == "GET":
            importers = Importers.objects.all()

            return render(request, "pbb_issue_codes.html", {
                "manufacturers":Manufacturers.objects.all(),
                "importers":Importers.objects.all(),
                "distributors":Distributors.objects.all(),
                "pharmacies":Pharmacies.objects.all(),
                "chemistis":Chemists.objects.all(),
                "medicine_count":Medicines.objects.all().count(),
                "code_count":Items.objects.all().count(),
                "manufacturers_count":Manufacturers.objects.all().count(),
                "importers_count":Importers.objects.all().count(),
                "distributors_count":Distributors.objects.all().count(),
                "pharmacies_count":Pharmacies.objects.all().count(),
                "chemists_count":Chemists.objects.all().count(),
                "pbb_approved":Items.objects.filter(is_active=True).count(),
                "available_codes":Items.objects.filter(downloaded=True, is_issued=False).count(),

            })
        elif request.method == "POST":
            # medicine_id = request.POST.get("medicine")
            importer_id = request.POST.get("importer")
            manufacturer_id = request.POST.get("manufacturer")
            # target_id = request.POST.get("target")
            download_count = request.POST.get("download_count")
            # packet_count = request.POST.get("packet")
            # medicine = Medicines.objects.get(id=medicine_id)
            if importer_id != "Choose...":
                importer = Importers.objects.get(id=importer_id)
            else:
                importer = None
            if manufacturer_id != "Choose...":
                manufacturer = Manufacturers.objects.get(id=manufacturer_id)
            else:
                manufacturer = None
            first = request.POST.get("first")
            last = request.POST.get("last")
            for x in range(int(first), int(last)+1):
                item = Items.objects.get(first_column=x)
                item.is_issued = True
                if importer:
                    item.importer = importer
                elif manufacturer:
                    item.manufacturer = manufacturer
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
    else:
        check_importer = Importers.objects.filter(user=user)
        check_manufacturer = Manufacturers.objects.filter(user=user)
        if check_importer:
            medicines = Medicines.objects.filter(importer=check_importer[0])
            items = Items.objects.filter(importer=check_importer[0])
            not_used = items.filter(used=False).order_by("first_column")
            used = items.filter(used=True).order_by("first_column")

        elif check_distributor:
            medicines = Medicines.objects.filter(manufacturer=check_menufacturer[0])
            items = Items.objects.filter(manufacturer=check_manufacturer[0])
            not_used = items.filter(used=False).order_by("first_column")
            used = items.filter(used=True).order_by("first_column")
        else:
            return HttpResponseRedirect("/")
        if request.method == "GET":
            return render(request, "user_issue_codes.html", {
                "medicines":medicines,
                "code_count":items.count(),
                "used":used.count(),
            })
        elif request.method == "POST":
            medicine_id = request.POST.get("medicine")
            box = int(request.POST.get("box"))
            packet = int(request.POST.get("packet"))
            totalCode_need = (box * packet) + box
            print(totalCode_need)
            medicine = Medicines.objects.get(id=medicine_id)
            code_count = items.count()
            counter = 0
            not_used = list(not_used)
            box_array = []
            for i in range(1, box+1):
                item = not_used[counter]
                box_obj = Boxes.objects.create(medicine=medicine, code=item.code, quantity=packet)
                box_obj.save()
                box_array.append(box_obj)
                item.medicine = medicine
                if check_importer:
                    item.importer = check_importer[0]
                elif check_manufacturer:
                    item.manufacturer = check_manufacturer[0]
                item.is_box = True
                item.box = box_obj
                item.used = True
                item.save()
                print("BOX "+str(item.code))
                print(counter)
                counter += 1
                for j in range(1, packet+1):
                    print(counter)
                    item = not_used[counter]
                    item.medicine = medicine
                    if check_importer:
                        item.importer = check_importer[0]
                    elif check_manufacturer:
                        item.manufacturer = check_manufacturer[0]
                    item.box = box_obj
                    item.used = True
                    item.save()
                    print("Packet "+str(item.code))
                    counter+=1
            
            return render(request, "user_issue_codes.html", {
                "medicines":medicines,
                "code_count":items.count(),
                "used":used.count(),
                "box_codes":box_array,
            })
                
                

                
                    

