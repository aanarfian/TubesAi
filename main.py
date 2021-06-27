from typing import Counter
import cv2
import numpy as np
import math
from skimage.feature import greycomatrix

img = cv2.imread('apelAI.jpg', 0)
gblur = cv2.GaussianBlur(img, (11, 11), 0)
_, thrash = cv2.threshold(gblur, 230, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# mask = cv2.bitwise_and(img,img,thrash = thrash)
mask = cv2.resize(thrash, (img.shape[1], img.shape[0]))
result = cv2.bitwise_or(img, img, mask=mask);

cv2.imshow("result", img)
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.001* cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 4:
        x1 ,y1, w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio <= 1.05:
          cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        else:
          cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 5:
        cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 10:
        cv2.putText(img, "Star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    else:
        cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

# 
perimeter = cv2.arcLength(contour,True)
area = cv2.contourArea(contour)
circularity = (4*math.pi*area)/perimeter**2
print(area)
print(perimeter)
print(circularity)

# menghitung slimness 
_, _, _, width =  cv2.boundingRect(contour)
_, _, height, _ = cv2.boundingRect(contour)
print(width)
print(height)
slimness = width / height
print(slimness)

cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

glcm = np.squeeze(greycomatrix(img, distances=[1], 
                               angles=[0], symmetric=True, 
                               normed=True))
entropy = -np.sum(glcm*np.log2(glcm + (glcm==0)))
print(entropy)


# Gaussian blur


# img = cv2.imread('apelAI.jpg', 0)
# gblur = cv2.GaussianBlur(img, (11, 11), 0)
# _, th1 = cv2.threshold(gblur, 230, 255, cv2.THRESH_BINARY)
# # kernel = np.ones((5, 5), np.float32)/25


# cv2.imshow("Image", th1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()







# import cv2
# import numpy as np

# img = cv2.imread('OpenCV-Tutorials/assets/apel.jpg', -1)

# rgb_planes = cv2.split(img)

# result_planes = []
# result_norm_planes = []
# for plane in rgb_planes:
#     dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
#     bg_img = cv2.medianBlur(dilated_img, 21)
#     diff_img = 255 - cv2.absdiff(plane, bg_img)
#     norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
#     result_planes.append(diff_img)
#     result_norm_planes.append(norm_img)

# result = cv2.merge(result_planes)
# result_norm = cv2.merge(result_norm_planes)


# gblur = cv2.GaussianBlur(result_norm, (11, 11), 0)
# _, th1 = cv2.threshold(gblur, 230, 255, cv2.THRESH_BINARY)
# # kernel = np.ones((5, 5), np.float32)/25

# cv2.imshow("Image", result_norm)
# cv2.waitKey(0)
# cv2.destroyAllWindows()