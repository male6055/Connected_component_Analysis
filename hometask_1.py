import numpy as np
import cv2

#black image
size = 501
empty_image = np.zeros((size, size), dtype=np.uint8)

# Define center point
center_x, center_y = size // 2, size // 2

# Create a manual Euclidean distance map
distance_map = np.zeros((size, size), dtype=np.float32)

# Compute the Euclidean distance using loops
for i in range(size):
    for j in range(size):
        distance_map[i, j] = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)

# Normalize the distance map to 0-255
max_distance = distance_map.max()
for i in range(size):
    for j in range(size):
        distance_map[i, j] = (distance_map[i, j] / max_distance) * 255

distance_map = distance_map.astype(np.uint8)


def quantized_image(image, levels):
    if levels == 1:
        return np.zeros((size,size), dtype=np.uint8)
    quantized_image = np.zeros((size,size), dtype=np.uint8)
    step = 255 // (levels - 1)
    h,w = image.shape[:2]
    for i in range(h):
        for j in range(w):
            quantized_image[i, j] = (image[i, j] // step) * step

    return quantized_image


distance_map_16 = quantized_image(distance_map, 16)
distance_map_4 = quantized_image(distance_map, 4)
distance_map_1 = quantized_image(distance_map, 1)

cv2.imshow("Original Euclidean Distance Map", distance_map)
cv2.imshow("16-Level Quantization", distance_map_16)
cv2.imshow("4-Level Quantization", distance_map_4)
cv2.imshow("1-Level Quantization", distance_map_1)

cv2.waitKey()
cv2.destroyAllWindows()
