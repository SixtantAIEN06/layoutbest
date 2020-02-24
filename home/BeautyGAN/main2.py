# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import os
import glob
from imageio import imread, imsave
import cv2
import argparse
from PIL import Image
import dlib

rect2=''

def preprocess(img):
    return (img / 255. - 0.5) * 2

def deprocess(img):
    return (img + 1) / 2

def beauty(image):
    global rect2
    im=Image.open(image)
    image=im.convert('RGB')
    image.save('./home/static/temp/toRGB.jpg')
    org_h,org_w,_=imread('./home/static/temp/toRGB.jpg').shape
    
    predictor = dlib.shape_predictor("./home/BeautyGAN/shape_predictor_68_face_landmarks.dat")
    face_cascade = cv2.CascadeClassifier('./home/BeautyGAN/haarcascade_frontalface_default.xml')
# Read the input image
    img = cv2.imread('./home/static/temp/toRGB.jpg')
    img_before=img[:,:,::-1]
    imsave('./home/static/temp/before.jpg',img_before)
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    rects = face_cascade.detectMultiScale(gray, 1.1, 5)
    print("rects",rects)
    rect2=rects
    # Draw rectangle around the faces
    
    for (face_num,(x, y, w, h)) in enumerate(rects):
        img = cv2.imread('./home/static/temp/before.jpg')

        if x>(w//8):
            x_=x-w//8  
            w_=w+w//8*2
        else:
            x_=x
            w_=w

                                 #放大臉抓取範圍
        if y>(h//8):
            y_=y-h//8
            h_=h+h//8*2  
        else:
            y_=y
            h_=h

        rect=dlib.rectangle(x_,y_,x_+w_,y_+h_)

        dimface = np.matrix([[p.x, p.y] for p in predictor(img, rect).parts()])
        dimface2=np.array(dimface[:17])         #下巴17個點+眉毛左右各3
        for i in range(3):
            if x>(w//8) and y>(h//8):
                dimface[26-i]=dimface[26-i]-[-w_//8,w_//8]   #抓到眉毛以上
        for i in range(3):
            if x>(w//8) and y>(h//8):
                dimface[26-i]=dimface[19-i]-[w_//8,w_//8]
            dimface2=np.append(dimface2,dimface[19-i],0)

        face_mask_w=dimface2[np.argmax(dimface2,0)][0][0,0]-dimface2[np.argmin(dimface2,0)][0][0,0];
        face_mask_h=dimface2[np.argmax(dimface2,0)][0][1,1]-dimface2[np.argmin(dimface2,0)][0][1,1];
        face_mask_x=dimface2[np.argmin(dimface2,0)][0][0,0]
        face_mask_y=dimface2[np.argmin(dimface2,0)][0][1,1]
        center=(face_mask_x+face_mask_w//2 ,face_mask_y+face_mask_h//2)


        mask=np.zeros((org_h,org_w,3),dtype=np.uint8)
        cv2.fillPoly(mask,[dimface2],(255,255,255))
        # cv2.imwrite("./home/static/temp/mask.jpg",mask)

        im1 = img[y_:y_+h_,x_:x_+w_,::-1]


        # Display the output
        imsave(f'./home/static/temp/im{face_num}.jpg', im1)

        

        batch_size = 1
        img_size = 256
        no_makeup = cv2.resize(imread(f'./home/static/temp/im{face_num}.jpg'), (img_size, img_size))
        X_img = np.expand_dims(preprocess(no_makeup), 0)
        makeups = glob.glob(os.path.join('home','static','makeupstyle','*'))
        result = np.ones((img_size, (len(makeups) + 1) * img_size, 3))
        result[:img_size, :img_size] = no_makeup / 255.
        final=np.ones((org_h, (len(makeups) + 1) * org_w, 3))
        final[:org_h, :org_w] = img 

        tf.reset_default_graph()
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        saver = tf.train.import_meta_graph(os.path.join('home','BeautyGAN','model', 'model.meta'))
        saver.restore(sess, tf.train.latest_checkpoint('home/BeautyGAN/model'))

        graph = tf.get_default_graph()
        X = graph.get_tensor_by_name('X:0')
        Y = graph.get_tensor_by_name('Y:0')
        Xs = graph.get_tensor_by_name('generator/xs:0')

        for i in range(len(makeups)):
            makeup = cv2.resize(imread(f"home/static/makeupstyle/{i+1}.jpg"), (img_size, img_size))
            # print(makeups[i])
            Y_img = np.expand_dims(preprocess(makeup), 0)
            Xs_ = sess.run(Xs, feed_dict={X: X_img, Y: Y_img})
            Xs_ = deprocess(Xs_)
            final[:org_h,(i + 1) *org_w :(i + 2) *org_w] = img 
            

            # result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = makeup / 255.
            result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = Xs_[0]
            
        imsave('./home/static/temp/result_.jpg', result)
        result_ = cv2.resize(imread('./home/static/temp/result_.jpg'), (w_*(len(makeups) + 1) , h_))

        imsave('./home/static/temp/result_.jpg', result_)
        # result_=Image.open('result_.jpg')
        im_cut=[]
        final=final[:,:,::-1]
        if face_num==0:
            for i in range(len(makeups)):
                # print(i*w,0, (i+1)*w, h)
                final[y_:y_+h_ , x_+(i+1)*org_w : x_+w_+(i+1)*org_w]=result_[:h_,(i+1)*w_:(i+2)*w_]
            imsave('./home/static/temp/resultsq.jpg', final)
            for i in range(len(makeups)):
                src=cv2.imread('./home/static/temp/resultsq.jpg')
                src=src[:org_h,(i+1)*org_w : (i+2)*org_w]
                org=cv2.imread('./home/static/temp/before.jpg')
                output=cv2.seamlessClone(src, org, mask, center,  cv2.NORMAL_CLONE  )
                print(output.shape)
                final[:org_h,(i+1)*org_w : (i+2)*org_w]=output[:,:,::-1]
            imsave('./home/static/temp/result.jpg', final) 
            
        else:
            final=cv2.imread('./home/static/temp/result.jpg')[:,:,::-1]
            for i in range(len(makeups)):
                # print(i*w,0, (i+1)*w, h)
                final[y_:y_+h_ , x_+(i+1)*org_w : x_+w_+(i+1)*org_w]=result_[:h_,(i+1)*w_:(i+2)*w_]
            imsave('./home/static/temp/resultsq.jpg', final)  
            for i in range(len(makeups)):      
                src=cv2.imread('./home/static/temp/resultsq.jpg')
                src=src[:org_h,(i+1)*org_w : (i+2)*org_w]
                org=cv2.imread('./home/static/temp/result.jpg')
                org=org[:org_h,(i+1)*org_w : (i+2)*org_w]

                output=cv2.seamlessClone(src, org, mask, center,  cv2.NORMAL_CLONE  )
                print(output.shape)
                final[:org_h,(i+1)*org_w : (i+2)*org_w]=output[:,:,::-1]
            imsave('./home/static/temp/result.jpg', final) 

        os.remove(f'./home/static/temp/im{face_num}.jpg')


        # face_num+=1   
        os.remove('./home/static/temp/result_.jpg')
        os.remove('./home/static/temp/resultsq.jpg')

        # for i in range(len(makeups)):
        #     src=cv2.imread('./home/static/temp/result.jpg')[:org_h,(i+1)*org_w : (i+2)*org_w]
        #     org=cv2.imread('./home/static/temp/before.jpg')
        #     output=cv2.seamlessClone(src, org, mask, center,  cv2.NORMAL_CLONE  )
        #     final[:org_h,(i+1)*org_w : (i+2)*org_w]=output[:,:,::-1]
        #     imsave('./home/static/temp/result.jpg', final)        


    os.remove('./home/static/temp/toRGB.jpg')


