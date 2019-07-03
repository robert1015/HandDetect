import chainer as ch
from chainer import datasets
import chainer.functions as F
import chainer.links as L
from chainer import Variable
from chainer.links import VGG16Layers

import numpy as np



class HandDetect(VGG16Layers):

    def __init__(self):
        super(HandDetect,self).__init__()
        with self.init_scope():
            self.deconv1 = L.Deconvolution2D(512, 256, 4, stride=2, pad=1) #28*28*256
            self.rconv1_1 = L.Convolution2D(256, 256, 3, stride=1, pad=1)
            self.rconv1_2 = L.Convolution2D(256, 256, 3, stride=1, pad=1)
            self.deconv2 = L.Deconvolution2D(256, 128, 4, stride=2, pad=1) #56*56*128
            self.rconv2_1 = L.Convolution2D(128, 128, 3, stride=1, pad=1)
            self.rconv2_2 = L.Convolution2D(128, 128, 3, stride=1, pad=1)
            self.HMcov = L.Convolution2D(128, 5, 3, stride=1, pad=1) #56*56*5


    def __call__(self, x):
        h = F.relu(self.forward(x,layers=['conv5_3'])['conv5_3'])
        h = F.relu(self.deconv1(h))
        h = F.relu(self.rconv1_1(h))
        h = F.relu(self.rconv1_2(h))
        h = F.relu(self.deconv2(h))
        h = F.relu(self.rconv2_1(h))
        h = F.relu(self.rconv2_2(h))
        h = F.sigmoid(self.HMcov(h))
        return h
