from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.files.storage import FileSystemStorage
from .dlib import recognize_faces_image
# from .dlib import forImport_recognize_faces_image
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
    luis=request.GET.get("luis")
    print("luis = ",luis)
    response = requests.get(
    url=f'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/47fdbcf4-00cb-4e9a-a55c-df61cef1a102?verbose=true&timezoneOffset=0&subscription-key=7e25519a1e41462e8561a0bd60f5ddc2&q={luis}')
    print("response.text = ",response.text)
    luisdata = jjj.loads(response.text)
    data = []
    nonumbercheck3 = []
    datas = Classified.objects.all()
    for d in datas:
        data.append(d.image_path)
    data3 = data
    if 'topScoringIntent' in luisdata:
        intent = luisdata['topScoringIntent']['intent']
        keyword = []
        keywordnumber = []
        if len(luisdata['entities']) != 0:
            for i in range(len(luisdata['entities'])):
                if 'resolution' not in (luisdata['entities'][i]):
                    # keyword.append(luisdata['entities'][i]['entity'])
                    keyword.append(luisdata['entities'][i]['type'])
                if 'resolution' in (luisdata['entities'][i]):
                    keywordnumber.append(luisdata['entities'][i]['resolution']['value'])
            if len(keyword) != 0:
                if len(keywordnumber) == 0:
                    nonumber = True
                else:
                    nonumber = False
                a = []
                b = []
                with open('home/object_detection/data/classes/222.txt','r') as f :
                    for i in f.readlines():
                      
                        a.append(i.replace('\n',''))
                with open('home/object_detection/data/classes/coco_2.names','r') as f :
                    for i in f.readlines():
                        b.append(i.replace('\n',''))
                print("keyword" ,keyword)
                engindex = []
                engkey = []
                cowlist = {}
                for i in keyword:
                    if i in a:
                        engindex.append(a.index(i))
                        print("engindex" ,engindex)
                    else:
                        print("重新輸入")
                        errormassage = "沒有該項目，請重新搜尋"
                        if 'queryset' in request.session:
                            output_imagepath = request.session['queryset']
                        else:
                            output_imagepath = data
                        return render(request,'select.html',locals())

                for i in engindex:
                    engkey.append(b[i])
                print("engkey" ,engkey)
                for i in range(len(keyword)):
                    if nonumber:
                        keywordnumber.append('0')
                        cowlist[engkey[i]] = keywordnumber[i]
                    else:
                        cowlist[engkey[i]] = keywordnumber[i]
                    cowlist2 = {}
                    cowlist2[engkey[i]] = keywordnumber[i]
                    print(cowlist2)
                    nonumbercheck = Classified.objects.filter(**cowlist2)
                    print(nonumbercheck)
                    nonumbercheck2 = []
                    for i in nonumbercheck:
                        nonumbercheck2.append(i.image_path)
                        print(nonumbercheck2)
                    nonumbercheck3 = list(set(nonumbercheck2 + nonumbercheck3))
                    print("nonumbercheck3 = ",nonumbercheck3)
                    
                if nonumber:
                    nonumbercheck3 = list(set(data3) - set(nonumbercheck3))
                    if 'queryset' in request.session:
                        if intent == "正面":
                            output_imagepath = list(set(request.session['queryset']) & set(nonumbercheck3)) 
                        elif intent == "負面":
                            output_imagepath = list(set(request.session['queryset']) - set(nonumbercheck3))                          
                    else:
                        if intent == "正面":
                            output_imagepath = nonumbercheck3
                        elif intent == "負面":
                            output_imagepath = list(set(data3) - set(nonumbercheck3))
                    if len(output_imagepath) == 0:
                        errormassage = "沒有該項目，請重新搜尋"
                        if 'queryset' in request.session:
                            output_imagepath = request.session['queryset']
                        else:
                            output_imagepath = data3
                        return render(request,'select.html',locals())
                    else:
                        request.session['queryset'] = output_imagepath
                        return render(request,'select.html',locals())

                else:
                    if intent == "正面":
                        datas=Classified.objects.filter(**cowlist)
                    elif intent == "負面":
                        datas=Classified.objects.exclude(**cowlist)

                # if intent == "正面":
                #     if nonumber:
                #         datas = Classified.objects.filter(**cowlist)
                #         datas2 = Classified.objects.exclude(**cowlist)
                #     else:
                #         datas=Classified.objects.filter(**cowlist)
                # elif intent == "負面":
                #     if nonumber:
                #         datas = Classified.objects.filter(**cowlist)
                #         datas2 = Classified.objects.exclude(**cowlist)
                #     else:
                #         datas = Classified.objects.exclude(**cowlist)

                data = []
                output_imagepath = []
                for d in datas:
                    data.append(d.image_path)
                    # print("data" , data)
                    # print("data",type(data))
                
                if 'queryset' in request.session:
                    data2 = request.session['queryset']
                    # print("data2",type(data2))
                    output_imagepath = list(set(data) & set(data2))
                else:
                    output_imagepath = data
                if len(output_imagepath) == 0:
                    # datas = Classified.objects.all()
                    # for d in datas:
                    #     data.append(d.image_path)
                    errormassage = "沒有該項目，請重新搜尋"
                    if 'queryset' in request.session:
                        output_imagepath = request.session['queryset']
                        print("request.session['queryset']",request.session['queryset'])
                    else:
                        output_imagepath = data3
                    return render(request,'select.html',locals())

                else:
                    request.session['queryset'] = output_imagepath
                    print("request.session['queryset']",request.session['queryset'])
                now=datetime.datetime.now()
                return render(request,'select.html',locals())
            else:
                print("重新輸入")
                errormassage = "沒有該項目，請重新搜尋"
                if 'queryset' in request.session:
                    output_imagepath = request.session['queryset']
                else:
                    output_imagepath = data
                return render(request,'select.html',locals())
        else:
            print("重新輸入")
            errormassage = "沒有該項目，請重新搜尋"
            if 'queryset' in request.session:
                output_imagepath = request.session['queryset']
            else:
                output_imagepath = data
            return render(request,'select.html',locals())
    else:
        print("重新輸入")
        errormassage = "沒有該項目，請重新搜尋"
        if 'queryset' in request.session:
            output_imagepath = request.session['queryset']
        else:
            output_imagepath = data
        return render(request,'select.html',locals())

    

