import cv2
import os
import numpy as np
import time
from sklearn.model_selection import train_test_split
import requests 
from PIL import Image
import xml.etree.ElementTree as ET 
import shutil
import glob
import pandas as pd

start_t= time.time()

cwd = os.getcwd()
"""
#Path of the data folder
path = os.path.join(cwd,'TestingDataShelf_03022020')
des = os.path.join(cwd,'resized_imgs')
dim = (416,416)
input_shape=416
files=[f for f in os.listdir(path) if '.jpg' in f]

if os.path.exists(des)!=True:
	os.mkdir(des)

print('Starting to resize the images..')

for j,i in enumerate(files):
		print("Resizing the "+str(j+1)+"th image...")
		if os.path.exists(os.path.join(des,i))!=True:
			image = cv2.imread(os.path.join(path,i))
			correct = np.array(255 * (image/ 255) ** 1.2 , dtype='uint8')
			cover = cv2.resize(correct,dim,interpolation = cv2.INTER_AREA)
			cv2.imwrite(os.path.join(des,i),cover)
print('Finished resizing!')
"""
path = os.path.join(os.path.dirname(cwd),'resized_imgs')
files=['labels_full.xml']

CLASS_MAPPING = {
	'1':'label'
	# Add your remaining classes here.
}


files=[f for f in os.listdir(path) if '.jpg' in f]
dim = (416,416)
input_shape=416
print("Starting to shuffle and split the data to train, validation and test dataset....")
train_files,split_files = train_test_split(files,test_size=0.1,shuffle=True)
val_files,test_files = train_test_split(split_files,test_size=0.5,shuffle=True)

print("Number of training files: "+str(len(train_files)))
print("Number of validation files: "+str(len(val_files)))
print("Number of test files: "+str(len(test_files)))

data=['train_files','val_files','test_files']
data_arr=[train_files,val_files,test_files]
for i in data:
	if os.path.exists(os.path.join(cwd,i))!=True:
		os.mkdir(os.path.join(cwd,i))

print("Saved files to their respective folders")
#List of the xml files


des =['train_txt','val_txt','test_txt']

train_txt=[]
val_txt=[]
test_txt=[]
if os.path.exists(os.path.join(cwd,'text_ann'))!=True:
	os.mkdir(os.path.join(cwd,'text_ann'))

for k in range(len(des)):
	if os.path.exists(os.path.join(cwd,'text_ann',des[k]))!=True:
		os.mkdir(os.path.join(cwd,'text_ann',des[k]))
MAPPING = ['label']
for class_no,file in enumerate(files):

	tree = ET.parse(cwd+'/'+file) 
	root = tree.getroot() 
	for image in root.findall('./images/image'):
		name = image.get('file') 
		name = name.strip().split('/')[-1]
		filename=name.strip().split('.jpg')[0]
		boxes_ =''
		for box in image.findall('box'):
			left=int(box.get('left'))
			top=int(box.get('top'))
			height=int(box.get('height'))
			width=int(box.get('width'))
			x_min = int(left)
			y_max = int(top)
			x_max = int((left + width))
			y_min = int((top + height))

			if x_min<0:
				x_min = 0
			
			if x_max > input_shape:
				x_max = input_shape
			if y_min < 0:
				y_min=0
			if x_max<x_min:
				temp = x_min
				x_min = x_max
				x_max = temp
			if y_max<y_min:
				temp = y_min
				y_min = y_max
				y_max = temp

			if y_max > input_shape:
				y_max = input_shape
			box=name+' '+MAPPING[class_no]+' '+str(x_min)+' '+str(y_min)+' '+str(x_max)+' '+str(y_max)+'\n'
			print(box)
			boxes_+=box
		if name in train_files and boxes_!='':
			with open(os.path.join(cwd,'text_ann',des[0],filename+'.txt'),'w') as f:
				f.write(boxes_)
				shutil.copy(os.path.join(os.path.dirname(cwd),'resized_imgs',name),os.path.join(cwd,'train_files',name))
				f.close()

		if name in val_files and boxes_!='':
			with open(os.path.join(cwd,'text_ann',des[1],filename+'.txt'),'w') as f:
				f.write(boxes_)
				shutil.copy(os.path.join(os.path.dirname(cwd),'resized_imgs',name),os.path.join(cwd,'val_files',name))
				f.close()
				
		
		if name in test_files and boxes_!='':
			with open(os.path.join(cwd,'text_ann',des[2],filename+'.txt'),'w') as f:
				f.write(boxes_)
				shutil.copy(os.path.join(os.path.dirname(cwd),'resized_imgs',name),os.path.join(cwd,'test_files',name))
				f.close()


