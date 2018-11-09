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
from PyQt5.QtWidgets import QFileDialog,QWidget,QLabel
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage,QPixmap

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
import vesselAlgorithm
from vesselAlgorithm import rotateMorphSeg
from vesselAlgorithm import interval_mapping
print('vessel_algorithm import')

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,MainWindow):
        super(Ui_MainWindow,self).__init__()

        self.oriImgPath = None
        self.oriImgName = None
        self.prevImg = None

        self.oriImg = None
        self.claheImg = None
        self.rotateMorImg = None
        self.segmentedImg = None
        self.vesselDataArray = []

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
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(295, 205, 181, 71))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
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

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vessel GUI"))
        self.pushButton.setText(_translate("MainWindow", "Analysis"))
        self.label.setText(_translate("MainWindow", "Data Manager"))
        self.label_2.setText(_translate("MainWindow", "Histogram"))
        self.pushButton_2.setText(_translate("MainWindow", "Data load"))
        self.toolButton_3.setText(_translate("MainWindow", "확대"))
        self.toolButton_4.setText(_translate("MainWindow", "관심 영역"))
        self.label_4.setText(_translate("MainWindow", "Parameter"))

    def pushAnalysisButtonClicked(self):
        '''
        self.getImgData(self.oriImgPath)
        print('interval_mapping fail?')
        #temp01 = interval_mapping(self.claheImg,0.0,1.0,0,255).astype('uint8')
        print("interval_mapping succ?")
        frame = QWidget()
        label_Image01 = QLabel(frame)
        tempClahe = self.convert_numpy_img_to_qpixmap(self.claheImg)
        print('convert succ?')
        label_Image01.setPixmap(tempClahe)
        self.gridLayout_2.addWidget(label_Image01, 1, 0, 1, 1)


        print('interval_mapping fail02?')
        #temp02 = interval_mapping(self.rotateMorImg,0.0,1.0,0,255).astype('uint8')
        print("interval_mapping succ02?")

        tempMorp = self.convert_numpy_img_to_qpixmap(self.rotateMorImg)

        frame02 = QWidget()
        label_Image02 = QLabel(frame02)
        label_Image02.setPixmap(tempMorp)'''

        self.getImgData(self.oriImgPath)
        tempClahePath = '/Users/hyeonwoojeong/Desktop/bono_workstation/projects/myPyQt/myTemplate/vesselGUI/uniformImg.png'
        tempRotatePath = '/Users/hyeonwoojeong/Desktop/bono_workstation/projects/myPyQt/myTemplate/vesselGUI/rotateMorpImh.png'

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

        self.gridLayout_2.addWidget(label_Image01, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(label_Image02, 0, 1, 1, 1)


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
    



    def fileNameParser(self,fileName):
        # '/' 기준으로 단어들을 Parsing 한 후 제일 마지막 단어를 선택하면 될 듯.
        # file name이 string이라는 가정을 깔고 가는 중 이다.
        tempFileName = fileName
        tempFinder = tempFileName.split('/')
        _fileName = tempFinder[-1]
        print('finder [-1] : ',_fileName)
        return _fileName

    def getImgData(self,imgPath):
        segmentAlgorithm = rotateMorphSeg(imgPath)
        self.oriImg , self.claheImg ,self.rotateMorImg ,self.segmentedImg = segmentAlgorithm.getImg()
        self.vesselDataArray = self.oriImg , self.claheImg ,self.rotateMorImg ,self.segmentedImg


    '''
    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()'''

'''
class fileDialog(QWidget):
    def __init__(self,pushButton):
        QThread.__init__(self)
        print("what push button : ",type(pushButton))
        self.fPath = None
        self.pushButton = pushButton
        print("what push button2 : ",type(pushButton))

        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.getFileName()
        # push -> file dialog event

    def pushButtonClicked(self):
        self.fPath = QFileDialog.getOpenFileName(self)
    
    def getFileName(self):
        return self.fPath
'''

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    #ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

