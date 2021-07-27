import matplotlib.pyplot as plt
import numpy as np
from tifffile import imread, imsave, imshow
import matplotlib.pyplot as plt
import time
import cv2

src = r"C:\Users\raper\Desktop\Temp\ratiometrique\combined_image_3+4.tif"

image = imread(src)
print(image.dtype)

image = cv2.normalize(image, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
print(image.dtype)

