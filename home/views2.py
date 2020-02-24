from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.files.storage import FileSystemStorage
from .dlib import forImport_recognize_faces_image
from .BeautyGAN import main2 as BeautyGAN
from .BeautyGAN import split as beautysplit
import cv2
import glob
import os
# import subprocess
import tensorflow as tf
import datetime
import requests
import json as jjj
from .models import Classified
# from .modelsclassified import classified
from django.core import serializers
from django.core.serializers import serialize



# from .flask.peeweetest import Classified

from .object_detection.evaluate import YoloTest
YoloTest = YoloTest()

# Create your views here.
def index(request):
    now=datetime.datetime.now()
    #return HttpResponse("<p>Hello world!</p>")
    return render(request,'home/index.html', locals())

def selected(request):
    # searchname=request.GET.get("searchname")
    if 'queryset' not in request.session:
        print("cowlist2","None")
    else:
        cowlist2 = request.session['queryset']
        print("cowlist2", cowlist2)
    luis=request.GET.get("luis")
    print("luis = ",luis)
    response = requests.get(
    url=f'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/47fdbcf4-00cb-4e9a-a55c-df61cef1a102?verbose=true&timezoneOffset=0&subscription-key=7e25519a1e41462e8561a0bd60f5ddc2&q={luis}')
    print("response.text = ",response.text)
    luisdata = jjj.loads(response.text)
    intent = luisdata['topScoringIntent']['intent']
    keyword = []
    keywordnumber = []
    if intent == "正面":
        for i in range(len(luisdata['entities'])):
            if 'resolution' not in (luisdata['entities'][i]):
                keyword.append(luisdata['entities'][i]['entity'])

            if 'resolution' in (luisdata['entities'][i]):
                keywordnumber.append(luisdata['entities'][i]['resolution']['value'])
        if len(keywordnumber) == 0:
            nonumber = True
        else:
            nonumber = False
        a = []
        b = []
        with open('home/object_detection/data/classes/111.txt','r') as f :
            for i in f.readlines():
                a.append(i.replace('\n',''))
        with open('home/object_detection/data/classes/coco.names','r') as f :
            for i in f.readlines():
                b.append(i.replace('\n',''))
        print("keyword" ,keyword)
        engindex = []
        engkey = []
        cowlist = {}
        for i in keyword:
            engindex.append(a.index(i))
        print("engindex" ,engindex)
        for i in engindex:
            engkey.append(b[i])
        print("engkey" ,engkey)
        for i in range(len(keyword)):
            if nonumber:
                keywordnumber.append('0')
                cowlist[engkey[i]] = keywordnumber[i]
            else:
                cowlist[engkey[i]] = keywordnumber[i]
        if nonumber:
            datas=Classified.objects.exclude(**cowlist)
        else:
            datas=Classified.objects.filter(**cowlist)
        request.session['queryset'] = cowlist
        print("request.session['queryset']",request.session['queryset'])
    elif intent =="負面":
        for i in range(len(luisdata['entities'])):
            if 'resolution' not in (luisdata['entities'][i]):
                keyword.append(luisdata['entities'][i]['entity'])
            if 'resolution' in (luisdata['entities'][i]):
                keywordnumber.append(luisdata['entities'][i]['resolution']['value'])
        if len(keywordnumber) == 0:
            nonumber = True
        else:
            nonumber = False
        a = []
        b = []
        with open('home/object_detection/data/classes/111.txt','r') as f :
            for i in f.readlines():
                a.append(i.replace('\n',''))
        with open('home/object_detection/data/classes/coco.names','r') as f :
            for i in f.readlines():
                b.append(i.replace('\n',''))
        print("keyword" ,keyword)
        engindex = []
        engkey = []
        cowlist = {}
        for i in keyword:
            engindex.append(a.index(i))
        print("engindex" ,engindex)
        for i in engindex:
            engkey.append(b[i])
        print("engkey" ,engkey)
        for i in range(len(keyword)):
            if nonumber:
                keywordnumber.append('0')
                cowlist[engkey[i]] = keywordnumber[i]
            else:
                cowlist[engkey[i]] = keywordnumber[i]
        if nonumber:
            datas=Classified.objects.filter(**cowlist)
            
        else:
            datas=Classified.objects.exclude(**cowlist)

        # datas=Classified.objects.filter(cat__gte=1,dog__gte=1)
        # datas=Classified.objects.filter(**cowlist)
    request.session['queryset'] = cowlist
    print(request.session['queryset'])
    now=datetime.datetime.now()
    return render(request,'select.html',locals())

