from PIL import Image
import os
import glob
import argparse
import numpy as np
import time

# parser = argparse.ArgumentParser()
# parser.add_argument('--type_num', type=int, default=0, help='type_num')
# args = parser.parse_args()


def split(type_):
    type_num=int(type_.strip('style'))
    im=Image.open('./home/static/temp/result.jpg')
    makeups = glob.glob(os.path.join('home','static','makeupstyle','*'))
    num=len(makeups)+1
    img_w=int(im.size[0]/num)
    img_h=int(im.size[1])
    im1 = im.crop((type_num*img_w,0, (type_num+1)*img_w, img_h)) 
    # im1.show()


    #wait click ok

    im1.save('./home/static/temp/split.jpg') 

