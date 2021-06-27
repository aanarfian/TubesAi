from __future__ import absolute_import, division, print_function
#import matplotlib.pyplot as plt
import numpy as np
import cv2

#Using the image provided in the question
img = cv2.imread('apelAI.jpg', 0)

yImg,xImg = img.shape
how_many_255 = len(np.where(img==255)[0])
tempThresImg = np.zeros((1,yImg * xImg - how_many_255), np.uint8)

count=0
for ii in range(xImg):
    for jj in range(yImg):
        if img[jj, ii] != 255:
            tempThresImg[0, count] =  img[jj, ii]
            count +=1

threshold, temp = cv2.threshold(tempThresImg,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) #using otsu threshold
ret,thresh = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY)

threshold1, thresh1 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) #using otsu threshold

cv2.imshow('Standard Way', thresh1)
cv2.imshow('Removed 255s', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
print('\n\nThreshold with Removal= %d \t Standard Threshold = %d \n\n' %(threshold, threshold1))