def gallery(request):
    now=datetime.datetime.now()
    datas=Classified.objects.all()
    # return JsonResponse(datas,safe=False)
    return render(request,'gallery.html',locals())

def facerecognition(request):
    date=datetime.datetime.now()
    print('face begin')
    if request.method =='POST' and request.FILES['photoupload']:
        myfile=request.FILES['photoupload']
        print('myfile', myfile)
        fs = FileSystemStorage(location='home/static/images/')
        fs.save(myfile.name,myfile)
        forImport_recognize_faces_image.readPara("home/dlib/encoding3.pickle",f'home/static/images/{myfile.name}','cnn') 
        #f'home/static/images/{myfile.name}
        photopath="images/upload.jpg"
        
    title = "FACE RECOGNITION"
    now = datetime.datetime.now()
    return render(request,'layout.html',locals())


def styletransfer(request):
    date=datetime.datetime.now()  
    if request.method =='POST' and request.FILES['photoupload']:
        myfile=request.FILES['photoupload']
        fs = FileSystemStorage(location='home/static/images/')
        fs.save(myfile.name,myfile)
        # forImport_recognize_faces_image.readPara("home/dlib/encoding3.pickle",f'home/static/images/{myfile.name}','cnn')
        BeautyGAN.beauty(f'home/static/images/{myfile.name}')
        makeups = glob.glob(os.path.join('home','static','makeupstyle','*'))
        photopaths=[]
        for i in range(len(makeups)):
            photopaths.append(f"makeupstyle/{i+1}.jpg")
        print(photopaths)
        return redirect("/styletransfer2")

    title = "STYLE TRANSFER"
    now = datetime.datetime.now()
    return render(request,'layout.html',locals())
    
def styletransfer2(request):
    date=datetime.datetime.now()
    if request.method =='POST' and request.POST["style"]:
        beautysplit.split(request.POST["style"])
        makeups = glob.glob(os.path.join('home','static','makeupstyle','*'))
        photopath="./home/static/temp/split.jpg"
        # stylephoto=os.listdir("./home/static/makeupstyle")
        # print(stylephoto)
        title = "SELECT THE STYLE YOU LIKE!"
    # elif os.path('./home/static/temp/split.jpg'):
    #     os.remove('./home/static/temp/split.jpg')  
    
    now=datetime.datetime.now()
    return render(request,'styletransfer2.html',locals())  
        

def upload(request):
    date=datetime.datetime.now()
    if request.method =='POST' and request.FILES['photoupload']:
        myfile=request.FILES['photoupload']
        fs = FileSystemStorage(location='home/static/images/')
        fs.save(myfile.name,myfile)
        # print(f'home/static/images/{myfile.name}.jpg')
        # photopath="images/upload.jpg"
        path_head='home/static/'
        img_path=f'images/{myfile.name}'
        # YoloTest.evaluate(f'home/static/images/{myfile.name}')
        YoloTest.evaluate(path_head,img_path)
        # print(YoloTest.dlist)
        for item in YoloTest.dlist:
            print("========================================")
            print(item)
            print("========================================")
            sort =Classified.objects.create(**item)
            sort .save()
            # sort = Classified(**item) 
            # sort.save()
    title="UPLOAD"
    now=datetime.datetime.now()
    return render(request,'layout.html',locals())


def delmypic(request):
    now=datetime.datetime.now()
    return render(request,'delmypic.html',locals())

def json(request):
    # if request.method =='POST':
    datas={"name":"ford","age":"31"}
    now=datetime.datetime.now()
    return JsonResponse(datas,safe=False)


def httpget(request):
    # if request.method =='POST':
    name=request.GET["name"]
    age=request.GET["age"]

    now=datetime.datetime.now()
    return HttpResponse(f"HELLO {name},{age}")


def signup(request):
    # if request.method =='POST':
    name=request.GET["name"]
    age=request.GET["age"]

    now=datetime.datetime.now()
    return HttpResponse(f"HELLO {name},{age}")

def login(request):


    now=datetime.datetime.now()
    return HttpResponse(f"HELLO {name},{age}")