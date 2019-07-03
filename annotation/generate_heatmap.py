import numpy as np
import cv2
import json

start, end = 0, 10

fingers = {'Thumb':0, 'IndexFinger':1, 'MiddleFinger':2, 'RingFinger':3, 'LittleFinger':4}

for i in range(start, end):
	i += 1
	filename = "../data/Hands_resize/Hand_000%04d" % (i) + ".txt"
	label = {}
	with open(filename,'r') as f:
		label = json.load(f)
	heatmaps = np.zeros((56,56,5))
	for finger, points in label.items():
		for p in points:
			heatmaps[p[1] // 4,p[0] // 4,fingers[finger]] = 1
		heatmaps[:,:,fingers[finger]] = cv2.GaussianBlur(heatmaps[:,:,fingers[finger]],(5,5),0)
		heatmaps[:,:,fingers[finger]] /= np.max(heatmaps[:,:,fingers[finger]])
		cv2.imwrite("../data/Heat_map/Hand_000%04d_%d.jpg" % (i, fingers[finger]), heatmaps[:,:,fingers[finger]] * 255)
		#cv2.imshow("a",heatmaps[:,:,fingers[finger]])
		#cv2.waitKey(0)
