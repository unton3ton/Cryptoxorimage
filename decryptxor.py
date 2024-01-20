# conda activate DCTWM 

# https://www.codetd.com/ru/article/12570593
# https://numpy.org/doc/stable/reference/generated/numpy.save.html#numpy.save
# 

import cv2
import numpy as np

name = "encryption.jpg"

img = cv2.imread(name, 0)

with open('key.npy', 'rb') as f:
    key = np.load(f)

decryption = cv2.bitwise_xor(img, key)

cv2.imwrite("decryption.jpg", decryption)