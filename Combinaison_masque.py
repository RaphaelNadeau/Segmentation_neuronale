import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from skimage import img_as_ubyte
from scipy import ndimage as nd
from os import listdir
from os.path import join

src = r"C:\Users\raper\Desktop\Temp"


ratio_src = join(src, "Ratiométrique")
channel1_src = join(src, "Channel_1")
channel2_src = join(src, "Channel_2")
lst_ratio = listdir(ratio_src)
lst_channel1 = listdir(channel1_src)
lst_channel2 = listdir(channel2_src)
lst_mask = []

for file in lst_ratio:
    if "mask" in file:
        lst_mask.append(file)
for mask in lst_mask:
    splitted_mask = mask.split("_")
    indice = splitted_mask[2].split("+")
    for image in lst_channel1:
        splitted_image = image.split("_")
        indice_image = splitted_image[1].split(".")
        if indice_image[0] == indice[0]:
            image1 = plt.imread(join(ratio_src, mask))[:, :, :-1]
            image2 = plt.imread(join(channel1_src, image))[:, :, :-1]
            masked_image = image2 * image1
            plt.imsave(join(channel1_src, image)+"+mask.png", masked_image)
    for image in lst_channel2:
        splitted_image = image.split("_")
        indice_image = splitted_image[1].split(".")
        if indice_image[0] == indice[1]:
            image1 = plt.imread(join(ratio_src, mask))[:, :, :-1]
            image2 = plt.imread(join(channel2_src, image))[:, :, :-1]
            masked_image = image2 * image1
            plt.imsave(join(channel2_src, image) + "+mask.png", masked_image)


