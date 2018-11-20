# python slide bar example
# python slidebar + histogram + image example

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider,QSizePolicy,QLabel)

from PyQt5.QtGui import QImage,QPixmap
import os
from skimage import io

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.curPath = os.path.dirname( os.path.abspath( __file__ ) )

        ### file path (revise this file path ) ###
        self.rotateImgPath = str(self.curPath) + '/data/rotateMorpImh.png'
        self.segmentedImgPath = str(self.curPath) + '/data/segmentedImg.png'

        ##########################################
        self.grid = QGridLayout()
        self.grid.addWidget(self.createHistogramGroup(), 0, 0)
        #self.createImageGroup(self.segmentedImgPath)
        self.grid.addWidget(self.createImageGroup(self.segmentedImgPath), 1, 0)
        self.grid.addWidget(self.createExampleGroup(), 0, 1)
        self.grid.addWidget(self.createExampleGroup(), 1, 1)
        self.setLayout(self.grid)

        self.setWindowTitle("PyQt5 Sliders")
        self.resize(400, 300)

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

    def createHistogramGroup(self):
    	tempImagePath = str(self.curPath)+ '/data/18.06.25/18_06_25_06.bmp'
    	tempForHisImg01 = io.imread(tempImagePath)
    	plotImg01 = PlotCanvas(tempForHisImg01)
    	return plotImg01

    def createImageGroup(self,filePath):
        label = QLabel(self)
        pixmap = QPixmap(filePath)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())

        return label
 

class PlotCanvas(FigureCanvas):
 
    def __init__(self,img,parent = None,width=3, height=2, dpi=100):
        #width=5; sheight=4; dpi=100; parent = None
        self.tempImg = img #get image (not path)
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout() # layout
        fig.subplots_adjust(0.2, 0.2, 0.8, 0.8) #plot size 
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)

        FigureCanvas.updateGeometry(self)

        self.plotImg(self.tempImg)

    def plotImg(self,img,dtype = 'float'): #plotting image. 
        if (dtype=='float') :
            ax = self.figure.add_subplot(111)
            ax.hist(img.ravel(),256,[img.min(),img.max()])
            #ax.set_title('Histogram for gray scale picture')
            #ax.xaxis.set_major_locator([0,1])
            self.draw()
            #plt.show()

        elif (dtype == 'int'):
            ax = self.figure.add_subplot(111)
            ax.hist(img.ravel(),256,[0,256])
            #ax.set_title('Histogram for gray scale picture')
           # ax.xaxis.set_major_locator([0,255])
            self.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    app.exec_()
    app.deleteLater()
    sys.exit()