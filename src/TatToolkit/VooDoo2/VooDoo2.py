import cv2
import numpy as np
from skimage import morphology, segmentation, measure
from skimage.morphology import binary_dilation, binary_erosion
from PIL import Image

class VooDoo2:
    def __init__(self, user_scale=5):
        self.min_cluster_size = self.scale_to_pixels(user_scale)
        print(f"User Scale: {user_scale}, Min Cluster Size: {self.min_cluster_size}")

    def scale_to_pixels(self, scale):
        # Map the scale from 1-10 to 1,000-50,000 pixels
        slope = (50000 - 1000) / (10 - 1)
        intercept = 1000 - slope
        return int(slope * scale + intercept)

    def identify_clusters(self, img):
        # Check if the image is already in grayscale
        if len(img.shape) == 2 or img.shape[2] == 1:
            gray = img
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform connected component analysis
        labeled = measure.label(binary, background=0)
        properties = measure.regionprops(labeled, binary)

      # Analyze cluster sizes
        cluster_sizes = [prop.area for prop in properties]
        max_size = max(cluster_sizes, default=0)
        min_size = min(cluster_sizes, default=0)
        mean_size = np.mean(cluster_sizes) if cluster_sizes else 0

        print(f"Cluster Sizes - Max: {max_size}, Min: {min_size}, Mean: {mean_size}")

        # Create a mask for large clusters
        large_cluster_mask = np.zeros_like(binary, dtype=bool)
        filtered_clusters = 0
        for prop in properties:
            if prop.area >= self.min_cluster_size:
                large_cluster_mask[labeled == prop.label] = True
            else:
                filtered_clusters += 1

        print(f"Filtered Clusters: {filtered_clusters} for min_cluster_size: {self.min_cluster_size}")
        return large_cluster_mask


    def draw_spaced_outlines(self, img, edges, color=0, dash_length=400, gap_length=600, thickness=1):
        dash_count = 0
        gap_count = 0
        for y in range(edges.shape[0]):
            for x in range(edges.shape[1]):
                if edges[y, x]:
                    if dash_count < dash_length:
                        cv2.circle(img, (x, y), thickness, color, -1)
                        dash_count += 1
                    else:
                        gap_count += 1
                        if gap_count == gap_length:
                            dash_count = 0
                            gap_count = 0

    def draw_solid_outline(self, img, edges, color=0, thickness=1):
        for y in range(edges.shape[0]):
            for x in range(edges.shape[1]):
                if edges[y, x]:
                    cv2.circle(img, (x, y), thickness, color, -1)

    def find_edges(self, segmented_image, num_thinning_iterations=3):
        large_cluster_mask = self.identify_clusters(segmented_image)

        edges_image = np.full(segmented_image.shape, 255, dtype=np.uint8)
        unique_segments = np.unique(segmented_image)
        sorted_segments = sorted(unique_segments)

        for idx, segment in enumerate(sorted_segments):
            mask = (segmented_image == segment)
            # Apply the large cluster mask only to non-dark segments
            if idx != 1:  # Assuming idx == 1 is the darker segment
                mask = mask & large_cluster_mask

            # Use larger structuring elements for dilation and erosion
            struct_elem_size = 12  # Increase this value for larger holes
            struct_elem = np.ones((struct_elem_size, struct_elem_size))

            mask = binary_dilation(mask, struct_elem)  # Dilation to fill small holes
            mask = binary_erosion(mask, struct_elem)   # Erosion to restore size

            # Convert mask to float for Gaussian blur
            mask_float = mask.astype(float)
            blur_size = 3  # Can be adjusted for more or less smoothing
            mask_blurred = cv2.GaussianBlur(mask_float, (blur_size, blur_size), 0)

            # Convert blurred mask back to binary for edge detection
            mask = mask_blurred > 0.5  # Threshold to convert back to binary

            segment_edges = segmentation.find_boundaries(mask, mode='outer', connectivity=1)
            if segment_edges.ndim == 3:
                segment_edges = segment_edges.any(axis=2)

            if idx == 4:  # Skip the 5th segment
                continue

            for _ in range(num_thinning_iterations):
                segment_edges = morphology.thin(segment_edges)

            if idx == 1:  # 7th segment (darkest)
                self.draw_solid_outline(edges_image, segment_edges)
            else:
                self.draw_spaced_outlines(edges_image, segment_edges)

        return edges_image
        
    def __call__(self, input_image, output_type="np", detect_resolution=None):
        if len(input_image.shape) == 3 and input_image.shape[2] == 3:
            input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

        edges_image = self.find_edges(input_image)

        if output_type == "pil":
            edges_image = Image.fromarray(edges_image)

        return edges_image
