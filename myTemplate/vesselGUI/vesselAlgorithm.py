
print('hellow')
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from skimage.morphology import disk
import os
import sys
import math
import skimage
from skimage import morphology
from skimage import img_as_float
from skimage import img_as_ubyte
from skimage import img_as_uint
from skimage import io
from skimage import util
from scipy.ndimage.filters import convolve
from scipy import signal
from skimage.filters import threshold_otsu
from skimage.filters import rank
from skimage.filters import median

from skimage import img_as_float #convert img, we should use this function. Do Not Use np.astype
from skimage import transform
from skimage.filters.rank import median
from skimage import data, filters

from retinaSeg import retinahelpfunction as rhf
from retinaSeg import retinapreprocess as rpp
import cv2



def morphology_line(length,degree = None):
    if degree != None:
        line = np.zeros((length,length))
        center = int(length/2)
        line[center,:] = 1
        return line
    else:
        line = np.zeros((length,length))
        center = int(length/2)
        line[center,:] = 1
        line = transform.rotate(line,degree)
        return line
    
def rotate_line_opening(img,rotateNum,length,option = 'sup'):
    if option =='sup':
        col,row = img.shape
        result = img
        degree = 180 / rotateNum
        for cnt in range(rotateNum+1):
            if cnt ==0:
                #temp = morphology.opening(img,rhf.strel_line(length,degree * cnt))
                #temp = morphology.dilation(img,rhf.strel_line(length,degree * cnt))
                pass
                #result = temp

            rotateSe1 = rhf.strel_line(length,degree *cnt)
            temp = morphology.opening(img,rotateSe1)
            result = np.dstack([result,temp] )

        '''
        for cnt in range(rotateNum+1):
            rhf.show_on_jupyter(result[:,:,cnt],'gray',str(degree * cnt))
        '''
        finalResult = np.zeros((col,row))
        #print(result.shape)
        for i in range(col):
            for j in range(row):
                #print(result[i,j,:])
                    finalResult[i,j] = np.max(result[i,j,:])
        
        #print(finalResult.shape)
        #print(finalResult)
        #rhf.show_on_jupyter(img,'gray','original')
        #rhf.show_on_jupyter(finalResult,'gray','result')
    elif option =='inf':
        col,row = img.shape
        result = img
        degree = 165 / rotateNum
        for cnt in range(rotateNum+1):
            if cnt ==0:
                pass

            rotateSe1 = rhf.strel_line(length,degree *cnt)
            temp = morphology.opening(img,rotateSe1)
            result = np.dstack([result,temp] )

        finalResult = np.zeros((col,row))
        for i in range(col):
            for j in range(row):
                    finalResult[i,j] = np.min(result[i,j,:])

    return finalResult
    
def interval_mapping(image, from_min, from_max, to_min, to_max):
    # map values from [from_min, from_max] to [to_min, to_max]
    # image: input array
    from_range = from_max - from_min
    to_range = to_max - to_min
    scaled = np.array((image - from_min) / float(from_range), dtype=float)
    return to_min + (scaled * to_range)



class rotateMorphSeg():
    def __init__(self,imgPath):
        self.imgPath = imgPath
        self.oriImg = None
        self.uniformImg = None
        self.claheImg = None
        self.invertImg = None
        self.rotateMorImg = None
        self.segmentedImg = None
        self.setAlgorithm()

    def setAlgorithm(self):
        self.oriImg = io.imread(self.imgPath)
        if len(self.oriImg.shape) == 3:
            self.oriImg = cv2.resize(self.oriImg[:,:,1],(1020,680))
        elif len(self.oriImg.shape) ==2:
            self.oriImg = cv2.resize(self.oriImg,(1020,680))	
        else:
            print('img size error!')
            exit(-1)		

        skimage.io.imsave('original.png',self.oriImg)
        resizedVal = (1020,680)
        blockSize = (102,68)

        self.uniformImg = rpp.luminosity_contrast_normalization(self.oriImg,blockSize,resizedVal)
        #skimage.io.imsave('uniformImg.png',self.uniformImg)

        self.claheImg = rpp.clahe_preprocessing(self.uniformImg)
        skimage.io.imsave('uniformImg.png',self.claheImg)

        self.invertImg = util.invert(self.claheImg)
        skimage.io.imsave('invertImg.png',self.invertImg)

        rotateFirstEq = rotate_line_opening(self.invertImg,18,21)
        rotateSecondEq = rotate_line_opening(self.invertImg,18,25,'inf')
        self.rotateMorImg = np.subtract(rotateFirstEq,rotateSecondEq)
        skimage.io.imsave('rotateMorpImh.png',self.rotateMorImg)

        low = 0.15
        high = threshold_otsu(self.rotateMorImg)

        temp = rpp.luminosity_contrast_normalization(self.rotateMorImg,blockSize,resizedVal)
        temp = cv2.normalize(img_as_float(temp), None, 0.0, 1.0, cv2.NORM_MINMAX)

        lowt = (temp > low).astype(float)
        hight = (temp > high).astype(float)
        hyst = filters.apply_hysteresis_threshold(temp, low, high)
        #hyst = hyst.astype('bool')

        self.segmentedImg = morphology.remove_small_objects(hyst,50)
        self.segmentedImg.dtype='uint8'
        cv2.imwrite('segmentedImg.png', self.segmentedImg *255)

    def getImg(self):
        #self.claheImg = interval_mapping(self.claheImg,0.0,1.0,0,255).astype('uint8')
        #self.rotateMorImg = interval_mapping(self.rotateMorImg,0.0,1.0,0,255).astype('uint8')
        return self.oriImg,self.claheImg,self.rotateMorImg,self.segmentedImg




    #def setHysthresisValue(self):
    #    pass
'''
if __name__ == '__main__':
    print("hellow")
    vesselPath03 = './data/18.06.25/18_06_25_06.bmp'
    temp = rotateMorphSeg(vesselPath03)
'''

