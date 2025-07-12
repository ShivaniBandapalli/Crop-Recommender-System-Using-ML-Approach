from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl


# Create your views here.
from Remote_User.models import ClientRegister_Model,crop_prediction,detection_ratio,crop_recommendation

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city)

        return render(request, 'RUser/Register1.html')
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_Crop_Yiled_OnDataSets(request):
        expense = 0
        kg_price=0
        if request.method == "POST":

            State = request.POST.get('State')
            cname=request.POST.get('cname')
            area = request.POST.get('area')
            stype = request.POST.get('stype')

            area1=int(area)

            if area1 < 10:
                production = 5000
            elif area1 < 50 and area1 > 10:
                production = 10000
            elif area1 < 100 and area1 > 50:
                production = 25000
            elif area1 < 250 and area1 > 100:
                production = 50000
                print(expense)
            elif area1 < 500 and area1 > 250:
                production = 100000
            else:
                production = 200000

            if area1<10:
                expense=15000
            elif area1<50 and area1>10:
                expense=70000
            elif area1 < 100 and area1 > 50:
                expense = 100000
            elif area1 < 250 and area1 > 100:
                expense = 150000
                print(expense)
            elif area1 < 500 and area1 > 250:
                expense = 200000
            else:
                expense=300000


            if  cname=="Dry ginger":
                kg_price=100
            elif cname == "Sugarcane":
                 kg_price = 50
            elif cname == "Sweet potato":
                 kg_price = 40
            elif cname == "Sugarcane":
                kg_price = 50
            elif cname == "Rice":
                kg_price = 50
            elif cname == "Banana":
                kg_price = 70
                print(kg_price)
            elif cname == "Black pepper":
                kg_price = 1170
            elif cname == "Coconut":
                kg_price = 25
            elif cname == "Dry chillies":
                kg_price = 400
            elif cname == "Grapes":
                kg_price = 50
            elif cname == "Groundnut":
                kg_price = 170
            elif cname == "Horse-gram":
                kg_price = 70
            elif cname == "Jowar":
                kg_price = 80
            elif cname == "Maize":
                 kg_price = 50
            elif cname == "Moong_Green Gram":
                 kg_price = 40
            elif cname == "Onion":
                kg_price = 90
            elif cname == "Ragi":
                kg_price = 70
            elif cname == "Small millets":
                kg_price = 120
            elif cname == "Soyabean":
                kg_price = 170
            elif cname == "Urad":
                kg_price = 125
            elif cname == "Bajra":
                kg_price = 400
            elif cname == "Turmeric":
                kg_price = 1250
            elif cname == "Potato":
                kg_price = 50
            elif cname == "Wheat":
                kg_price = 90
            elif cname == "Coriander":
                kg_price = 280
            elif cname == "Arecanut":
                kg_price = 180



            production1 = int(production)

            yield1=(production1*(kg_price))-int(expense)

            prod=production1/area1

            crop_prediction.objects.create(State_Name=State,names=cname,Area=area,Soil_Type=stype,Yield_Prediction=yield1,Production_Prediction=prod)


            return render(request, 'RUser/Predict_Crop_Yiled_OnDataSets.html',{'objs':yield1,'objs1':prod})
        return render(request, 'RUser/Predict_Crop_Yiled_OnDataSets.html')


def Recommend_Crop(request):
    expense = 0
    kg_price = 0
    if request.method == "POST":

        State = request.POST.get('State')
        area = request.POST.get('area')
        stype = request.POST.get('stype')

        area1=int(area)

        if stype == "Sandy" and area1>20:
            Crop_Name = "Groundnet"
        elif stype == "Loamy" and area1>50:
            Crop_Name = "Wheat OR Gram OR Sugarcane OR Jute OR Vegetables"
        elif stype == "Black" and area1>70:
            Crop_Name = "Cotton crop OR  Jowar OR Sunflower and millets"
        elif stype == "Red" and area1>150:
            Crop_Name = "Cotton OR Wheat OR pulses OR millets OR tobacco OR oil seeds OR Potatoes"
        elif stype == "Peat" and area1>60:
            Crop_Name = "Potatoes, OR sugar beet, OR celery, OR onions, OR carrots, lettuce and market garden crops"
        elif stype == "Silt" and area1>50:
            Crop_Name = "Tomatoes, OR sage, OR peonies,OR hellebore,OR roses, OR butterfly bush, OR ferns,OR daffodils"
        elif stype == "Chalk" and area1>50:
            Crop_Name = "Akebia,OR Clematis, OR Grape vines,OR Ivy,Jasmine,OR Lonicera and Virginia creeper"
        else:
            Crop_Name="No Recomendatiaon"

        crop_recommendation.objects.create(State_Name=State,names=Crop_Name,Area=area,Soil_Type=stype)

        return render(request, 'RUser/Recommend_Crop.html', {'objs': Crop_Name})
    return render(request, 'RUser/Recommend_Crop.html')



