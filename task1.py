import numpy as np
import cv2

my_image = cv2.imread("gradient.png", 0)
cv2.imshow("Original", my_image)
cv2.waitKey()

h, w = my_image.shape[:2]
out_image1 = np.zeros((h, w), dtype=np.uint8)
out_image2 = np.zeros((h, w), dtype=np.uint8)
out_image3 = np.zeros((h, w), dtype=np.uint8)

for i in range(h):
    for j in range(w):
        p = my_image[i, j]

        if p <= 15:
            out_image1[i, j] = 0
        elif 15 < p <= 31:
            out_image1[i, j] = 1
        elif 31 < p <= 47:
            out_image1[i, j] = 2
        elif 47 < p <= 63:
            out_image1[i, j] = 3
        elif 63 < p <= 79:
            out_image1[i, j] = 4
        elif 79 < p <= 95:
            out_image1[i, j] = 5
        elif 95 < p <= 111:
            out_image1[i, j] = 6
        elif 111 < p <= 127:
            out_image1[i, j] = 7
        elif 127 < p <= 143:
            out_image1[i, j] = 8
        elif 143 < p <= 159:
            out_image1[i, j] = 9
        elif 159 < p <= 175:
            out_image1[i, j] = 10
        elif 175 < p <= 191:
            out_image1[i, j] = 11
        elif 191 < p <= 207:
            out_image1[i, j] = 12
        elif 207 < p <= 223:
            out_image1[i, j] = 13
        elif 223 < p <= 239:
            out_image1[i, j] = 14
        elif 239 < p <= 255:
            out_image1[i, j] = 15


# 4 level
for i in range(h):
    for j in range(w):
        p = my_image[i, j]

        if p <= 63:
            out_image2[i, j] = 0
        elif 63 < p <= 127:
            out_image2[i, j] = 1
        elif 127 < p <= 191:
            out_image2[i, j] = 2
        elif 191 < p <= 255:
            out_image2[i, j] = 3


# 1 level
for i in range(h):
    for j in range(w):
        p = my_image[i, j]

        if p <= 127:
            out_image3[i, j] = 0
        elif 127 < p <= 255:
            out_image3[i, j] = 1



cv2.imshow("16 Levels", out_image1*16)
cv2.waitKey()


cv2.imshow("4 Levels", out_image2*64)
cv2.waitKey()

cv2.imshow("1 Levels", out_image3*128)
cv2.waitKey()
cv2.destroyAllWindows()
