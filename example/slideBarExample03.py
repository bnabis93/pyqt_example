# python slide bar example
# python slidebar + histogram + image example
# slide value change and image.

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,QSpinBox, QHBoxLayout,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider,QSizePolicy,QLabel)

from PyQt5.QtGui import QImage,QPixmap
import os
from skimage import io

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

MAXVAL = 10000


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


        #self.layout = QtWidgets.QHBoxLayout(self)
        self.slider1 = CustomSlider()
        self.slider2 = CustomSlider()
        self.grid.addWidget(self.slider1, 0, 1)
        self.grid.addWidget(self.slider2, 1, 1)
        self.setLayout(self.grid)

        self.setWindowTitle("PyQt5 Sliders")
        self.resize(400, 300)

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
 
class CustomSlider(QWidget):
    def __init__(self, *args, **kwargs):
        super(CustomSlider, self).__init__(*args, **kwargs)

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.valueChanged.connect(self.handleSliderValueChange)
        #value change(parameter = function)
        self.numbox = QSpinBox()
        self.numbox.valueChanged.connect(self.handleNumboxValueChange)

        self.slider.setMaximum(MAXVAL)
        self.numbox.setMaximum(MAXVAL)

        layout = QHBoxLayout(self)
        layout.addWidget(self.numbox)
        layout.addWidget(self.slider)

    @QtCore.pyqtSlot(int)
    def handleSliderValueChange(self, value):
        self.numbox.setValue(value)
        print("slider value : ",value)

    @QtCore.pyqtSlot(int)
    def handleNumboxValueChange(self, value):
        # Prevent values outside slider range
        if value < self.slider.minimum():
            self.numbox.setValue(self.slider.minimum())
        elif value > self.slider.maximum():
            self.numbox.setValue(self.slider.maximum())

        self.slider.setValue(self.numbox.value())


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