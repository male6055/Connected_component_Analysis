import numpy as np
import cv2

def connected_component_analysis(image):
    h, w = image.shape[:2]
    labels = np.zeros((h, w), dtype=np.uint8)
    label = 1
    equivalence = {}
    for i in range(h):
        for j in range(w):
            if image[i, j] == 255:
                neighbors = []
                if i > 0 and labels[i - 1, j] > 0:
                    neighbors.append(int(labels[i - 1, j]))
                if j > 0 and labels[i, j - 1] > 0:
                    neighbors.append(int(labels[i, j - 1]))
                if not neighbors:
                    labels[i, j] = label
                    equivalence[label] = {label}
                    label += 1
                else:
                    min_label = min(neighbors)
                    labels[i, j] = min_label
                    union_set = set()
                    for neighbor_label in neighbors:
                        union_set = union_set.union(equivalence[neighbor_label])
                    for lab in union_set:
                        equivalence[lab] = union_set
    for i in range(h):
        for j in range(w):
            if labels[i, j] > 0:
                labels[i, j] = min(equivalence[labels[i, j]])
    return labels, equivalence

image_path = "cc.png"
binary_image = cv2.imread(image_path, 0)
labels_matrix, equivalence_dict_loops = connected_component_analysis(binary_image)
output_path = "labeled_cc.png"
cv2.imwrite(output_path, labels_matrix * 255)
unique_labels = np.unique(labels_matrix)
unique_components = unique_labels[unique_labels != 0]
print(f"Number of connected components: {len(unique_components)}")
