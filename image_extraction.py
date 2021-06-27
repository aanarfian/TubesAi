from pywt import dwt2
import cv2
import numpy as np
import math
from skimage.feature import greycomatrix
import csv

for i in range(13) :
    pathfile = "mateng/" +str(i+1)+ ".jpg"
    img = cv2.imread(pathfile, 0)
    gblur = cv2.GaussianBlur(img, (5, 5), 0)

    # cv2.imshow("shapes", gblur)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # _, (cH, cV, cD) = dwt2(gblur.T, 'db1')
    # # a - LL, h - LH, v - HL, d - HH as in matlab
    # energy = (cH**2 + cV**2 + cD**2).sum()/gblur.size
    m,n = gblur.shape
    # print(gblur.shape)
    # print(m)
    # print(n)
    cA, (cH, cV, cD) = dwt2(gblur,'db1')
    # a - LL, h - LH, v - HL, d - HH as in matlab
    cHsq = [[elem * elem for elem in inner] for inner in cH]
    cVsq = [[elem * elem for elem in inner] for inner in cV]
    cDsq = [[elem * elem for elem in inner] for inner in cD]
    Energy = (np.sum(cHsq) + np.sum(cVsq) + np.sum(cDsq))/(m*n)
    print ("energy =", Energy)

    # print ("energy =", energy)

    # entropi
    glcm = np.squeeze(greycomatrix(gblur, distances=[1], 
                                angles=[0], symmetric=True, 
                                normed=True))
    entropy = -np.sum(glcm*np.log2(glcm + (glcm==0)))
    print("entropi", entropy)

    # deviasi & mean
    mean, std = cv2.meanStdDev(gblur)
    print("rerata kontras", std[0][0])
    print("intensitas", mean[0][0])

    # smoothness
    R = 1 - 1/(1+std[0][0]**2)
    print("smoothness", R)

    with open('data_training.csv', mode='a', newline="") as data_training:
        data_write = csv.writer(data_training, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_write.writerow([Energy, entropy, std[0][0], mean[0][0], R, 1])





