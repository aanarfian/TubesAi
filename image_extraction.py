from pywt import dwt2
import numpy as np
import cv2
from skimage.feature import greycomatrix

def process_image(filename):
    # load image dan convert grayscale
    img = cv2.imread(filename, 0)
    # menghaluskan gambar dengan blur
    gblur = cv2.GaussianBlur(img, (5, 5), 0)
    return gblur

def get_energy(gblur):
    m,n = gblur.shape
    cA, (cH, cV, cD) = dwt2(gblur,'db1')
    # a - LL, h - LH, v - HL, d - HH as in matlab
    cHsq = [[elem * elem for elem in inner] for inner in cH]
    cVsq = [[elem * elem for elem in inner] for inner in cV]
    cDsq = [[elem * elem for elem in inner] for inner in cD]
    Energy = (np.sum(cHsq) + np.sum(cVsq) + np.sum(cDsq))/(m*n)
    return Energy

def get_entropy(gblur):
    glcm = np.squeeze(greycomatrix(gblur, distances=[1], 
                                angles=[0], symmetric=True, 
                                normed=True))
    entropy = -np.sum(glcm*np.log2(glcm + (glcm==0)))
    return entropy

def get_intensity_and_st_deviation(gblur):
    mean, std = cv2.meanStdDev(gblur)
    return mean[0][0], std[0][0]

def get_smoothnes(std):
    R = 1 - 1/(1+std**2)
    return R