import numpy as np
import cv2
from queue import Queue

def connected_component_analysis_loops(image):
    """
    Perform connected component analysis using loops and maintain equivalence classes using a dictionary.
    """
    h, w = image.shape
    labels = np.zeros((h, w), dtype=np.int32)
    label = 1
    equivalence = {}

    # First pass: Label connected components and maintain equivalence classes
    for i in range(h):
        for j in range(w):
            if image[i, j] == 255:  # Path pixel
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

def find_maze_entry_exit(binary_image):
    """
    Detect the most likely entrance (top) and exit (bottom) in a maze.
    It searches for the largest continuous path in the first and last row.
    """
    h, w = binary_image.shape

    # Find possible start points (top row)
    top_indices = np.where(binary_image[0] == 255)[0]
    start = (0, top_indices[len(top_indices) // 2]) if len(top_indices) > 0 else None

    # Find possible end points (bottom row)
    bottom_indices = np.where(binary_image[h - 1] == 255)[0]
    end = (h - 1, bottom_indices[len(bottom_indices) // 2]) if len(bottom_indices) > 0 else None

    return start, end

# Load the maze image
image_path = "Maze.png"  # Ensure the correct path
maze = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Convert to binary (white paths as 255, black walls as 0)
_, binary_maze = cv2.threshold(maze, 127, 255, cv2.THRESH_BINARY)

# Perform CCA to find connected paths
labels, equivalence_dict = connected_component_analysis_loops(binary_maze)

# Find the maze entry and exit
start, end = find_maze_entry_exit(binary_maze)

# Ensure start and end points are valid
if start is None or end is None:
    raise ValueError("Failed to detect start or end points of the maze.")

# Extract start and end labels
start_label = labels[start]
end_label = labels[end]

# Solve the maze using BFS if the start and end are connected
if start_label == end_label and start_label > 0:
    q = Queue()
    q.put(start)
    visited = np.zeros((binary_maze.shape), dtype=bool)
    parent = {}

    while not q.empty():
        x, y = q.get()
        if (x, y) == end:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4-directional movement
            nx, ny = x + dx, y + dy
            if 0 <= nx < binary_maze.shape[0] and 0 <= ny < binary_maze.shape[1]:
                if labels[nx, ny] == start_label and not visited[nx, ny]:
                    visited[nx, ny] = True
                    parent[(nx, ny)] = (x, y)
                    q.put((nx, ny))

    # Backtrack to extract the solution path
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)

    # Draw the solution on the maze
    solved_maze = cv2.cvtColor(binary_maze, cv2.COLOR_GRAY2BGR)
    for x, y in path:
        solved_maze[x, y] = (0, 0, 255)  # Red solution path

    # Save the solved maze
    output_path = "Solved_Maze.png"
    cv2.imwrite(output_path, solved_maze)
    print(f"✅ Maze solved! Solution saved at {output_path}")

else:
    print("❌ Maze is not connected, check for breaks in the path.")
