import sys
import os.path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from Ui_Annotation_tool import Ui_Annotation_Tool

import json

import cv2

class Annotation_tool(QMainWindow, Ui_Annotation_Tool):
	def __init__(self, Parent=None):
		super().__init__(Parent)
		self.setupUi(self)
		self.loader = PictureLoader()
	def keyPressEvent(self,e):
		if e.key() == Qt.Key_N:
			#save automatically
			with open(self.loader.path[:-4] + '.txt','w+') as f:
				json.dump(self.loader.keypoints,f)
			self.loader.index += 1
			self.loader.LoadImage()
			self.ShowImage(self.loader)
			self.loader.keypoints={}
		elif e.key() == Qt.Key_R:
			self.loader.LoadImage()
			self.ShowImage(self.loader)
			self.loader.keypoints={}
			
		elif e.key() == Qt.Key_S:
			with open(self.loader.path[:-4] + '.txt','w+') as f:
				json.dump(self.loader.keypoints,f)

		elif e.key() == Qt.Key_Tab:
			for i in range(5):
				if getattr(self,"Finger_"+str(i+1)).isChecked():
					getattr(self, "Finger_" + str(i+2 if i != 4 else 1)).setChecked(True)
					break
	def mousePressEvent(self, ev):
		size = self.loader.image.shape[0]
		co = list(map(int, [ev.pos().x() / 500 * size, ev.pos().y() / 500 * size]))
		if self.Finger_1.isChecked():
			color = [239,41,41]
			finger = "Thumb"
		elif self.Finger_2.isChecked():
			color = [143,89,2]
			finger = "IndexFinger"
		elif self.Finger_3.isChecked():
			color = [78,154,6]
			finger = "MiddleFinger"
		elif self.Finger_4.isChecked():
			color = [32,74,135]
			finger = "RingFinger"
		elif self.Finger_5.isChecked():
			color = [0,0,0]
			finger = "LittleFinger"
		else:
			return
		self.loader.drawPoint(co, color)
		self.loader.UpdatePoint(co,finger)
		self.ShowImage(self.loader)
	def closeEvent(self,e):
		print("closing")
		with open("checkpoint.txt",'w+') as f:
			f.write("%d" % self.loader.index)

	def ShowImage(self, loader):
		h,w,c = loader.image.shape
		bpl = 3 * w
		pic = QImage(loader.image.data, w, h, bpl, QImage.Format_RGB888).rgbSwapped()
		self.ImageLabel.setPixmap(QPixmap(pic))
		self.CurrentImageName.setText(loader.path.split('/')[-1])


class PictureLoader:
	def __init__(self):
		try:
			with open("checkpoint.txt",'r') as f:
				self.index = int(f.readline())
		except:
			with open("checkpoint.txt",'w+') as f:
				f.write("0\n")
				self.index = 0
		self.path = ""
		self.keypoints = {}
		self.image = None
	def LoadImage(self):
		self.path = "../data/Hands_resize/Hand_0000%03d" % (self.index) + ".jpg"
		self.image = cv2.imread(self.path)
	def drawPoint(self, coordinate, color):
		x,y = coordinate[1],coordinate[0]
		self.image[x-1:x+2,y-1:y+2,:]=color[::-1]
	def UpdatePoint(self, co,finger):
		if finger not in self.keypoints:
			self.keypoints[finger]=[co]

		else:
			self.keypoints[finger].append(co)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Annotation_tool()
	window.show()
	sys.exit(app.exec_())