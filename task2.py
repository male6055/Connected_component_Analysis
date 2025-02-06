import numpy as np
import cv2

def connected_component_analysis(image):
    h, w = image.shape
    labels = np.zeros((h, w), dtype=np.uint8)
    label = 1
    equivalence = {}

    for i in range(h):
        for j in range(w):
            if image[i, j] == 255:  # Foreground pixel
                neighbors = []

                # Check top neighbor
                if i > 0 and labels[i - 1, j] > 0:
                    neighbors.append(int(labels[i - 1, j]))

                # Check left neighbor
                if j > 0 and labels[i, j - 1] > 0:
                    neighbors.append(int(labels[i, j - 1]))

                if not neighbors:
                    labels[i, j] = label
                    equivalence[label] = {label}
                    label += 1
                else:
                    min_label = min(neighbors)
                    labels[i, j] = min_label

                    for neighbor_label in neighbors:
                        equivalence[min_label].update(equivalence[neighbor_label])
                        equivalence[neighbor_label] = equivalence[min_label]

    # Second pass: Resolve equivalence classes
    for i in range(h):
        for j in range(w):
            if labels[i, j] > 0:
                labels[i, j] = min(equivalence[labels[i, j]])

    return labels, equivalence


image_path = "cc.png"
binary_image = cv2.imread(image_path, 0)

labels_loops, equivalence_dict_loops = connected_component_analysis(binary_image)

output_path_loops = "labeled_cc.png"
cv2.imwrite(output_path_loops, labels_loops*255)

unique_labels = np.unique(labels_loops)
unique_components = unique_labels[unique_labels != 0]
print(f"Number of connected components: {len(unique_components)}")
