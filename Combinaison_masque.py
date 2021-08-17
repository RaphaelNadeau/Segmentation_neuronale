import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import join
from time import time

src = r"C:\Users\raper\Desktop\Temp_2"  # path source pour accèder aux données

ratio_src = join(src, "Ratiométrique")
channel1_src = join(src, "Channel_1")
channel2_src = join(src, "Channel_2")
lst_ratio = listdir(ratio_src)
lst_channel1 = listdir(channel1_src)
lst_channel2 = listdir(channel2_src)
lst_mask = []
time_stamp = []

for file in lst_ratio:  # Récupère tous les masques dans le fichier où ils sont sauvegardés et les places dans une liste à part
    if "mask" in file:
        lst_mask.append(file)
for mask in lst_mask:
    splitted_mask = mask.split("_")
    indice = splitted_mask[2].split("+")
    t0 = time()
    for image in lst_channel1:  # Permet l'application du masque binaire sur l'image du canal 1
        splitted_image = image.split("_")
        indice_image = splitted_image[1].split(".")
        if indice_image[0] == indice[0]:
            image1 = plt.imread(join(ratio_src, mask))[:, :, :-1]
            image2 = plt.imread(join(channel1_src, image))[:, :, :-1]
            masked_image = image2 * image1
            plt.imsave(join(channel1_src, image) + "+mask.png", masked_image)
    time_stamp.append(time() - t0)
    t0 = time()
    for image in lst_channel2:  # Permet l'application du masque binaire sur l'image du canal 2
        splitted_image = image.split("_")
        indice_image = splitted_image[1].split(".")
        if indice_image[0] == indice[1]:
            image1 = plt.imread(join(ratio_src, mask))[:, :, :-1]
            image2 = plt.imread(join(channel2_src, image))[:, :, :-1]
            masked_image = image2 * image1
            plt.imsave(join(channel2_src, image) + "+mask.png", masked_image)
    time_stamp.append(time() - t0)
print("Le temps moyen d'application d'un masque est de {}s.".format(np.mean(time_stamp)))
