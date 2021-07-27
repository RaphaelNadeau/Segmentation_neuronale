import matplotlib.pyplot as plt
import numpy as np
from tifffile import imread, imsave, imshow
import matplotlib.pyplot as plt
import time
import cv2

src = r"C:\Users\raper\Desktop\Temp\ratiometrique\combined_image_3+4.tif"

image = imread(src)
print(image.dtype)

image = np.float32(image)
print(image.dtype, image.shape)
img = image.reshape(-1)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 10
ret, label, center = cv2.kmeans(img, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape(image.shape)
cv2.imshow("res2", res2)
cv2.waitKey(0)
cv2.destroyAllWindows()

