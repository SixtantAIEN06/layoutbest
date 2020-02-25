from PIL import Image
import os
import glob
import argparse
import numpy as np
import time
import random, string
# from ..object_detection.evaluate import YoloTest
# from ..dlib import recognize_faces_image
# from ..models import Classified,Members

# YoloTest = YoloTest()

# parser = argparse.ArgumentParser()
# parser.add_argument('--type_num', type=int, default=0, help='type_num')
# args = parser.parse_args()


def split(type_,user_id):
    type_num=int(type_.strip('style'))
    if type_num==999:
        print("ok")
        # im=Image.open('./home/static/temp/split.jpg')

        # picname=''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        # im.save(f'./home/static/images/{picname}.jpg') 
        # path_head='home/static/'
        # img_path=f'images/{picname}.jpg'
        # # YoloTest.evaluate(f'home/static/images/{myfile.name}')
        # YoloTest.evaluate(path_head,img_path)

        # a=recognize_faces_image.readPara("home/dlib/encoding/encoding_all_nj1_300p.pickle",f'home/static/images/{picname}.jpg','hog',0.45)
        # a=dict(a)
        # print("a",a)
        # id={}
        # id["image_owner"]=user_id
        # a.update(id)
        # dataset=[]
        # for i in YoloTest.dlist:
        #     i.update(a)
        #     dataset.append(i)
        # print("dataset",dataset)
        
        # # print("a+list",dict(YoloTest.dlist))
        # for item in YoloTest.dlist:
        #     print("========================================")
        #     print(item)
        #     print("========================================")
            
        #     sort =Classified.objects.create(**item)
        #     sort .save()
    else:
        im=Image.open('./home/static/temp/result.jpg')
        makeups = glob.glob(os.path.join('home','static','makeupstyle','*'))
        num=len(makeups)+1
        img_w=int(im.size[0]/num)
        img_h=int(im.size[1])
        im1 = im.crop((type_num*img_w,0, (type_num+1)*img_w, img_h)) 

        im1.save('./home/static/temp/split.jpg') 

