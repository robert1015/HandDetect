import chainer as ch
from chainer import dataset, datasets
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions

import os

import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy

class HandDataset(dataset.DatasetMixin):
	def __init__(self, handpaths, HMpaths, root='.',dtype=None):
		super().__init__()
		self._handpaths = handpaths
		self._HMpaths = HMpaths
		self._root = root
		self.dtype = dtype

	def get_example(self, i):
		handpath = os.path.join(self._root, self._handpaths[i])
		f = Image.open(handpath)
		imagesample = numpy.asarray(f, dtype = self.dtype)
		HMsample = np.zeros((5,56,56))
		for j in range(5):
			HMpath = os.path.join(self._root, self._HMpaths[i][j])
			f = Image.open(HMpath)
			HMsample[j,...] = numpy.asarray(f, dtype = self.dtype)[None,...]
		return imagesample.transpose([2,0,1]), HMsample
	def __len__(self):
		return len(self._handpaths)


def get_dataset(args):
	# datasize = args.datasize
	datasize = 10
	# RootPath = args.root
	RootPath = "../data/"
	Imagelist = ["Hands_resize/Hand_%07d.jpg" % (i + 1) for i in range(datasize)]

	# HMPath = args.HMPath
	HMlist = [["Heat_map/Hand_%07d_%d.jpg" % (i + 1,j) for j in range(5)] for i in range(datasize)]

	Handloader = HandDataset(Imagelist, HMlist, RootPath)
	train, test = datasets.split_dataset_random(Handloader,int(datasize * .7))
	return train, test

# if __name__ == '__main__':
# 	args = ""
# 	train, test = get_dataset(args)
# 	print(len(train))
# 	print(len(test))
