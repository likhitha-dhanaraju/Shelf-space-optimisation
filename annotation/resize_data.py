import cv2
import os
from PIL import Image
from resizeimage import resizeimage
import imutils


dataset = '/home/likhitha/Documents/Projects/Dumla/part_train/'
des = '/home/likhitha/Documents/Projects/Dumla/annotation/resized_imgs/'

dim = (640,640)

print('Starting to resize the images..')
for i in os.listdir(dataset):
	#with open(dataset+ j+ i, 'r+b') as f:
		#with Image.open(f) as image:
		image = cv2.imread(dataset+i)
		cover = cv2.resize(image,dim,interpolation = cv2.INTER_AREA)
			#cover = resizeimage.resize_cover(image, [640, 640])
		cv2.imwrite(des + i,cover)
    
print('Finished resizing images!')

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
