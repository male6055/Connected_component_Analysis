import numpy
import cv2

empty_image = numpy.zeros((501,501), dtype = numpy.uint8)
cv2.imshow('empty_image',empty_image)
cv2.waitKey()