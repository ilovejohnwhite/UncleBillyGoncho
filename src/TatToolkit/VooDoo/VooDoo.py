import cv2
import numpy as np
from skimage import morphology, segmentation
from PIL import Image

class VooDoo:
    def __init__(self):
        pass

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
        edges_image = np.full(segmented_image.shape, 255, dtype=np.uint8)
        unique_segments = np.unique(segmented_image)
        sorted_segments = sorted(unique_segments)

        for idx, segment in enumerate(sorted_segments):
            mask = (segmented_image == segment)
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
