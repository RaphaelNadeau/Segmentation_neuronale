import os
import numpy as np
import tifffile
import matplotlib.pyplot as plt
import time

src = r"C:\Users\raper\Desktop\Temp" # path source pour accèder aux données
finalImages = []
combinedImages = []
compteur = 1
begin = time.time()
for root, dirnames, filenames in os.walk(src): # une boucle qui traverse les différents fichiers et dossiers à partir de la source
    #print(root, dirnames, filenames)
    images = []
    if dirnames == []:
        for file in filenames:  #traverse dans tous les fichiers qui sont présent dans un dossier
            if file.endswith("tif"):
                fullname = os.path.join(root, file)
                # print(fullname)
                images.append(tifffile.imread(fullname))
                image = np.mean(images, 0) # fait la moyenne de toutes les images dans le dossier, on obtient alors l'image d'intensité moyenne pour la channel en question
                # print("fart")
        # print(images[0].shape)
        # print(image.shape)
        # plt.imshow(image, cmap='gray')
        # plt.show()
        tifffile.imsave(src + "\\" + f"image{compteur}.tif", image)
        finalImages.append(image)
        # print("SHIT")
        if compteur % 2 == 0:   # la prochaine portion combine l'image de la channel 1 et l'image de la channel 2 pour avoir l'image ratiométrique
            combined_image = np.add(finalImages[compteur-2], finalImages[compteur-1])
            # print(combined_image.shape)
            # plt.imshow(combined_image, cmap='gray')
            # plt.show()
            combinedImages.append(combined_image)
            tifffile.imsave(src + "\\" + f"combined_image_{compteur-1}+{compteur}.tif", combined_image)
            # print("Prout!!!!!!")
        compteur += 1
        # if compteur > 2:
        #     break

end = time.time()
print(end - begin)
# print(finalImages[0])
# print(finalImages[1])
# print(finalImages[0] == combinedImages[0])
print(len(finalImages))
print(len(combinedImages))
print(len(finalImages)/2 == len(combinedImages))
