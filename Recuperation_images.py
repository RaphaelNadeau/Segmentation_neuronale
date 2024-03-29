import os
import numpy as np
import tifffile
import matplotlib.pyplot as plt


src = r"C:\Users\raper\Desktop\Temp_2"  # path source pour accèder aux données


def extraction_image(source_file, saving_file=None, ratiometrique=True, save=False):
    """
    :param source_file: Le directory source dans lequel sont les images à récupérer
    :type source_file: str
    :param saving_file: Le directory dans lequel les images seront sauvegardées, None par défaut si l'on ne veut pas sauvegarder
    :type saving_file: str
    :param ratiometrique: Détermine si les images à récupérer sont de nature ratiométrique ou non
    :type ratiometrique: bool
    :param save: Détermine si l'on veut sauvegarder les images ou seulement extraire les images pour les manipulés, False par défaut
    :type save: bool
    :return: un tuple avec une liste contenant toutes les images individuelle et une liste avec toutes les images ratiométriques
    :rtype: tuple
    """
    finalimages = []
    combinedimages = []
    compteur = 1
    for root, dirnames, filenames in os.walk(source_file):
        images = []
        if "Channel_1" in root or "Channel_2" in root or "Ratiométrique" in root:
            continue
        elif not dirnames:
            for file in filenames:
                if file.endswith("tif"):
                    fullname = os.path.join(root, file)
                    images.append(tifffile.imread(fullname))
                    image = np.sum(images, 0)
            finalimages.append(image)
            if save:
                channel1 = saving_file + "\\" + "Channel_1"
                channel2 = saving_file + "\\" + "Channel_2"
                if not os.path.exists(channel1):
                    os.makedirs(channel1)
                if not os.path.exists(channel2):
                    os.makedirs(channel2)
                if compteur % 2 == 1:
                    plt.imsave(channel1 + "\\" + f"image_{compteur}.png", image, cmap='gray')
                elif compteur % 2 == 0:
                    plt.imsave(channel2 + "\\" + f"image_{compteur}.png", image, cmap='gray')
            if ratiometrique:
                if compteur % 2 == 0:
                    combined_image = np.add(finalimages[compteur - 2], finalimages[compteur - 1])
                    combinedimages.append(combined_image)
                    if save:
                        ratio = saving_file + "\\" + "Ratiométrique"
                        if not os.path.exists(ratio):
                            os.makedirs(ratio)
                        plt.imsave(ratio + "\\" + f"combined_image_{compteur - 1}+{compteur}.png", combined_image,
                                   cmap='gray')
            compteur += 1
    return finalimages, combinedimages


extraction_image(src, src, save=True)
