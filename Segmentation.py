import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from skimage import img_as_ubyte
from time import time
import cv2 as cv
from scipy import ndimage as nd

n = 10
src = r"C:\Users\raper\Desktop\Temp\ratiometrique\combined_image_1+2(contrast).jpg"
#src1 = r"C:\Users\raper\Desktop\Temp\ratiometrique\combined_image_1+2(contrast).jpg"


def kmeans_segmentation(source, nb_cluster):
    img = cv.imread(source)
    image = np.array(img, dtype=np.float64) / 255
    w, h, d = tuple(image.shape)  # La taille originale de l'image
    assert d == 3
    image_array = np.reshape(image, (w * h, d))
    image_array_sample = shuffle(image_array, random_state=0)[:1000]
    kmeans = KMeans(init="k-means++", n_clusters=nb_cluster, random_state=0).fit(image_array_sample)
    labels = kmeans.predict(image_array)
    return kmeans.cluster_centers_, labels, w, h, d


def recreate_image(codebook, labels, w, h):
    """Recreate the (compressed) image from the code book & labels"""
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image


# ## Make a binary mask of the image ##
def binary(codebook, labels, width, height, denoising=True):
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
    binaire = np.reshape(binaire, (width, height))
    if denoising:
        binaire_open = nd.binary_opening(binaire, np.ones((3, 3)))
        binaire_closed = nd.binary_closing(binaire_open, np.ones((3, 3)))
        return binaire_closed
    else:
        return binaire


a, b, c, d, e = kmeans_segmentation(src, n)
# f, g, h, i, j = kmeans_segmentation(src1, n)
bin1 = binary(a, b, c, d, denoising=True)
# bin2 = binary(f, g, h, i, denoising=True)
bin3 = binary(a, b, c, d, denoising=False)
# bin4 = binary(f, g, h, i, denoising=False)

plt.subplot(2, 2, 1)
plt.axis("off")
plt.imshow(bin1)

plt.subplot(2, 2, 2)
plt.axis("off")
# plt.imshow(bin2, cmap="inferno")

plt.subplot(2, 2, 3)
plt.axis("off")
plt.imshow(bin3)

plt.subplot(2, 2, 4)
plt.axis("off")
# plt.imshow(bin4, cmap="inferno")
plt.show()
