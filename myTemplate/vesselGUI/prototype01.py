# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
#
# My first prototype for vessel analysis.
#
# _developer : qhsh9713@gmail.com


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QWidget,QLabel, QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QPushButton

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage,QPixmap

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
import vesselAlgorithm
from vesselAlgorithm import rotateMorphSeg
from vesselAlgorithm import interval_mapping
from skimage import io
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
import os


import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import cv2
from skimage.filters import threshold_otsu
from skimage import filters
from skimage import morphology


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,MainWindow):
        super(Ui_MainWindow,self).__init__()

        self.curPath = os.path.dirname( os.path.abspath( __file__ ) )
        self.oriImgPath = None
        self.oriImgName = None
        self.prevImg = None

        self.oriImg = None
        self.claheImg = None
        self.rotateMorImg = None
        self.preSegImg =None
        self.segmentedImg = None
        self.vesselDataArray = []
        self.segmentAlgorithm = None

        self.segWidget = None

        self.otsuValue = None



        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.setupUi(MainWindow)


    def setupUi(self, MainWindow):

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")     

        # pushButton = "Analysis button"
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 130, 114, 32))
        self.pushButton.setObjectName("pushButton")     
        self.pushButton.clicked.connect(self.pushAnalysisButtonClicked)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 157, 114, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.pushParamButtonClicked)


        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(279, 29, 491, 491))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")   
        #gridLayoutWidget2 = img viewer
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.gridLayoutWidget_2)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.gridLayout_2.addWidget(self.graphicsView_3, 0, 1, 1, 1)

        self.graphicsView = QtWidgets.QGraphicsView(self.gridLayoutWidget_2)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 1, 1, 1, 1)

        self.graphicsView_2 = QtWidgets.QGraphicsView(self.gridLayoutWidget_2)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.gridLayout_2.addWidget(self.graphicsView_2, 0, 0, 1, 1)

        self.graphicsView_4 = QtWidgets.QGraphicsView(self.gridLayoutWidget_2)
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.gridLayout_2.addWidget(self.graphicsView_4, 1, 0, 1, 1)


        # histogram grid
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(20, 330, 231, 191))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.graphicsView_6 = QtWidgets.QGraphicsView(self.gridLayoutWidget_3)
        self.graphicsView_6.setObjectName("graphicsView_6")
        self.gridLayout_3.addWidget(self.graphicsView_6, 0, 1, 1, 1)
        self.graphicsView_5 = QtWidgets.QGraphicsView(self.gridLayoutWidget_3)
        self.graphicsView_5.setObjectName("graphicsView_5")
        self.gridLayout_3.addWidget(self.graphicsView_5, 0, 0, 1, 1)
        self.graphicsView_7 = QtWidgets.QGraphicsView(self.gridLayoutWidget_3)
        self.graphicsView_7.setObjectName("graphicsView_7")
        self.gridLayout_3.addWidget(self.graphicsView_7, 1, 0, 1, 1)
        self.graphicsView_8 = QtWidgets.QGraphicsView(self.gridLayoutWidget_3)
        self.graphicsView_8.setObjectName("graphicsView_8")

        self.gridLayout_3.addWidget(self.graphicsView_8, 1, 1, 1, 1)
       

        ################ List view ##################
        #data manager 
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(20, 30, 230, 90))
        self.listView.setObjectName("listView")

        #parameter
        self.listView_2 = QtWidgets.QListView(self.centralwidget)
        self.listView_2.setGeometry(QtCore.QRect(20, 210, 230, 90))
        self.listView_2.setObjectName("listView_2")

        #############################################

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(86, 10, 101, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(87, 312, 101, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        #pushButton_2 = "Data Loader" , signal (file dialog)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(17, 130, 114, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.pushDataButtonClicked)

        self.toolButton_3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_3.setGeometry(QtCore.QRect(90, 160, 34, 23))
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_4 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_4.setGeometry(QtCore.QRect(30, 160, 54, 23))
        self.toolButton_4.setObjectName("toolButton_4")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(88, 190, 101, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        #################### slide Bar ####################

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(570, 500, 160, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.slider1 = CustomSlider()
        #self.slider2 = CustomSlider()

        #self.horizontalSlider = QtWidgets.QSlider(self.gridLayoutWidget)
        #self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        #self.horizontalSlider.setObjectName("horizontalSlider")
        #self.horizontalSlider_2 = QtWidgets.QSlider(self.gridLayoutWidget)
        #self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        #self.horizontalSlider_2.setObjectName("horizontalSlider_2")

        self.gridLayout.addWidget(self.slider1, 2, 0, 1, 1)
        #self.gridLayout.addWidget(self.slider2, 1, 0, 1, 1)

        ###################################################


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        # status bar 
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vessel GUI"))
        self.pushButton.setText(_translate("MainWindow", "Segmentation"))
        self.pushButton_2.setText(_translate("MainWindow", "Data load"))
        self.pushButton_3.setText(_translate("MainWindow", "Get Parameter"))
        self.label.setText(_translate("MainWindow", "Data Manager"))
        self.label_2.setText(_translate("MainWindow", "Histogram"))
        self.toolButton_3.setText(_translate("MainWindow", "확대"))
        self.toolButton_4.setText(_translate("MainWindow", "관심 영역"))
        self.label_4.setText(_translate("MainWindow", "Parameter"))

    def pushAnalysisButtonClicked(self):

        self.getImgData(self.oriImgPath)

        ## 수정해야함
        
        tempClahePath = str(self.curPath) + '/uniformImg.png'
        tempRotatePath = str(self.curPath) + '/rotateMorpImh.png'
        tempSegPath = str(self.curPath) + '/segmentedImg.png'

        frame01 = QWidget() #Replace it with any frame you will putting this label_image on it
        label_Image01 = QLabel(frame01)
        image_profile01 = QImage(tempClahePath) #QImage object

        image_profile01 = image_profile01.scaled(250,250, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration    
        label_Image01.setPixmap(QtGui.QPixmap.fromImage(image_profile01)) 


        frame02 = QWidget() #Replace it with any frame you will putting this label_image on it
        label_Image02 = QLabel(frame02)
        image_profile02 = QImage(tempRotatePath) #QImage object

        image_profile02 = image_profile02.scaled(250,250, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration    
        label_Image02.setPixmap(QtGui.QPixmap.fromImage(image_profile02)) 
        print(label_Image02)

        frame03 = QWidget() #Replace it with any frame you will putting this label_image on it
        label_Image03 = QLabel(frame03)
        image_profile03 = QImage(tempSegPath) #QImage object

        image_profile03 = image_profile03.scaled(250,250, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration    
        label_Image03.setPixmap(QtGui.QPixmap.fromImage(image_profile03)) 
        print(label_Image03)

        self.gridLayout_2.addWidget(label_Image01, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(label_Image02, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(label_Image03, 1, 1, 1, 1)
        self.segWidget = label_Image03
        print("prev grid : ",self.gridLayout_2)
        print("prev widget : ",self.segWidget)

        ########### plotting histogram area ####################
        tempForHisImg01 = io.imread(tempClahePath)
        plotImg01 = PlotCanvas(tempForHisImg01)
        self.gridLayout_3.addWidget(plotImg01,1, 0, 1, 1)

        tempForHisImg02 = io.imread(tempRotatePath)
        plotImg02 = PlotCanvas(tempForHisImg02)
        self.gridLayout_3.addWidget(plotImg02,0, 1, 1, 1)

        tempForHisImg03 = io.imread(tempSegPath)
        plotImg03 = PlotCanvas(tempForHisImg03)
        self.gridLayout_3.addWidget(plotImg03,1, 1, 1, 1)
        ########################################################


        self.slider1.setImg(self.segmentedImg)
        self.slider1.setHighVal(self.otsuValue)
        self.slider1.setGrid(self.gridLayout_2)
        self.slider1.setWidget(self.segWidget)
        self.slider1.setSegPath(tempSegPath)



    #def getQImg(self,Img):
    def convert_numpy_img_to_qpixmap(self,np_img):
        height, width = np_img.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())

    def pushDataButtonClicked(self):
        # file Dialog -> list view?
        # siganl ?
        tempFlag = True
        fname = QFileDialog.getOpenFileName(self)
        self.oriImgPath = fname[0]
        self.oriImgName = self.fileNameParser(self.oriImgPath)

        print("full fname : ",fname)
        print("file path : ",self.oriImgPath)

        frame = QWidget() #Replace it with any frame you will putting this label_image on it
        label_Image = QLabel(frame)
        image_profile = QImage(self.oriImgPath) #QImage object

        image_profile = image_profile.scaled(250,250, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration    
        label_Image.setPixmap(QtGui.QPixmap.fromImage(image_profile)) 

        #self.clearLayout(self.gridLayout_2)
        #for i in reversed(range(self.gridLayout_2.count())): 
        #    self.gridLayout_2.itemAt(i).widget().deleteLater() 
        self.gridLayout_2.addWidget(label_Image, 0, 0, 1, 1)
        
        # plot histogram
        tempForHisImg = io.imread(self.oriImgPath)
        plotImg = PlotCanvas(tempForHisImg)
        self.gridLayout_3.addWidget(plotImg,0, 0, 1, 1)

        self.prevImg = label_Image
        # list view control 
        if tempFlag == True:
            # list view 추가

            model = QStandardItemModel()
            item = QStandardItem(self.oriImgName)
            #item.setForeground(self.red)
            item.setCheckable(True)
            model.appendRow(QStandardItem(item))
            self.listView.setModel(model)
            tempFlag = False

    def pushParamButtonClicked(self):
        # param = getParam()
        Params = [
            {"name": "Param1", "color": "yellow", "bg_color": "yellow"},
            {"name": "Param2", "color": "red", "bg_color": "red"},
            {"name": "Param3", "color": "green", "bg_color": "gray"},
        ]

        model = UserModel(Params)
        self.listView_2.setModel(model)


    def fileNameParser(self,fileName):
        # '/' 기준으로 단어들을 Parsing 한 후 제일 마지막 단어를 선택하면 될 듯.
        # file name이 string이라는 가정을 깔고 가는 중 이다.
        tempFileName = fileName
        tempFinder = tempFileName.split('/')
        _fileName = tempFinder[-1]
        print('finder [-1] : ',_fileName)
        return _fileName

    def getImgData(self,imgPath):
        self.segmentAlgorithm = rotateMorphSeg(imgPath)
        self.oriImg , self.claheImg ,self.rotateMorImg ,self.segmentedImg = self.segmentAlgorithm.getImg()

        self.vesselDataArray = self.oriImg , self.claheImg ,self.rotateMorImg ,self.segmentedImg

        self.otsuValue = self.segmentAlgorithm.getSegmentedHighValue()
        self.preSegImg = self.segmentAlgorithm.getPrevSegImg()


class PlotCanvas(FigureCanvas):
 
    def __init__(self,img,parent = None,width=3, height=2, dpi=100):
        #width=5; height=4; dpi=100; parent = None
        self.tempImg = img
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout()
        fig.subplots_adjust(0.2, 0.2, 0.8, 0.8)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plotImg(self.tempImg)

    def plotImg(self,img,dtype = 'float'):
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


class UserModel(QAbstractListModel):
    def __init__(self, data=None, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def data(self, QModelIndex, role=None):
        item = self._data[QModelIndex.row()]

        if role == Qt.DisplayRole:
            return "%s" % (item['name'])
        elif role == Qt.DecorationRole:
            return QColor(item['color'])
        elif role == Qt.BackgroundRole:
            return QBrush(Qt.Dense7Pattern)
        elif role == Qt.ToolTipRole:
            return "Tool Tip: %s" % (item['name'])
        return QVariant()

class CustomSlider(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(CustomSlider, self).__init__(*args, **kwargs)
        MAXVAL = 10000

        self.flag1 = 0
        self.flag2 = 0

        self.segmentedImg = None
        self.gridLayout = None
        self.otsuValue = None
        self.prevWidget = None
        self.segPath = None

        self.sliderMin = MAXVAL 
        self.sliderMax = MAXVAL
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.valueChanged.connect(self.handleSliderValueChange)
        #value change(parameter = function)
        self.numbox = QtWidgets.QSpinBox()
        self.numbox.valueChanged.connect(self.handleNumboxValueChange)

        #self.slider.setMaximumSize(QtCore.QSize(16777215, 25))

        #set maximum value
        self.slider.setMaximum(self.sliderMax)
        self.numbox.setMaximum(self.sliderMax)
        #self.slider.setValue(MAXVAL -500000)


        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.numbox)
        layout.addWidget(self.slider)

    @QtCore.pyqtSlot(int)
    def handleSliderValueChange(self, value):
        tempVal = float(value / 10000)
        self.imgClear(self.prevWidget)

        self.numbox.setValue(tempVal)

        self.flag1 = 1
        if self.flag1 == 1:
            self.handleSegmentedImgValue(tempVal)
            temp = self.makeWidget()
            print("temp : ",temp)
            print("grid : ",self.gridLayout)
            self.gridLayout.addWidget(temp, 1, 1, 1, 1)
            self.prevWidget = temp
            self.flag1 = 0
        

    @QtCore.pyqtSlot(int)
    def handleNumboxValueChange(self, value):
        # Prevent values outside slider range
        tempVal = float(value/10000)
        self.flag2 = 1
        self.imgClear(self.prevWidget)

        if tempVal < float(self.slider.minimum() / 10000):
            self.numbox.setValue(float(self.slider.minimum() / 10000))
        elif tempVal > float(self.slider.maximum() /10000):
            self.numbox.setValue(float(self.slider.maximum()/10000))

        if self.flag2 ==1 :
            self.slider.setValue(float(self.numbox.value()/10000) )
            self.handleSegmentedImgValue(tempVal)
            temp = self.makeWidget()
            self.gridLayout.addWidget(temp, 1, 1, 1, 1)
            self.prevWidget = temp
            self.flag2 = 0

    def setImg(self,img):
        self.segmentedImg = img

    def setHighVal(self,highVal):
        self.otsuValue = highVal

    def setGrid(self,grid):
        self.gridLayout = grid

    def setWidget(self,imgWidget):
        self.prevWidget = imgWidget

    def setSegPath(self,segPath):
        self.segPath = segPath

    def handleSegmentedImgValue(self,lowValue):
        tempLow = lowValue
        tempHigh = self.otsuValue
        tempImg = self.segmentedImg

        lowt = (tempImg > tempLow).astype(float)
        hight = (tempImg > tempHigh).astype(float)
        hyst = filters.apply_hysteresis_threshold(tempImg, tempLow, tempHigh)
        #hyst = hyst.astype('bool')

        self.segmentedImg = morphology.remove_small_objects(hyst,50)
        self.segmentedImg.dtype='uint8'
        cv2.imwrite('segmentedImg.png', self.segmentedImg *255)

    def makeWidget(self):
        frame03 = QWidget() #Replace it with any frame you will putting this label_image on it
        label_Image03 = QLabel(frame03)
        image_profile03 = QImage(self.segPath) #QImage object

        image_profile03 = image_profile03.scaled(250,250, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration    
        label_Image03.setPixmap(QtGui.QPixmap.fromImage(image_profile03))
        return label_Image03


    def imgClear(self,imgWidget):
        print("clear widget : ",imgWidget)
        self.gridLayout.removeWidget(imgWidget)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    #ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

