import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from skimage import img_as_ubyte
from scipy import ndimage as nd
from os import listdir
from os.path import join

n = 10
src = r"C:\Users\raper\Desktop\Temp\Ratiométrique"


def kmeans_segmentation(source, nb_cluster):
    """
    Fonction permettant de ségmenter une image RGB avec un algorithme de KMeans, on obtient alors différentes couleurs
    moyennes pour les différents segments.
    :param source: Le fichier image à ségmenter
    :type source: ndarray
    :param nb_cluster: Le nombre de division demander pour la segmentation
    :type nb_cluster: int
    :return: La valeur moyenne des différents groupes, les étiquettes associées à chaque groupe, la hauteur de l'image
    et la largeur de l'image
    :rtype: tuple avec à l'intérieur (ndarray, ndarray, int, int)
    """
    img = plt.imread(source)[:, :, :-1]
    print(source)
    image = np.array(img, dtype=np.float64)
    h, w, d = tuple(image.shape)  # La taille originale de l'image
    assert d == 3
    image_array = np.reshape(image, (w * h, d))
    image_array_sample = shuffle(image_array, random_state=0)[:1000]
    kmeans = KMeans(init="k-means++", n_clusters=nb_cluster, random_state=0).fit(image_array_sample)
    labels = kmeans.predict(image_array)
    return kmeans.cluster_centers_, labels, h, w


def recreate_image(codebook, labels, height, width):
    """
    Permet de reconstituer l'image ségmentée avec le KMeans avec les couleurs associées aux bonnes étiquettes
    :param codebook: Les valeurs moyennes des groupes formés par la segmentation par Kmeans
    :type codebook: ndarray
    :param labels: Les étiquettes provennant de la ségmentation par Kmeans.
    :type labels: ndarray
    :param height: La hauteur de l'image
    :type height: int
    :param width: La largeur de l'image
    :type width: int
    :return: L'image reconstituée avec les résultats de la segmentation
    :rtype: ndarray
    """
    d = codebook.shape[1]
    image = np.zeros((height, width, d))
    label_idx = 0
    for i in range(height):
        for j in range(width):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image


## Make a binary mask of the image ##
def binary(codebook, labels, height, width, denoising=True):
    """
    :param codebook: Les valeurs moyennes des groupes formés par la segmentation par Kmeans
    :type codebook: ndarray
    :param labels: Les étiquettes provennant de la ségmentation par Kmeans.
    :type labels: ndarray
    :param height: La hauteur de l'image
    :type height: int
    :param width: La largeur de l'image
    :type width: int
    :param denoising: Détermine si le masque binaire subi une réduction de bruit
    :type denoising: bool
    :return: Le masque binaire de l'image analysée
    :rtype: ndarray
    """
    gray_value_ubyte = img_as_ubyte(codebook)
    gray_sorted = np.argsort(gray_value_ubyte, axis=0)
    binaire = np.zeros(524288)
    for i in range(0, 524288, 1):  # 524288, 1000
        if labels[i] in gray_sorted[-4:, 0]:
            binaire[i] = True
        else:
            binaire[i] = False
    binaire = np.reshape(binaire, (height, width))
    if denoising:
        binaire_open = nd.binary_opening(binaire, np.ones((3, 3)))
        binaire_closed = nd.binary_closing(binaire_open, np.ones((3, 3)))
        return binaire_closed
    else:
        return binaire




list_of_files = listdir(src)
for file in list_of_files:
    if file.endswith(".png"):
        # Pour s'assurer de ne pas reségmenter les images qui ont déjà été traitées
        if "_segmented" in file or "_binary_mask" in file:
            continue
        else:
            filename = join(src, file)  # Le nom complet du fichier en cours
            file_split = file.split(".")
            kmean = kmeans_segmentation(filename, n)  # Ségmentation de l'image en cours
            segmented_image = recreate_image(kmean[0], kmean[1], kmean[2], kmean[3])  # Recréation de l'image ségmentée
            #plt.imsave(src + "\\" + file_split[0] + "_segmented.png", segmented_image)
            binaire = binary(kmean[0], kmean[1], kmean[2], kmean[3], denoising=True)  # Création d'un masque binaire associé à l'image
            #plt.imsave(src + "\\" + file_split[0] + "_binary_mask.png", binaire, cmap='gray')
            ## Décomenter si l'on veut voir le mask binaire pendant le traitement des images
            plt.imshow(binaire, cmap='gray')
            plt.axis("off")
            plt.show()
    else:
        continue
