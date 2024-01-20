# conda activate DCTWM 

import cv2 #, os, sys
import numpy as np

name = "test1.jpg" # "img/test.png"

img = cv2.imread(name, 0)
# flag = cv2.IMREAD_ GRAYSCALE 
# To return the image in grayscale format, use this flag.
# As an alternative, we can set this flag's integer value to 0.

# print(img.shape[0], img.shape[1])
# # подготовка под предельный размер телеги
if img.shape[1] > 1280 or img.shape[0] > 1280:
	if img.shape[1] >= img.shape[0]:
		width = 1280
		height = int(img.shape[0] * 1280 / img.shape[1])
	else:
		height = 1280
		width = int(img.shape[1] * 1280 / img.shape[0])

	dim = (width, height)
	img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
# print(img.shape[0], img.shape[1])

key = np.random.randint(0, 256, size=[img.shape[0], img.shape[1]], dtype=np.uint8)
with open('key.npy', 'wb') as f:
    np.save(f, key)

encryption = cv2.bitwise_xor(img, key)

cv2.imwrite("encryption.jpg", encryption)

# os.execl(sys.executable, 'python', 'decryptxor.py')