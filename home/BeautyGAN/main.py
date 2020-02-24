# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import os
import glob
from imageio import imread, imsave
from PIL import Image
import cv2
import argparse



def preprocess(img):
    return (img / 255. - 0.5) * 2

def deprocess(img):
    return (img + 1) / 2

def beauty(image):

    im = Image.open(image)
    image = im.convert('RGB')
    image.save('./home/static/temp/before.jpg')
    
    org_h,org_w,_=imread('./home/static/temp/before.jpg').shape


    batch_size = 1
    img_size = 256
    no_makeup = cv2.resize(imread('./home/static/temp/before.jpg'), (img_size, img_size))
    X_img = np.expand_dims(preprocess(no_makeup), 0)
    makeups = glob.glob(os.path.join('home','static','makeupstyle','*'))

    result = np.ones((img_size, (len(makeups) + 1) * img_size, 3))
    result[:img_size, :img_size] = no_makeup / 255.

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
        makeup = cv2.resize(imread(makeups[i]), (img_size, img_size))
        Y_img = np.expand_dims(preprocess(makeup), 0)
        Xs_ = sess.run(Xs, feed_dict={X: X_img, Y: Y_img})
        Xs_ = deprocess(Xs_)


        # result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = makeup / 255.
        result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = Xs_[0]

        
    imsave('./home/static/temp/result_.jpg', result)
    result2 = cv2.resize(imread('./home/static/temp/result_.jpg'), (org_w*(len(makeups) + 1) , org_h))
    imsave('./home/static/temp/result.jpg', result2)
    os.remove('./home/static/temp/result_.jpg')
    

# if __name__=="__main__":
#     beauty('./home/static/images/baby.jpg')