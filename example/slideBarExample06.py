import sys
import cv2
import numpy as np
import PIL
import os
from matplotlib import pyplot as plt

from scipy import ndimage
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


class Przetwarzanie_obrazow(QDialog):
    def __init__(self):
        super(Przetwarzanie_obrazow, self).__init__()
        #load ui.
        loadUi('gui.ui', self)
        # use ui file's name, loadUi -> inherit everthing of ui file.
        # just make signale - slot 

        self.image = None
        self.image_2 = None
        self.imageLoaded = False
        self.imageLoaded_2 = False
        self.processedImage = None
        self.imageFilePath = None
        self.loadButton_2.clicked.connect(self.loadClicked_2)
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.clicked.connect(self.saveClicked)

        #9
        self.gaussButton.clicked.connect(self.gaussClicked)
        self.hSlider_gauss.valueChanged.connect(self.gaussDisplay)
        self.medianButton.clicked.connect(self.medianClicked)
        self.hSlider_median.valueChanged.connect(self.medianDisplay)
        self.prewittButton.clicked.connect(self.prewittClicked)
        self.sobelButton.clicked.connect(self.sobelClicked)
        self.bilateralButton.clicked.connect(self.bilateralClicked)
        self.hSlider_bilateral.valueChanged.connect(self.bilateralDisplay)
        self.robertsButton.clicked.connect(self.robertsClicked)

        #8
        self.dilateGrayscaleButton.clicked.connect(self.dilateGrayscaleClicked)
        self.hSlider_dilateGrayscale.valueChanged.connect(self.dilateGrayscaleDisplay)
        self.erodeGrayscaleButton.clicked.connect(self.erodeGrayscaleClicked)
        self.hSlider_erodeGrayscale.valueChanged.connect(self.erodeGrayscaleDisplay)

        #7
        self.dilateBinaryButton.clicked.connect(self.dilateBinaryClicked)
        self.hSlider_dilateBinary.valueChanged.connect(self.dilateBinaryDisplay)
        self.hSlider_dilateBinaryLowerThreshold.valueChanged.connect(self.dilateBinaryDisplay)
        self.hSlider_dilateBinaryUpperThreshold.valueChanged.connect(self.dilateBinaryDisplay)
        self.erodeBinaryButton.clicked.connect(self.erodeBinaryClicked)
        self.hSlider_erodeBinary.valueChanged.connect(self.erodeBinaryDisplay)
        self.hSlider_erodeBinaryLowerThreshold.valueChanged.connect(self.erodeBinaryDisplay)
        self.hSlider_erodeBinaryUpperThreshold.valueChanged.connect(self.erodeBinaryDisplay)

        #2
        self.AddWeightedTwoImagesButton.clicked.connect(self.addWeightedTwoImagesClicked)
        self.hSlider_addWeightedTwoImages.valueChanged.connect(self.addWeightedTwoImagesDisplay)

        self.AddWeightedConstButton.clicked.connect(self.addWeightedConstClicked)
        self.hSlider_addWeightedConst.valueChanged.connect(self.addWeightedConstDisplay)

        self.divideConstButton.clicked.connect(self.divideConstClicked)
        self.hSlider_divideConst.valueChanged.connect(self.divideConstDisplay)

        self.divideImagesButton.clicked.connect(self.divideImagesClicked)

        self.powImageButton.clicked.connect(self.powImageClicked)

        #1
        self.resizeImageButton.clicked.connect(self.resizeClicked)
        self.SaveSecondImageButton.clicked.connect(self.saveClicked_2)

        #4
        self.uniformButton.clicked.connect(self.uniformClicked)
        self.hSlider_uniform.valueChanged.connect(self.uniformDisplay)

        self.variousHeightButton.clicked.connect(self.variousHeightClicked)
        self.hSlider_variousHeight.valueChanged.connect(self.variousHeightDisplay)

        self.variousWidthButton.clicked.connect(self.variousWidthClicked)
        self.hSlider_variousWidth.valueChanged.connect(self.variousWidthDisplay)


        self.rotateButton.clicked.connect(self.rotateClicked)
        self.hSlider_rotate.valueChanged.connect(self.rotateDisplay)

        #histogram
        self.histogramButton.clicked.connect(self.histogramClicked)
        self.histogramLocalThresholdButton.clicked.connect(self.histogramLocalThresholdClicked)
        self.histogramGlobalThresholdButton.clicked.connect(self.histogramGlobalThresholdClicked)


        self.hSlider_histogramGlobalUpperThreshold.valueChanged.connect(self.histogramGlobalThresholdDisplay)
        self.hSlider_histogramGlobalLowerThreshold.valueChanged.connect(self.histogramGlobalThresholdDisplay)

        self.hSlider_histogramLocalUpperThreshold.valueChanged.connect(self.histogramLocalThresholdDisplay)
        self.hSlider_histogramLocalLowerThreshold.valueChanged.connect(self.histogramLocalThresholdDisplay)

        self.equalizeHistButton.clicked.connect(self.equalizehistClicked)

    #5//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    @pyqtSlot()
    def equalizehistClicked(self):
        img_to_yuv = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2YUV)
        img_to_yuv[:, :, 0] = cv2.equalizeHist(img_to_yuv[:, :, 0])
        hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)
        self.processedImage = hist_equalization_result
        self.displayImage(2)

    @pyqtSlot()
    def histogramGlobalThresholdDisplay(self):
        self.histogramGlobalUpperThresholdBox.setText(str(self.getHistogramGlobalUpperThresholdSliderValue()))
        self.histogramGlobalLowerThresholdBox.setText(str(self.getHistogramGlobalLowerThresholdSliderValue()))
        if self.imageLoaded:
            image1_1 = self.image.copy()
            image1_1 = cv2.inRange(image1_1, self.getHistogramGlobalLowerThresholdSliderValue(),
                                   self.getHistogramGlobalUpperThresholdSliderValue())
            self.processedImage = image1_1
            self.displayImage(2)

    def getHistogramGlobalUpperThresholdSliderValue(self):
        return int(self.hSlider_histogramGlobalUpperThreshold.value())

    def getHistogramGlobalLowerThresholdSliderValue(self):
        return int(self.hSlider_histogramGlobalLowerThreshold.value())

    @pyqtSlot()
    def histogramGlobalThresholdClicked(self):
        self.hSlider_histogramGlobalLowerThreshold.setValue(self.getHistogramGlobalLowerThresholdValue())
        self.histogramGlobalUpperThresholdBox.setText(str(255))
        self.hSlider_histogramGlobalUpperThreshold.setValue(self.getHistogramGlobalUpperThresholdValue())
        self.histogramGlobalLowerThresholdBox.setText(str(120))
        if self.imageLoaded:
            image1_1 = self.image.copy()
            image1_1 = cv2.inRange(image1_1, self.getHistogramGlobalLowerThresholdValue(), self.getHistogramGlobalUpperThresholdValue())

            self.processedImage = image1_1
            self.displayImage(2)

    def getHistogramGlobalLowerThresholdValue(self):
        return int(self.histogramGlobalLowerThresholdBox.text())

    def getHistogramGlobalUpperThresholdValue(self):
        return int(self.histogramGlobalUpperThresholdBox.text())

    @pyqtSlot()
    def histogramLocalThresholdDisplay(self):
        self.histogramLocalUpperThresholdBox.setText(str(self.getHistogramLocalUpperThresholdSliderValue()))
        self.histogramLocalLowerThresholdBox.setText(str(self.getHistogramLocalLowerThresholdSliderValue()))
        if self.imageLoaded:
            image_tmp = self.image.copy()
            image_tmp = cv2.medianBlur(image_tmp, 5)
            image_tmp = cv2.cvtColor(image_tmp, cv2.COLOR_RGB2GRAY)
            ret, image_tmp = cv2.threshold(image_tmp, self.getHistogramLocalLowerThresholdSliderValue(),
                                           self.getHistogramLocalUpperThresholdSliderValue(), cv2.THRESH_BINARY)
            image_tmp = cv2.adaptiveThreshold(image_tmp, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            self.processedImage = image_tmp
            self.displayImage(2)

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

    @pyqtSlot()
    def histogramClicked(self):
        if self.imageLoaded:
            color = ('b', 'g', 'r')
            plt.figure(1)
            for i, col in enumerate(color):
                histr = cv2.calcHist([self.processedImage], [i], None, [256], [0, 256])
                plt.plot(histr, color=col)
                plt.xlim([0, 256])
        plt.show()
        self.displayImage(2)
        plt.show()

            #4 /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @pyqtSlot()
    def rotateClicked(self):

        self.hSlider_rotate.setValue(self.getRotateValue())
        if self.imageLoaded:
            M1 = cv2.getRotationMatrix2D((self.image.shape[1]/2,self.image.shape[0]/2), self.getRotateValue(),1)

            self.processedImage = cv2.warpAffine(self.image,M1,(self.image.shape[1],self.image.shape[0]))
            self.displayImage(2)

    @pyqtSlot()
    def rotateDisplay(self):
        self.rotateBox.setText(str(self.getRotateValue()))
        if self.imageLoaded:
            M1 = cv2.getRotationMatrix2D((self.image.shape[1] / 2, self.image.shape[0] / 2), self.getRotateSliderValue(), 1)

            self.processedImage = cv2.warpAffine(self.image, M1, (self.image.shape[1], self.image.shape[0]))
            self.displayImage(2)

    def getRotateValue(self):
        return int(self.rotateBox.text())


    def getRotateSliderValue(self):
        return int(self.hSlider_rotate.value())

    #/////////////////////////////////////////////////////////////////////////////////////////////
    @pyqtSlot()
    def variousWidthClicked(self):

        self.hSlider_variousWidth.setValue(self.getVariousWidthValue())
        if self.imageLoaded:
            factor = self.getVariousWidthValue()/100
            self.processedImage = cv2.resize(self.image, (0,0), fx=factor, fy=1 )
            self.displayImage(2)


    @pyqtSlot()
    def variousWidthDisplay(self):
        self.variousWidthBox.setText(str(self.getVariousWidthSliderValue()))
        if self.imageLoaded:
            factor = self.getVariousWidthSliderValue()/100
            self.processedImage = cv2.resize(self.image, (0,0), fx=factor, fy=1 )
            self.displayImage(2)

    def getVariousWidthSliderValue(self):
        return int(self.hSlider_variousWidth.value())

    def getVariousWidthValue(self):
        return int(self.variousWidthBox.text())

    #/////////

    @pyqtSlot()
    def variousHeightClicked(self):

        self.hSlider_variousHeight.setValue(self.getVariousHeightValue())
        if self.imageLoaded:
            factor = self.getVariousHeightValue()/100
            self.processedImage = cv2.resize(self.image, (0,0), fx=1, fy=factor )
            self.displayImage(2)


    @pyqtSlot()
    def variousHeightDisplay(self):
        self.variousHeightBox.setText(str(self.getVariousHeightSliderValue()))
        if self.imageLoaded:
            factor = self.getVariousHeightSliderValue()/100
            self.processedImage = cv2.resize(self.image, (0,0), fx=1, fy=factor )
            self.displayImage(2)

    def getVariousHeightSliderValue(self):
        return int(self.hSlider_variousHeight.value())

    def getVariousHeightValue(self):
        return int(self.variousHeightBox.text())

    #////////

    @pyqtSlot()
    def uniformClicked(self):

        self.hSlider_uniform.setValue(self.getUniformValue())
        if self.imageLoaded:
            factor = self.getUniformValue()/100
            self.processedImage = cv2.resize(self.image, (0,0), fx=factor, fy=factor )
            self.displayImage(2)


    @pyqtSlot()
    def uniformDisplay(self):
        self.uniformBox.setText(str(self.getUniformSliderValue()))
        if self.imageLoaded:
            factor = self.getUniformSliderValue()/100
            self.processedImage = cv2.resize(self.image, (0,0), fx=factor, fy=factor )
            self.displayImage(2)

    def getUniformSliderValue(self):
        return int(self.hSlider_uniform.value())

    def getUniformValue(self):
        return int(self.uniformBox.text())

    #1 /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    @pyqtSlot()
    def saveClicked_2(self):
        if self.imageLoaded_2:
            fname,fliter = QFileDialog.getSaveFileName(self,'Save File','C:\\',"Image Files (*.jpg)")
            if fname:
                cv2.imwrite(fname,self.image_2)
            else:
                print('Error')

    @pyqtSlot()
    def resizeClicked(self):
        if self.imageLoaded & self.imageLoaded_2:
            rows1, cols1, channels1 = self.image.shape
            rows2, cols2, channels2 = self.image_2.shape

            if rows1 < rows2:
                if cols1 <= cols2:
                    blank_image1 = np.zeros((rows2, cols2, 3), np.uint8)

                    blank_image1[0 + rows2 - rows1:rows2, 0:cols1] = self.image
                    blank_image2 = self.image_2

                    self.image = blank_image1
                    self.image_2 = blank_image2
                else:

                    blank_image1 = np.zeros((rows2, cols1, 3), np.uint8)
                    blank_image2 = np.zeros((rows2, cols1, 3), np.uint8)

                    blank_image1[0 + rows2 - rows1:rows2, 0:cols1] = self.image
                    blank_image2[0:rows2, 0:cols2] = self.image_2

                    self.image = blank_image1
                    self.image_2 = blank_image2
            elif cols1 < cols2:

                blank_image1 = np.zeros((rows1, cols2, 3), np.uint8)
                blank_image2 = np.zeros((rows1, cols2, 3), np.uint8)

                blank_image2[0:rows1, 0:cols1] = self.image
                blank_image1[0 + rows1 - rows2:rows1, 0:cols2] = self.image_2


                self.image = blank_image1
                self.image_2 = blank_image2
            else:

                blank_image1 = np.zeros((rows1, cols1, 3), np.uint8)

                blank_image1[0 + rows1 - rows2:rows1, 0:cols2] = self.image_2
                blank_image2 = self.image

                self.image = blank_image1
                self.image_2 = blank_image2

            cv2.waitKey()

    #2 /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    @pyqtSlot()
    def powImageClicked(self):
        if self.imageLoaded:
            imghsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV).astype("float32")
            (h, s, v) = cv2.split(imghsv)
            s = s * self.getPowImageValue()/2
            s = np.clip(s, 0, 255)
            imghsv = cv2.merge([h, s, v])
            self.processedImage = cv2.cvtColor(imghsv.astype("uint8"), cv2.COLOR_HSV2BGR)

            image2 = np.int16(self.processedImage.copy())
            contrast = self.getPowImageValue()*32
            brightness = 0
            image2 = image2 * (contrast / 127 + 1) - contrast + brightness
            image2 = np.clip(image2, 0, 255)
            self.processedImage = np.uint8(image2)

            imghsv = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2HSV).astype("float32")
            (h, s, v) = cv2.split(imghsv)
            v = v - self.getPowImageValue()*32
            v = np.clip(v, 0, 255)
            imghsv = cv2.merge([h, s, v])

            self.processedImage = cv2.cvtColor(imghsv.astype("uint8"), cv2.COLOR_HSV2BGR)
            self.displayImage(2)

    def getPowImageValue(self):
        return int(self.powImageBox.text())

    @pyqtSlot()
    def divideImagesClicked(self):
        if self.imageLoaded & self.imageLoaded_2:
            self.processedImage = cv2.divide(self.image, self.image_2)
            self.displayImage(2)

    @pyqtSlot()
    def divideConstDisplay(self):
        self.divideConstBox.setText(str(self.getDivideConstSliderValue()))
        if self.imageLoaded:
            blank_image = np.zeros((self.image.shape[0], self.image.shape[1], self.image.shape[2]), np.uint8)
            blank_image[:] = self.getDivideConstSliderValue()
            self.processedImage = cv2.divide(self.image, blank_image)
            self.displayImage(2)

    @pyqtSlot()
    def divideConstClicked(self):
        self.hSlider_divideConst.setValue(self.getdivideConstValue())
        if self.imageLoaded:
            blank_image = np.zeros((self.image.shape[0], self.image.shape[1], self.image.shape[2]), np.uint8)
            blank_image[:] = self.getdivideConstValue()
            self.processedImage = cv2.divide(self.image, blank_image)
            self.displayImage(2)

    def getdivideConstValue(self):
        if int(self.divideConstBox.text()) > 0:
            return int(self.divideConstBox.text())
        else:
            return 2

    def getDivideConstSliderValue(self):
        return int(self.hSlider_divideConst.value())

    @pyqtSlot()
    def addWeightedTwoImagesDisplay(self):
        self.AddWeightedTwoImagesBox.setText(str(self.getAddWeightedTwoImagesSliderValue()))
        if self.imageLoaded & self.imageLoaded_2:
            self.processedImage = cv2.addWeighted(self.image, float(self.getAddWeightedTwoImagesValue())/100, self.image_2,float((100-float(self.getAddWeightedTwoImagesValue()))/100),0)
            self.displayImage(2)

    @pyqtSlot()
    def addWeightedTwoImagesClicked(self):
        self.hSlider_addWeightedTwoImages.setValue(self.getAddWeightedTwoImagesValue())
        if self.imageLoaded & self.imageLoaded_2:
            self.processedImage = cv2.addWeighted(self.image, float(self.getAddWeightedTwoImagesValue())/100, self.image_2, float((100-float(self.getAddWeightedTwoImagesValue()))/100), 0)
            self.displayImage(2)


    def getAddWeightedTwoImagesValue(self):
        if int(self.AddWeightedTwoImagesBox.text()) >= 0 & int(self.AddWeightedTwoImagesBox.text()) <= 100:
            return float(self.AddWeightedTwoImagesBox.text())
        else:
            return 50

    def getAddWeightedTwoImagesSliderValue(self):
        return int(self.hSlider_addWeightedTwoImages.value())

    @pyqtSlot()
    def addWeightedConstDisplay(self):
        self.AddWeightedConstBox.setText(str(self.getAddWeightedConstSliderValue()))
        if self.imageLoaded:
            self.processedImage = self.adjustGamma(self.image, self.getAddWeightedConstValue())
            self.displayImage(2)

    @pyqtSlot()
    def addWeightedConstClicked(self):
        self.hSlider_addWeightedConst.setValue(self.getAddWeightedConstValue())
        if self.imageLoaded:
            self.processedImage = self.adjustGamma(self.image, self.getAddWeightedConstValue())
            self.displayImage(2)

    def getAddWeightedConstValue(self):
        if int(self.AddWeightedConstBox.text()) >= 0 & int(self.AddWeightedConstBox.text()) <= 100:
            return float(self.AddWeightedConstBox.text())
        else:
            return 2

    def getAddWeightedConstSliderValue(self):
        return int(self.hSlider_addWeightedConst.value())

    def adjustGamma(self, image, gamma):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    #7 /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @pyqtSlot()
    def erodeBinaryDisplay(self):
        self.erodeBinaryBox.setText(str(self.getErodeBinarySliderValue()))
        self.erodeBinaryLowerThresholdBox.setText(str(self.getErodeBinaryLowerThresholdValue()))
        self.erodeBinaryUpperThresholdBox.setText(str(self.getErodeBinaryUpperThresholdValue()))
        if self.imageLoaded:
            self.processedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            ret, self.processedImage = cv2.threshold(self.processedImage, self.getErodeBinaryLowerThresholdValue(),
                                                     self.getErodeBinaryUpperThresholdValue(), cv2.THRESH_BINARY)
            self.processedImage = cv2.erode(self.processedImage, self.getErodeBinaryKernelValue(), iterations=1)
            self.displayImage(2)

    @pyqtSlot()
    def erodeBinaryClicked(self):
        self.hSlider_erodeBinary.setValue(self.getErodeBinaryValue())
        self.hSlider_erodeBinaryLowerThreshold.setValue(self.getErodeBinaryLowerThresholdValue())
        self.hSlider_erodeBinaryUpperThreshold.setValue(self.getErodeBinaryUpperThresholdValue())
        if self.imageLoaded:
            self.processedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            ret, self.processedImage = cv2.threshold(self.processedImage, self.getErodeBinaryLowerThresholdValue(),
                                                     self.getErodeBinaryUpperThresholdValue(), cv2.THRESH_BINARY)
            self.processedImage = cv2.erode(self.processedImage, self.getErodeBinaryKernelValue(), iterations=1)
            self.displayImage(2)

    @pyqtSlot()
    def dilateBinaryDisplay(self):
        self.dilateBinaryBox.setText(str(self.getDilateBinarySliderValue()))
        self.dilateBinaryLowerThresholdBox.setText(str(self.getDilateBinaryLowerThresholdValue()))
        self.dilateBinaryUpperThresholdBox.setText(str(self.getDilateBinaryUpperThresholdValue()))
        if self.imageLoaded:
            self.processedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            ret, self.processedImage = cv2.threshold(self.processedImage, self.getDilateBinaryLowerThresholdValue(), self.getDilateBinaryUpperThresholdValue(), cv2.THRESH_BINARY)
            self.processedImage = cv2.dilate(self.processedImage, self.getDilateBinaryKernelValue(), iterations=1)
            self.displayImage(2)

    @pyqtSlot()
    def dilateBinaryClicked(self):
        self.hSlider_dilateBinary.setValue(self.getDilateBinaryValue())
        self.hSlider_dilateBinaryLowerThreshold.setValue(self.getDilateBinaryLowerThresholdValue())
        self.hSlider_dilateBinaryUpperThreshold.setValue(self.getDilateBinaryUpperThresholdValue())
        if self.imageLoaded:
            self.processedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            ret, self.processedImage = cv2.threshold(self.processedImage, self.getDilateBinaryLowerThresholdValue(), self.getDilateBinaryUpperThresholdValue(), cv2.THRESH_BINARY)
            self.processedImage = cv2.dilate(self.processedImage, self.getDilateBinaryKernelValue(), iterations=1)
            self.displayImage(2)

    #8 /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    @pyqtSlot()
    def erodeGrayscaleDisplay(self):
        self.erodeGrayscaleBox.setText(str(self.getErodeGrayscaleSliderValue()))
        if self.imageLoaded:
            self.processedImage = cv2.erode(self.image, self.getErodeGrayscaleKernelValue(), iterations=1)
            self.processedImage = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2GRAY)
            self.displayImage(2)

    @pyqtSlot()
    def erodeGrayscaleClicked(self):
        self.hSlider_erodeGrayscale.setValue(self.getErodeGrayscaleValue())
        if self.imageLoaded:
            self.processedImage = cv2.erode(self.image, self.getErodeGrayscaleKernelValue(), iterations=1)
            self.processedImage = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2GRAY)
            self.displayImage(2)

    @pyqtSlot()
    def dilateGrayscaleDisplay(self):
        self.dilateGrayscaleBox.setText(str(self.getDilateGrayscaleSliderValue()))
        if self.imageLoaded:
            self.processedImage = cv2.dilate(self.image, self.getDilateGrayscaleKernelValue(),iterations = 1)
            self.processedImage = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2GRAY)
            self.displayImage(2)

    @pyqtSlot()
    def dilateGrayscaleClicked(self):
        self.hSlider_dilateGrayscale.setValue(self.getDilateGrayscaleValue())
        if self.imageLoaded:
            self.processedImage = cv2.dilate(self.image, self.getDilateGrayscaleKernelValue(),iterations = 1)
            self.processedImage = cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2GRAY)
            self.displayImage(2)

    #9 /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    @pyqtSlot()
    def robertsClicked(self):
        if self.imageLoaded:
            self.processedImage = self.robertsCross(self.imageFilePath)

            if self.processedImage.shape[0] > self.image.shape[0]:
                factory_y = self.image.shape[0] / self.processedImage.shape[0]
                factory_x = self.image.shape[1] / self.processedImage.shape[1]
                self.processedImage = cv2.resize(self.processedImage, (0, 0), fx=factory_x, fy=factory_y)

            if self.processedImage.shape[0] < self.image.shape[0]:
                factory_y = self.processedImage.shape[0] / self.image.shape[0]
                factory_x = self.processedImage.shape[1] / self.image.shape[1]
                self.processedImage = cv2.resize(self.processedImage, (0, 0), fx=factory_x, fy=factory_y)

            self.displayImage(2)

    @pyqtSlot()
    def sobelClicked(self):
        if self.imageLoaded:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            img_gaussian = cv2.GaussianBlur(gray, (3, 3), 0)
            img_sobelx = cv2.Sobel(img_gaussian, cv2.CV_8U, 1, 0, ksize=5)
            img_sobely = cv2.Sobel(img_gaussian, cv2.CV_8U, 0, 1, ksize=5)
            self.processedImage = img_sobelx + img_sobely
            self.displayImage(2)

    @pyqtSlot()
    def prewittClicked(self):
        if self.imageLoaded:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            img_gaussian = cv2.GaussianBlur(gray, (3, 3), 0)
            kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
            kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
            img_prewittx = cv2.filter2D(img_gaussian, -1, kernelx)
            img_prewitty = cv2.filter2D(img_gaussian, -1, kernely)
            self.processedImage = img_prewittx + img_prewitty
            self.displayImage(2)

    @pyqtSlot()
    def bilateralDisplay(self):
        self.bilateralBox.setText(str(self.getBilateralSliderValue()))
        if self.imageLoaded:
            self.processedImage = cv2.bilateralFilter(self.image,9, self.getBilateralValue(),self.getBilateralValue())
            self.displayImage(2)

    @pyqtSlot()
    def bilateralClicked(self):
        self.hSlider_bilateral.setValue(self.getBilateralValue())
        if self.imageLoaded:
            self.processedImage = cv2.bilateralFilter(self.image,9, self.getBilateralValue(),self.getBilateralValue())
            self.displayImage(2)

    @pyqtSlot()
    def medianDisplay(self):
        self.medianBox.setText(str(self.getMedianSliderValue()))
        if self.imageLoaded:
            self.processedImage = cv2.medianBlur(self.image, self.getMedianValue())
            self.displayImage(2)

    @pyqtSlot()
    def medianClicked(self):
        self.hSlider_median.setValue(self.getMedianValue())
        if self.imageLoaded:
            self.processedImage = cv2.medianBlur(self.image, self.getMedianValue())
            self.displayImage(2)

    @pyqtSlot()
    def gaussDisplay(self):
        self.gaussBox.setText(str(self.getGaussSliderValue()))
        if self.imageLoaded:
            self.processedImage = cv2.GaussianBlur(self.image, (self.getGaussSliderValue(), self.getGaussSliderValue()), 0)
            self.displayImage(2)

    @pyqtSlot()
    def gaussClicked(self):
        self.hSlider_gauss.setValue(self.getGaussValue())
        if self.imageLoaded:
            self.processedImage = cv2.GaussianBlur(self.image, (self.getGaussValue(), self.getGaussValue()), 0)
            self.displayImage(2)

    @pyqtSlot()
    def loadClicked(self):
        fname, fliter = QFileDialog.getOpenFileName(self,'Open File','C:\\',"Image Files (*.jpg)")
        self.imageFilePath = os.path.realpath(fname)
        if fname:
            self.loadImage(fname)
        else:
            print('Invalid Image')

    @pyqtSlot()
    def loadClicked_2(self):
        fname, fliter = QFileDialog.getOpenFileName(self,'Open File','C:\\',"Image Files (*.jpg)")
        if fname:
            self.loadImage_2(fname)
        else:
            print('Invalid Image')

    @pyqtSlot()
    def saveClicked(self):
        if self.imageLoaded:
            fname,fliter = QFileDialog.getSaveFileName(self,'Save File','C:\\',"Image Files (*.jpg)")
            if fname:
                cv2.imwrite(fname,self.processedImage)
            else:
                print('Error')

    def getErodeBinarySliderValue(self):
        return int(self.hSlider_erodeBinary.value())

    def getErodeBinaryKernelValue(self):
        kernel = np.ones((int(self.erodeBinaryBox.text()), int(self.erodeBinaryBox.text())), np.uint8)
        return kernel

    def getErodeBinaryValue(self):
        if int(self.erodeBinaryBox.text()) >= 0:
            return int(self.erodeBinaryBox.text())
        else:
            return 1

    def getErodeBinaryUpperThresholdValue(self):
        return int(self.hSlider_erodeBinaryUpperThreshold.value())

    def getErodeBinaryLowerThresholdValue(self):
        return int(self.hSlider_erodeBinaryLowerThreshold.value())

    def getDilateBinaryUpperThresholdValue(self):
        return int(self.hSlider_dilateBinaryUpperThreshold.value())

    def getDilateBinaryLowerThresholdValue(self):
        return int(self.hSlider_dilateBinaryLowerThreshold.value())

    def getDilateBinaryKernelValue(self):
        kernel = np.ones((int(self.dilateBinaryBox.text()), int(self.dilateBinaryBox.text())), np.uint8)
        return kernel

    def getDilateBinaryValue(self):
        if int(self.dilateBinaryBox.text()) >= 0:
            return int(self.dilateBinaryBox.text())
        else:
            return 1

    def getDilateBinarySliderValue(self):
        return int(self.hSlider_dilateBinary.value())

    def getErodeGrayscaleKernelValue(self):
        kernel = np.ones((int(self.erodeGrayscaleBox.text()), int(self.erodeGrayscaleBox.text())), np.uint8)
        return kernel

    def getErodeGrayscaleValue(self):
        if int(self.erodeGrayscaleBox.text()) >= 0:
            return int(self.erodeGrayscaleBox.text())
        else:
            return 1

    def getErodeGrayscaleSliderValue(self):
            return int(self.hSlider_erodeGrayscale.value())

    def getDilateGrayscaleKernelValue(self):
        kernel = np.ones((int(self.dilateGrayscaleBox.text()), int(self.dilateGrayscaleBox.text())), np.uint8)
        return kernel

    def getDilateGrayscaleValue(self):
        if int(self.dilateGrayscaleBox.text()) >= 0:
            return int(self.dilateGrayscaleBox.text())
        else:
            return 1

    def getDilateGrayscaleSliderValue(self):
            return int(self.hSlider_dilateGrayscale.value())


    def robertsLoadImage(self, infilename):
            img = PIL.Image.open(infilename)
            img.load()
            img = img.convert('L')
            return np.asarray(img, dtype="int32")

    def robertsSaveImage(self, data):
            img = PIL.Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"), "L")
            open_cv_image = np.array(img)
            return open_cv_image

    def robertsCross(self, infilename):
        roberts_cross_v = np.array([[0, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, -1]])

        roberts_cross_h = np.array([[0, 0, 0],
                                    [0, 0, 1],
                                    [0, -1, 0]])
        image = self.robertsLoadImage(infilename)

        vertical = ndimage.convolve(image, roberts_cross_v)
        horizontal = ndimage.convolve(image, roberts_cross_h)

        output_image = np.sqrt(np.square(horizontal) + np.square(vertical))

        convertedValue = self.robertsSaveImage(output_image)

        return convertedValue

    def ScaleLoadedImage(self):
        rows, cols, channels = self.image.shape

        if rows<351 | cols<401:
            if rows>cols:
                factor = rows / 351
                self.image = cv2.resize(self.image, (0, 0), fx=factor, fy=factor)
            else:
                factor = cols / 401
                self.image = cv2.resize(self.image, (0, 0), fx=factor, fy=factor)
        else:
            if rows>cols:
                factor = 351 / rows
                self.image = cv2.resize(self.image, (0, 0), fx=factor, fy=factor)
            else:
                factor = 401 / cols
                self.image = cv2.resize(self.image, (0, 0), fx=factor, fy=factor)

    def ScaleLoadedImage_2(self):
        rows, cols, channels = self.image_2.shape

        if rows<351 | cols<401:
            if rows>cols:
                factor = rows / 351
                self.image_2 = cv2.resize(self.image_2, (0, 0), fx=factor, fy=factor)
            else:
                factor = cols / 401
                self.image_2 = cv2.resize(self.image_2, (0, 0), fx=factor, fy=factor)
        else:
            if rows>cols:
                factor = 351 / rows
                self.image_2 = cv2.resize(self.image_2, (0, 0), fx=factor, fy=factor)
            else:
                factor = 401 / cols
                self.image_2 = cv2.resize(self.image_2, (0, 0), fx=factor, fy=factor)

    def loadImage(self,fname):
        self.image = cv2.imread(fname)
        self.imageLoaded = True
        self.ScaleLoadedImage()
        self.processedImage = self.image.copy()
        self.displayImage(1)
        self.displayImage(2)

    def loadImage_2(self,fname):
        self.image_2 = cv2.imread(fname)
        self.ScaleLoadedImage_2()
        self.imageLoaded_2 = True

    def getBilateralValue(self):
        s = self.getBilateralSliderValue()
        try:
            if int(self.bilateralBox.text()) >= 0:
                if int(self.bilateralBox.text()) % 2 == 1:
                    return int(self.bilateralBox.text())
                else:
                    return int(self.bilateralBox.text()) + 1
            else:
                return 1
        except ValueError:
            return s

    def getMedianValue(self):
        if int(self.medianBox.text()) >= 0:
                return int(self.medianBox.text())*2+1

    def getGaussValue(self):
        if int(self.gaussBox.text()) >= 0:
            if int(self.gaussBox.text()) % 2 == 1:
                return int(self.gaussBox.text())*3
            else:
                return int(self.gaussBox.text())*3+1
        else:
            return 1

    def getBilateralSliderValue(self):
        if int(self.hSlider_bilateral.value()) % 2 == 1:
            return int(self.hSlider_bilateral.value())*3
        else:
            return int(self.hSlider_bilateral.value())*3 + 1

    def getMedianSliderValue(self):
        if int(self.hSlider_median.value()) %2 == 1:
            return int(self.hSlider_median.value())
        else:
            return int(self.hSlider_median.value())+1

    def getGaussSliderValue(self):
        if int(self.hSlider_gauss.value()) %2 == 1:
            return int(self.hSlider_gauss.value())
        else:
            return int(self.hSlider_gauss.value())+1

    def displayImage(self,window=1):
        qformat = QImage.Format_Indexed8

        if len(self.processedImage.shape) == 3: #rows[0], cols[1], channels[2]
            if(self.processedImage.shape[2])==4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img=QImage(self.processedImage, self.processedImage.shape[1], self.processedImage.shape[0], self.processedImage.strides[0], qformat)
        #BGR > RGB
        img = img.rgbSwapped()

        if window==1:
            self.img_before.setPixmap(QPixmap.fromImage(img))
            self.img_before.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if window==2:
            self.img_after.setPixmap(QPixmap.fromImage(img))
            self.img_after.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


app = QApplication(sys.argv)
window = Przetwarzanie_obrazow()
window.setWindowTitle('Image Processing')
window.show()
sys.exit(app.exec_())