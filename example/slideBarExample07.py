import sys
import cv2
import numpy as np
import PIL
import os
from matplotlib import pyplot as plt

from scipy import ndimage
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot , Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QDialog,QLineEdit, QApplication, QFileDialog,QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider,QSizePolicy,QLabel)
from skimage import io

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Window(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1082, 622)
        self.curPath = os.path.dirname( os.path.abspath( __file__ ) )

        ### file path (revise this file path ) ###
        self.rotateImgPath = str(self.curPath) + '/data/rotateMorpImh.png'
        self.segmentedImgPath = str(self.curPath) + '/data/segmentedImg.png'

        ####

        self.tab_7 = QWidget()
        self.tab_7.setObjectName("tab_7")

        self.histogramLocalUpperThresholdBox = QLineEdit(self.tab_7)
        self.histogramLocalUpperThresholdBox.setGeometry(QtCore.QRect(620, 30, 31, 21))
        self.histogramLocalUpperThresholdBox.setObjectName("histogramLocalUpperThresholdBox")

        self.hSlider_histogramLocalUpperThreshold = QSlider(self.tab_7)
        self.hSlider_histogramLocalUpperThreshold.setGeometry(QtCore.QRect(620, 50, 401, 19))
        self.hSlider_histogramLocalUpperThreshold.setMaximum(255)
        self.hSlider_histogramLocalUpperThreshold.setProperty("value", 120)
        self.hSlider_histogramLocalUpperThreshold.setOrientation(QtCore.Qt.Horizontal)
        self.hSlider_histogramLocalUpperThreshold.setObjectName("hSlider_histogramLocalUpperThreshold")
        self.hSlider_histogramLocalLowerThreshold = QSlider(self.tab_7)
        self.hSlider_histogramLocalLowerThreshold.setGeometry(QtCore.QRect(190, 50, 401, 19))
        self.hSlider_histogramLocalLowerThreshold.setMaximum(255)
        self.hSlider_histogramLocalLowerThreshold.setProperty("value", 120)
        self.hSlider_histogramLocalLowerThreshold.setOrientation(QtCore.Qt.Horizontal)
        self.hSlider_histogramLocalLowerThreshold.setObjectName("hSlider_histogramLocalLowerThreshold")

        ##########################################

    def createExampleGroup(self):

        groupBox = QGroupBox("Slider Example")

        radio1 = QRadioButton("&Radio horizontal slider")

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(10)
        slider.setSingleStep(1)

        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(slider)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox


    def createImageGroup(self,filePath):
        label = QLabel(self)
        pixmap = QPixmap(filePath)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())

        return label

    def getHistogramLocalUpperThresholdSliderValue(self):
        return int(self.hSlider_histogramLocalUpperThreshold.value())

    def getHistogramLocalLowerThresholdSliderValue(self):
        return int(self.hSlider_histogramLocalLowerThreshold.value())

    def getHistogramLocalLowerThresholdValue(self):
        return int(self.histogramLocalLowerThresholdBox.text())

    def getHistogramLocalUpperThresholdValue(self):
        return int(self.histogramLocalUpperThresholdBox.text())

    @pyqtSlot()
    def histogramLocalThresholdClicked(self):
        # hSlider_histogramGlobalLowerThreshold = slider
        self.hSlider_histogramGlobalLowerThreshold.setValue(self.getHistogramLocalLowerThresholdValue())
        self.histogramLocalUpperThresholdBox.setText(str(255))
        self.hSlider_histogramGlobalUpperThreshold.setValue(self.getHistogramLocalUpperThresholdValue())
        self.histogramLocalLowerThresholdBox.setText(str(120))
        if self.imageLoaded:
            image_tmp = self.image.copy()
            image_tmp = cv2.medianBlur(image_tmp, 5)
            image_tmp = cv2.cvtColor(image_tmp, cv2.COLOR_RGB2GRAY)
            ret, image_tmp = cv2.threshold(image_tmp, 127, 255, cv2.THRESH_BINARY)
            image_tmp = cv2.adaptiveThreshold(image_tmp, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            self.processedImage = image_tmp
            self.displayImage(2)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Window()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())