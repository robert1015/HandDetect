# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Annotation_tool.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Annotation_Tool(object):
    def setupUi(self, Annotation_Tool):
        Annotation_Tool.setObjectName("Annotation_Tool")
        Annotation_Tool.resize(704, 532)
        self.centralwidget = QtWidgets.QWidget(Annotation_Tool)
        self.centralwidget.setObjectName("centralwidget")
        self.ImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.ImageLabel.setGeometry(QtCore.QRect(0, 0, 500, 500))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageLabel.sizePolicy().hasHeightForWidth())
        self.ImageLabel.setSizePolicy(sizePolicy)
        self.ImageLabel.setText("")
        self.ImageLabel.setScaledContents(True)
        self.ImageLabel.setObjectName("ImageLabel")
        self.SelectBox = QtWidgets.QGroupBox(self.centralwidget)
        self.SelectBox.setGeometry(QtCore.QRect(560, 50, 120, 281))
        self.SelectBox.setTitle("")
        self.SelectBox.setObjectName("SelectBox")
        self.Finger_1 = QtWidgets.QRadioButton(self.SelectBox)
        self.Finger_1.setGeometry(QtCore.QRect(10, 30, 112, 23))
        self.Finger_1.setStyleSheet("color: rgb(239, 41, 41);")
        self.Finger_1.setObjectName("Finger_1")
        self.Finger_2 = QtWidgets.QRadioButton(self.SelectBox)
        self.Finger_2.setGeometry(QtCore.QRect(10, 60, 112, 23))
        self.Finger_2.setStyleSheet("color: rgb(143, 89, 2);")
        self.Finger_2.setObjectName("Finger_2")
        self.Finger_3 = QtWidgets.QRadioButton(self.SelectBox)
        self.Finger_3.setGeometry(QtCore.QRect(10, 90, 112, 23))
        self.Finger_3.setStyleSheet("color: rgb(78, 154, 6);")
        self.Finger_3.setObjectName("Finger_3")
        self.Finger_4 = QtWidgets.QRadioButton(self.SelectBox)
        self.Finger_4.setGeometry(QtCore.QRect(10, 120, 112, 23))
        self.Finger_4.setStyleSheet("color: rgb(32, 74, 135);")
        self.Finger_4.setObjectName("Finger_4")
        self.Finger_5 = QtWidgets.QRadioButton(self.SelectBox)
        self.Finger_5.setGeometry(QtCore.QRect(10, 150, 112, 23))
        self.Finger_5.setObjectName("Finger_5")
        self.CurrentImageName = QtWidgets.QLabel(self.centralwidget)
        self.CurrentImageName.setGeometry(QtCore.QRect(566, 390, 131, 20))
        self.CurrentImageName.setObjectName("CurrentImageName")
        Annotation_Tool.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Annotation_Tool)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 704, 28))
        self.menubar.setObjectName("menubar")
        Annotation_Tool.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Annotation_Tool)
        self.statusbar.setObjectName("statusbar")
        Annotation_Tool.setStatusBar(self.statusbar)

        self.retranslateUi(Annotation_Tool)
        QtCore.QMetaObject.connectSlotsByName(Annotation_Tool)

    def retranslateUi(self, Annotation_Tool):
        _translate = QtCore.QCoreApplication.translate
        Annotation_Tool.setWindowTitle(_translate("Annotation_Tool", "Annotation Tool"))
        self.Finger_1.setText(_translate("Annotation_Tool", "Thumb"))
        self.Finger_2.setText(_translate("Annotation_Tool", "Index Finger"))
        self.Finger_3.setText(_translate("Annotation_Tool", "MiddleFinger"))
        self.Finger_4.setText(_translate("Annotation_Tool", "Ring Finger"))
        self.Finger_5.setText(_translate("Annotation_Tool", "Little Finger"))
        self.CurrentImageName.setText(_translate("Annotation_Tool", "No Image"))


