import argparse
import os

from chainer import serializers
import chainer.links as L
from chainer.backends import cuda

import models.HandDetect as HandDetect

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def predict():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default='hand.model')
    parser.add_argument('--data', type=str, default='data/Hands_resize/')
    args = parser.parse_args()
    
    model = HandDetect.HandDetect()
    serializers.load_npz(args.model_path,model)
    #model = model.to_gpu(device=0)
    print("Model loaded.")
    while True:
        i = int(input())
        if i <= 0:
            break
        imagepath = args.data + "Hand_%07d.jpg" %(i)
        f = Image.open(imagepath)
        image = np.asarray(f,dtype=np.float32)
        x = L.model.vision.vgg.prepare(image)
        x =image.reshape((1,3,224,224))
        #x = cuda.to_gpu(x,device=0)
        heatmap = model(x)
        heatmap = heatmap.data
        #heatmap = cuda.to_cpu(heatmap)
        plt.figure()
        plt.imshow(image / 255)
        plt.figure()
        print(np.max(heatmap[0,0,...]))
        plt.imshow(heatmap[0,0,...],cmap='gray')
        plt.show()

        
if __name__ == "__main__":
    predict()
        
    