import os
import numpy as np
import tifffile
import matplotlib.pyplot as plt
import time

src = r"C:\Users\raper\Desktop\Temp"  # path source pour accèder aux données


# finalImages = []
# combinedImages = []
# compteur = 1
# begin = time.time()
# # une boucle qui traverse les différents fichiers et dossiers à partir de la source
# for root, dirnames, filenames in os.walk(src):
#     # print(root, dirnames, filenames)
#     images = []
#     if dirnames == []:
#         for file in filenames:  # traverse dans tous les fichiers qui sont présent dans un dossier
#             if file.endswith("tif"):
#                 fullname = os.path.join(root, file)
#                 # print(fullname)
#                 images.append(tifffile.imread(fullname))
#                   # fait la moyenne de toutes les images dans le dossier, on obtient alors l'image d'intensité moyenne pour la channel en question
#                 image = np.mean(images, 0)
#         plt.imshow(image, cmap='gray')
#         plt.show()
#         #tifffile.imsave(src + "\\" + f"image{compteur}.tif", image)
#         finalImages.append(image)
#
#         if compteur % 2 == 0:  # la prochaine portion combine l'image de la channel 1 et l'image de la channel 2 pour avoir l'image ratiométrique
#             combined_image = np.add(finalImages[compteur - 2], finalImages[compteur - 1])
#             # print(combined_image.shape)
#             # plt.imshow(combined_image, cmap='gray')
#             # plt.show()
#             combinedImages.append(combined_image)
#             #tifffile.imsave(src + "\\" + f"combined_image_{compteur - 1}+{compteur}.tif", combined_image)
#
#         compteur += 1
#         if compteur > 4:
#             break
#
# end = time.time()
# print(end - begin)
# print(finalImages[0])
# print(finalImages[1])
# print(finalImages[0] == combinedImages[0])
# print(len(finalImages))
# print(len(combinedImages))
# print(len(finalImages) / 2 == len(combinedImages))

def extraction_image(source_file, saving_file, ratiometrique=True, save=True):
    finalimages = []
    combinedimages = []
    compteur = 1
    for root, dirnames, filenames in os.walk(source_file):
        images = []
        if not dirnames:
            for file in filenames:
                if file.endswith("tif"):
                    fullname = os.path.join(root, file)
                    images.append(tifffile.imread(fullname))
                    image = np.mean(images, 0)
            plt.imshow(image, cmap='gray')
            plt.show()
            finalimages.append(image)
            if save:
                tifffile.imsave(src + "\\" + f"image{compteur}.tif", image)
            if ratiometrique:
                if compteur % 2 == 0:
                    combined_image = np.add(finalImages[compteur - 2], finalImages[compteur - 1])
                    combinedimages.append(combined_image)
                    if save:
                        tifffile.imsave(src + "\\" + f"combined_image_{compteur - 1}+{compteur}.tif", combined_image)
            compteur += 1
    return finalimages, combinedimages
