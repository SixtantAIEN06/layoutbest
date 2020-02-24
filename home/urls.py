from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('search/',views.search),
    path('styletransfer/',views.styletransfer),
    path('styletransfer2/',views.styletransfer2),
    path('delmypic/',views.delmypic,name='uplaodfile'),
    # path('styletransfer/{imgpath:imgpath}',views.styletransfer),
    path('json/',views.json),
    path('upload/',views.upload),
    path('facerecognition/',views.facerecognition),
    path('styletransfer/json/',views.json),
    path('styletransfer/httpget/',views.httpget),
    path('selected/',views.selected),
    path('login/',views.login),
    path('logout/',views.logout),
    path('signup/',views.signup),
    path('json/',views.json),
    path('httpget/',views.httpget),
    path('tryaudio/',views.tryaudio),


]
