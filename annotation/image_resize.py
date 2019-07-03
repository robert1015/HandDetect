import cv2 as cv
import random

i = 2
j = 1
sample = random.sample(range(10000),1200)
while(1):
	filename = "../data/Hands/Hand_000%04d" % (sample[i]) + ".jpg"
	ori = cv.imread(filename)
	if ori is None:
		i += 1
		continue
	new = cv.resize(ori,(224,224))
	cv.imwrite("../data/Hands_resize/Hand_000%04d" % (j) + ".jpg", new)
	i += 1
	j += 1
	if j == 1001:
		break
	