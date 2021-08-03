import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from skimage import img_as_ubyte
from time import time
import cv2 as cv

n = 10
src = r"C:\Users\raper\Desktop\Temp\ratiometrique\combined_image_33+34.jpg"
img = cv.imread(src)
image = np.array(img, dtype=np.float64) / 255


w, h, d = original_shape = tuple(image.shape)
assert d == 3
image_array = np.reshape(image, (w * h, d))

print("Fitting model on a small sub-sample of the data")
t0 = time()
image_array_sample = shuffle(image_array, random_state=0)[:1000]
kmeans = KMeans(init="k-means++", n_clusters=n, random_state=0).fit(image_array_sample)
print("done in %0.3fs." % (time() - t0))

print("Predicting color indices on the full image (k-means)")
t0 = time()
labels = kmeans.predict(image_array)
print("done in %0.3fs." % (time() - t0))


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


# Display all results, alongside original image
# plt.figure(1)
# plt.clf()
plt.subplot(2, 1, 1)
plt.axis('off')
plt.title('Original image (96,615 colors)')
plt.imshow(img)

# plt.figure(2)
# plt.clf()
plt.subplot(2, 1, 2)
plt.axis('off')
plt.title('Quantized image (3 colors, K-Means)')
plt.imshow(recreate_image(kmeans.cluster_centers_, labels, w, h))
# plt.show()
plt.clf()



# ## Make a binary mask of the image ##
def binary(codebook, labels):
    gray_value_ubyte = img_as_ubyte(codebook)
    gray_sorted = np.argsort(gray_value_ubyte, axis=0)
    binaire = np.zeros(524288)
    for i in range(0, 524288, 1):  # 524288, 1000
        if labels[i] in gray_sorted[-4:, 0]:
            binaire[i] = True
        else:
            binaire[i] = False
    # print(binary)
    binaire = np.reshape(binaire, (512, 1024))
    return binaire


binary(kmeans.cluster_centers_, labels)
plt.axis('off')
plt.imshow(binaire)
plt.show()