def gallery(request):
    now=datetime.datetime.now()
    datas=Classified.objects.all()
    try:
        del request.session['queryset']
    except:
        print('no session queryset')
    # return JsonResponse(datas,safe=False)
    # if 'queryset' not in request.session:
    #     print("cowlist2","None")
    # elif 'queryset' in request.session:
    #     print("cowlist2","YES")

    return render(request,'gallery.html',locals())

def facerecognition(request):
    date=datetime.datetime.now()
    print('face begin')
    if request.method =='POST' and request.FILES['photoupload']:
        myfile=request.FILES['photoupload']
        print('myfile', myfile)
        fs = FileSystemStorage(location='home/static/images/')
        fs.save(myfile.name,myfile)
        a=recognize_faces_image.readPara("home/dlib/encoding/encoding_all_nj1_300p.pickle",f'home/static/images/{myfile.name}','hog',0.45)
        
        # forImport_recognize_faces_image.readPara("home/dlib/encoding3.pickle",f'home/static/images/{myfile.name}','cnn') 
        #f'home/static/images/{myfile.name}
        photopath="images/upload.jpg"
        
    title = "FACE RECOGNITION"
    now = datetime.datetime.now()
    return render(request,'layout.html',locals())


def styletransfer(request):
     
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
        #print('rect2',BeautyGAN.rect2)
        if list(BeautyGAN.rect2):
            return redirect("/styletransfer2")
        else:
            message="請放入人臉的照片"
            return render(request,'layout.html',locals())

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

        a=recognize_faces_image.readPara("home/dlib/encoding/encoding_all_nj1_300p.pickle",f'home/static/images/{myfile.name}','hog',0.45)
        a=dict(a)
        print("a",a)

        dataset=[]
        for i in YoloTest.dlist:
            i.update(a)
            dataset.append(i)
        print("dataset",dataset)
       
        # print("a+list",dict(YoloTest.dlist))
        
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
    

    now=datetime.datetime.now()
    return render(request,'signup.html')

def login(request):


    now=datetime.datetime.now()
    return render(request,'login.html')


def tryaudio(request):
    return render(request,'tryaudioandcam.html')