import chainer as ch
from chainer import dataset, datasets
import chainer.links as L

import os

import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt

import json

class HandDataset(dataset.DatasetMixin):
    def __init__(self, Handpaths, Labelpaths, root='.',dtype=None, guassian=False):
        super().__init__()
        self._image = Handpaths
        self._label = Labelpaths
        self._root = root
        self.dtype = dtype
        self.G = guassian

    def get_example(self, i):
        handpath = os.path.join(self._root, self._image[i])
        labelpath = os.path.join(self._root, self._label[i])
        f = Image.open(handpath)
        imagesample = np.asarray(f, dtype = self.dtype)
        imagesample = L.model.vision.vgg.prepare(imagesample)
        HMsample = self.generate_heatmap(labelpath)
        return imagesample, HMsample
    def generate_heatmap(self, labelpath):
        fingers = {'Thumb':0, 'IndexFinger':1, 'MiddleFinger':2, 'RingFinger':3, 'LittleFinger':4}
        label = {}
        with open(labelpath,'r') as f:
            label = json.load(f)
        heatmaps = np.zeros((5,56,56),dtype=np.float32)
        for finger, points in label.items():
            n = fingers[finger]
            for p in points:
                heatmaps[n,p[1] // 4,p[0] // 4] = 1
            if self.G:
                heatmaps[n,:,:] = cv2.GaussianBlur(heatmaps[n,:,:],(3,3),0)
                heatmaps[n,:,:] /= np.max(heatmaps[n,:,:])
        return heatmaps
    def __len__(self):
        return len(self._image)


def get_dataset(args=""):
    if args == "":
        datasize = 10
        RootPath = "../data/Hands_resize"
    else:
        datasize = args.datasize
        RootPath = args.data
        guassian = args.guassian
        
    Imagelist = ["Hand_%07d.jpg" % (i + 1) for i in range(datasize)]

    Labellist = ["Hand_%07d.txt" % (i + 1) for i in range(datasize)]

    Handloader = HandDataset(Imagelist, Labellist, RootPath, guassian=guassian)
    train, test = datasets.split_dataset_random(Handloader,int(datasize * .7))
    return train, test

if __name__ == '__main__':
    args = ""
    train, test = get_dataset("")
    print(len(train))
    print(len(test))
    hand, HM = train[0]
    plt.imshow(hand[0].transpose((1,2,0)))
    plt.show()
    for i in range(5):
        plt.imshow(HM[0,i,...], cmap='gray')
        plt.show()