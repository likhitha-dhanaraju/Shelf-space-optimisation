import csv 
import requests 
import xml.etree.ElementTree as ET 
  
  
folder = '/home/likhitha/Documents/Projects/Dumla/annotation/'

files=['train_void.xml','train_voidless.xml'] 
classes =['0','-1']

"""
Write a brief about the structure of xml files
"""

"""
Annotation in the form of 'name_of_image box1 box2 ... boxN'
boxN is of the form x_min y_min x_max y_max
"""

for class_no,file in enumerate(files):

	tree = ET.parse(folder+file) 
	root = tree.getroot() 
	filename=file.strip().split('.')[0]

	with open(filename+'.txt', 'w') as f:

	    for image in root.findall('./images/image'):
	        name = image.get('file')  
	        data=name.strip().split('/')
	        data=data[-1]+' '
	        dim=[]
	        for box in image.findall('box'):
	        	left=box.get('left')
	        	top=box.get('top')
	        	height=box.get('height')
	        	width=box.get('width')
	        	dim.append([left,top,height,width,classes[class_no]])
	        for box in dim:
	        	for j,i in enumerate(box):
	        		data+=i
	        		if j!=4:
	        			data+=','
	        	data+=' '

	        f.write(data+'\n')



