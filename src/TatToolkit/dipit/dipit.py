import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

class DipItPreprocessor:
    def __init__(self, n_clusters=7, smoothing_kernel_size=(7, 7)):
        self.n_clusters = n_clusters
        self.smoothing_kernel_size = smoothing_kernel_size

    def cluster_colors(self, image):
        pixels = image.reshape(-1, 3)
        kmeans = KMeans(n_clusters=self.n_clusters)
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_
        labels = kmeans.predict(pixels)
        clustered_image = centers[labels].reshape(image.shape).astype(np.uint8)
        return clustered_image

    def smooth_clusters(self, clustered_image):
        kernel = np.ones(self.smoothing_kernel_size, np.uint8)
        smoothed_image = cv2.morphologyEx(clustered_image, cv2.MORPH_CLOSE, kernel)
        return smoothed_image

    def __call__(self, input_image):
        processed_image = np.array(input_image)
        clustered_image = self.cluster_colors(processed_image)
        smoothed_image = self.smooth_clusters(clustered_image)
        return Image.fromarray(smoothed_image)

# Example usage
# preprocessor = DipItPreprocessor()
# result = preprocessor(input_image)