#Convert the annotations voc file 

def create_root(IMAGE_DIR,file_prefix, width, height):
	root = ET.Element("annotations")
	ET.SubElement(root, "folder").text = "images"
	ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
	ET.SubElement(root, "path").text = IMAGE_DIR+"/{}.jpg".format(file_prefix)
	size = ET.SubElement(root, "size")
	ET.SubElement(size, "width").text = str(width)
	ET.SubElement(size, "height").text = str(height)
	ET.SubElement(size, "depth").text = "3"
	return root


def create_object_annotation(root, voc_labels):
	for voc_label in voc_labels:
		obj = ET.SubElement(root, "object")
		ET.SubElement(obj, "name").text = voc_label[0]
		ET.SubElement(obj, "pose").text = "Unspecified"
		ET.SubElement(obj, "truncated").text = str(0)
		ET.SubElement(obj, "difficult").text = str(0)
		bbox = ET.SubElement(obj, "bndbox")
		ET.SubElement(bbox, "xmin").text = str(int(voc_label[1]))
		ET.SubElement(bbox, "ymin").text = str(int(voc_label[2]))
		ET.SubElement(bbox, "xmax").text = str(int(voc_label[3]))
		ET.SubElement(bbox, "ymax").text = str(int(voc_label[4]))
	return root

def create_file(IMAGE_DIR,DESTINATION_DIR,file_prefix, width, height, voc_labels):
	root = create_root(IMAGE_DIR,file_prefix, width, height)
	root = create_object_annotation(root, voc_labels)
	tree = ET.ElementTree(root)
	tree.write("{}/{}.xml".format(DESTINATION_DIR, file_prefix))

def read_file(ANNOTATIONS_DIR_PREFIX,DESTINATION_DIR,IMAGE_DIR,file_path):
	file_prefix = file_path.split(".txt")[0]
	image_file_name = "{}.jpg".format(file_prefix)
	w, h = 416,416
	with open(ANNOTATIONS_DIR_PREFIX+'/'+file_path, 'r') as file:
		lines = file.readlines()
		voc_labels = []
		for line in lines:
			voc = []
			line = line.strip()
			data = line.split()
			voc.append(data[1])
			voc.append(float(data[2]))
			voc.append(float(data[3]))
			voc.append(float(data[4]))
			voc.append(float(data[5]))
			voc_labels.append(voc)
		create_file(IMAGE_DIR,DESTINATION_DIR,file_prefix, w, h, voc_labels)
	print("Processing complete for file: {}".format(file_path))




def start():
	for val,i in enumerate(['train','val','test']):
		DESTINATION_DIR = os.path.join(cwd,'annotations',i+'_ann')
		ANNOTATIONS_DIR_PREFIX = os.path.join(cwd,'text_ann',des[val])
		if not os.path.exists(DESTINATION_DIR):
			os.makedirs(DESTINATION_DIR)
		IMAGE_DIR =os.path.join(cwd,data[val])
		for filename in os.listdir(os.path.join(cwd,'text_ann',des[val])):
			read_file(ANNOTATIONS_DIR_PREFIX,DESTINATION_DIR,IMAGE_DIR,filename)
		else:
			print("Skipping file: {}".format(filename))

if __name__ == "__main__":
	start()

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

    xml_df = pd.DataFrame(xml_list, columns=column_name)
    names=[]
    for i in xml_df['filename']:
        names.append(i)
    xml_df['filename']=names

    return xml_df

def main():
	for folder in ['train_ann','val_ann','test_ann']:
	    image_path = os.path.join(os.getcwd(),'annotations', folder)
	    xml_df = xml_to_csv(image_path)
	    xml_df.to_csv(folder+'_labelsfull.csv', index=None)
	    print('Successfully converted xml to csv.')

main()
end_t=time.time()

print("Finished the pre-processing in "+str(end_t-start_t)+" seconds!")