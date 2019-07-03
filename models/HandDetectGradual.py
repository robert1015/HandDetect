import chainer as ch
from chainer import datasets
import chainer.functions as F
import chainer.links as L
from chainer import Variable
from chainer.links import VGG16Layers

import numpy as np



class HandDetectGradual(ch.Chain):

    def __init__(self):
        super(HandDetectGradual,self).__init__()
        with self.init_scope():
            self.featureNet = VGG16Layers()
            self.deconv1 = L.Deconvolution2D(512, 256, 4, stride=2, pad=1) #28*28*256
            self.rconv1_1 = L.Convolution2D(256, 256, 3, stride=1, pad=1)
            self.rconv1_2 = L.Convolution2D(256, 256, 3, stride=1, pad=1)
            self.deconv2 = L.Deconvolution2D(256, 128, 4, stride=2, pad=1) #56*56*128
            self.rconv2_1 = L.Convolution2D(128, 128, 3, stride=1, pad=1)
            self.rconv2_2 = L.Convolution2D(128, 128, 3, stride=1, pad=1)
            
            self.HMcov = L.Convolution2D(128, 5, 3, stride=1, pad=1) #56*56*5

    def image_to_map(self, im): #from image to heatmap stream
        h = F.relu(self.featureNet.forward(im,layers=['conv5_3'])['conv5_3'])
        h = F.relu(self.deconv1(h))
        h = F.relu(self.rconv1_1(h))
        h = F.relu(self.rconv1_2(h))
        h = F.relu(self.deconv2(h))
        h = F.relu(self.rconv2_1(h))
        h = F.relu(self.rconv2_2(h))
        return h
    def map_to_map(self, m): #from heatmap to get refined heatmap stream
#         print("map_to_map" + str(m.data.shape))
        h=m
        refineNet = self.featureNet.copy(mode='share')
        for i, layer in enumerate(refineNet.children()):
#             print(layer.W.shape)
            if i > 12:
                break
            if i >= 4:
#                 print(i)
                h = F.relu(layer(h))
            if i in [6,9]:
                h = F.max_pooling_2d(h,2,stride=2)
#         print(h.data.shape)
        h = F.relu(self.deconv1(h))
        h = F.relu(self.rconv1_1(h))
        h = F.relu(self.rconv1_2(h))
        h = F.relu(self.deconv2(h))
        h = F.relu(self.rconv2_1(h))
        h = F.relu(self.rconv2_2(h))
        return h
    def __call__(self, x):
        h = self.image_to_map(x)
        h = self.map_to_map(h)
        h = F.sigmoid(self.HMcov(h))
        return h

if __name__ == '__main__':
    a = VGG16Layers()
    for i in a.children():
        print(i.W.shape)