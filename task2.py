import numpy as np
import cv2

my_image = cv2.imread('cc.png',0)
cv2.imshow('original',my_image)

h,w = my_image.shape[:2]

out_image = np.zeros((h,w),dtype = np.uint8)

for i in range(h):
    for j in range(w):
        p = my_image[i,j]
        if p==255:
            out_image[i,j]=


