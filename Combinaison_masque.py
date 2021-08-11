import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import join
from time import time

src = r"C:\Users\raper\Desktop\Temp_2"


ratio_src = join(src, "Ratiométrique")
channel1_src = join(src, "Channel_1")
channel2_src = join(src, "Channel_2")
# test_src = join(src, "Test")
lst_ratio = listdir(ratio_src)
lst_channel1 = listdir(channel1_src)
lst_channel2 = listdir(channel2_src)
# lst_test = listdir(test_src)
lst_mask = []
time_stamp = []
for file in lst_ratio:
    if "mask" in file:
        lst_mask.append(file)
for mask in lst_mask:
    splitted_mask = mask.split("_")
    indice = splitted_mask[2].split("+")
    t0 = time()
    for image in lst_channel1:
        splitted_image = image.split("_")
        indice_image = splitted_image[1].split(".")
        if indice_image[0] == indice[0]:
            image1 = plt.imread(join(ratio_src, mask))[:, :, :-1]
            image2 = plt.imread(join(channel1_src, image))[:, :, :-1]
            masked_image = image2 * image1
            plt.imsave(join(channel1_src, image)+"+mask.png", masked_image)
    time_stamp.append(time()-t0)
    t0 = time()
    for image in lst_channel2:
        splitted_image = image.split("_")
        indice_image = splitted_image[1].split(".")
        if indice_image[0] == indice[1]:
            image1 = plt.imread(join(ratio_src, mask))[:, :, :-1]
            image2 = plt.imread(join(channel2_src, image))[:, :, :-1]
            masked_image = image2 * image1
            plt.imsave(join(channel2_src, image) + "+mask.png", masked_image)
    time_stamp.append(time()-t0)
print("Le temps moyen d'application d'un masque est de {}s.".format(np.mean(time_stamp)))

# image = plt.imread(r"C:\Users\raper\Desktop\Temp\Ratiométrique\combined_image_35+36.png")[:, :, :-1]
# mask1 = plt.imread(join(test_src, lst_test[0]))[:, :, :-1]
# mask2 = plt.imread(join(test_src, lst_test[1]))[:, :, :-1]
# mask3 = plt.imread(join(test_src, lst_test[2]))[:, :, :-1]
# mask4 = plt.imread(join(test_src, lst_test[3]))[:, :, :-1]
# mask5 = plt.imread(join(test_src, lst_test[4]))[:, :, :-1]
# mask6 = plt.imread(join(test_src, lst_test[5]))[:, :, :-1]
# mask7 = plt.imread(join(test_src, lst_test[6]))[:, :, :-1]
# mask8 = plt.imread(join(test_src, lst_test[7]))[:, :, :-1]
#
# plt.subplot(2, 4, 1)
# plt.imshow(image * mask1, cmap="gray")
# plt.axis("off")
# plt.subplot(2, 4, 2)
# plt.imshow(image * mask2, cmap="gray")
# plt.axis("off")
# plt.subplot(2, 4, 3)
# plt.imshow(image * mask3, cmap="gray")
# plt.axis("off")
# plt.subplot(2, 4, 4)
# plt.imshow(image * mask4, cmap="gray")
# plt.axis("off")
# plt.subplot(2, 4, 5)
# plt.imshow(image * mask5, cmap="gray")
# plt.axis("off")
# plt.subplot(2, 4, 6)
# plt.imshow(image * mask6, cmap="gray")
# plt.axis("off")
# plt.subplot(2, 4, 7)
# plt.imshow(image * mask7, cmap="gray")
# plt.axis("off")
# plt.subplot(2, 4, 8)
# plt.imshow(image * mask8, cmap="gray")
# plt.axis("off")
#
# plt.show()
