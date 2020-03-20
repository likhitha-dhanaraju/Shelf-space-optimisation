import cv2
import os
import numpy as np
cwd = os.getcwd()
path = os.path.join(cwd,'TestingDataShelf_03022020')
print(path)
des = os.path.join(cwd,'far_images')
if os.path.exists(des)!=True:
	os.mkdir(des)

dim = (416,416)
files=[f for f in os.listdir(path) if '.jpg' in f]

print('Starting to resize the images..')

for j,i in enumerate(files):
		print(j)
		image = cv2.imread(os.path.join(path,i))
		correct = np.array(255 * (image/ 255) ** 1.2 , dtype='uint8')
		cover = cv2.resize(correct,dim,interpolation = cv2.INTER_AREA)
		#cover = resizeimage.resize_cover(image, [640, 640])
		cv2.imwrite(os.path.join(des,i),cover)
print('Finished resizing!')


"""

Using PIL 

import os
from PIL import Image

dataset = '/home/likhitha/Documents/Projects/Happiness_in_a_box/part_train/'

filenames = [f for f in os.listdir(dataset) if f.endswith('.jpg')]
print('Starting to resize images....')
for i in filenames:
    im = Image.open(dataset+i)
    imResize = im.resize((640,640), Image.ANTIALIAS)
    imResize.save(dataset+i , 'JPEG', quality=90)
print('Finished resizing images!')

"""
