import cv2
import numpy as np

img = cv2.imread('apelAI.jpg', 0)
gblur = cv2.GaussianBlur(img, (11, 11), 0)
_, th1 = cv2.threshold(gblur, 230, 255, cv2.THRESH_BINARY)
# kernel = np.ones((5, 5), np.float32)/25


cv2.imshow("Image", th1)
cv2.waitKey(0)
cv2.destroyAllWindows()

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