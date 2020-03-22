import requests
import base64
import json
import numpy as np
import os
import cv2
import ast
import time
# Import utilites 
import visualization_utils as vis_util 

CWD_PATH = os.getcwd()
input_shape=416

category_index1= {1: {'id': 1, 'name': 'empty'}, 2: {'id': 2, 'name': 'non_empty'}}
category_index2= {1: {'id': 1, 'name': 'label'}}

RESIZED_TEST_DATA = os.path.join(os.path.dirname(CWD_PATH),'data_folders','test_data_resized')
ORIG_TEST_DATA = os.path.join(os.path.dirname(CWD_PATH),'data_folders','test_data')
DES_PATH = os.path.join(CWD_PATH,'test_results_todelete')

if os.path.exists(DES_PATH)!=True:
	os.mkdir(DES_PATH)

DIR_LIST=['no_label','detected_label']

for label in DIR_LIST:
	if os.path.exists(os.path.join(DES_PATH,label))!=True:
		os.mkdir(os.path.join(DES_PATH,label))

images = os.listdir(RESIZED_TEST_DATA)

for img in images:

	start = time.time()
	image_path=os.path.join(RESIZED_TEST_DATA,img)
	URL = "http://localhost:8501/v1/models/detection_model:predict" 
	headers = {"content-type": "application/json"}
	image_content = base64.b64encode(open(image_path,'rb').read()).decode("utf-8")

	body = {
		"instances": [
					 {"b64":image_content}
					]
		}

	r = requests.post(URL, data=json.dumps(body), headers = headers) 

	text = r.text

	lis = text.strip().split('{')[2]
	l = lis.strip().split(',\n')

	for item in range(len(l)):
		name = l[item].strip().split(':')
		if name[0] =='"detection_boxes"' :
			value = name[-1].strip().split(':')[-1]
			val_list = value.strip().split('}')
			val_list = val_list[0].strip().split('\n')
			boxes_=val_list[0]

		if name[0] =='"detection_scores"':
			value = name[-1].strip().split(':')[-1]
			val_list = value.strip().split('}')
			val_list = val_list[0].strip().split('\n')
			scores_=val_list[0]
		if name[0] =='"detection_classes"' :
			value = name[-1].strip().split(':')[-1]
			val_list = value.strip().split('}')
			val_list = val_list[0].strip().split('\n')
			classes_=val_list[0]
	boxes =  ast.literal_eval(boxes_)
	scores =  ast.literal_eval(scores_)
	classes = ast.literal_eval(classes_)
	boxes1 = np.array(boxes)
	classes1 = np.array(classes)
	scores1 = np.array(scores)
	imagevoid = cv2.imread(image_path)

	_,pred_boxes,strings=vis_util.visualize_boxes_and_labels_on_image_array( 
			imagevoid, 
			np.squeeze(boxes1), 
			np.squeeze(classes1).astype(np.int32), 
			np.squeeze(scores1), 
			category_index1,
			use_normalized_coordinates = True, 
			line_thickness = 3, 
			min_score_thresh = 0.6)

	images_list=[]
	orig_images_list=[]
	number = 0

	for num,value in enumerate(strings):

		if 'non_empty' not in value[0]:
			number+=1
			ymin,xmin,ymax,xmax = pred_boxes[num]
			im_width,im_height,_ = imagevoid.shape
			(left, right, top, bottom) = (int(xmin * im_width), int(xmax * im_width),
									  int(ymin * im_height), int(ymax * im_height))
			images_list.append(imagevoid[top:bottom,left:right])

			orig_image = cv2.imread(os.path.join(ORIG_TEST_DATA,img))
			orig_width,orig_height,_ = orig_image.shape
			min_shape = min(orig_width,orig_height)
			dim=(int(min_shape),int(min_shape))
			orig_image = cv2.resize(orig_image,dim,interpolation = cv2.INTER_AREA)
			(left, right, top, bottom) = (int(xmin * min_shape), int(xmax * min_shape),
									  int(ymin * min_shape), int(ymax * min_shape))
			orig_images_list.append(orig_image[top:bottom,left:right])

	if number==0:
		print("No void detected")
		FIN_PATH=os.path.join(DES_PATH,DIR_LIST[0])

	if number==1:
		print("Single void detected")
		FIN_PATH=os.path.join(DES_PATH,DIR_LIST[1])

		#cv2.imwrite(os.path.join(DES_PATH,DIR_LIST[1],img),images_list[0])

	if number>1:
		print(str(number)+" voids detected!")
		FIN_PATH=os.path.join(DES_PATH,DIR_LIST[1])
		#for k,i in enumerate(images_list):
			#cv2.imwrite(os.path.join(DES_PATH,DIR_LIST[1],img+str(k)+'.jpg'),i)

	end=time.time()
	print("Void detection in "+img+' done! in '+str(end-start)+' seconds')

	if len(images_list)!=0:

		for j,image in enumerate(images_list):

			start = time.time()
			URL = "http://localhost:8501/v1/models/label_detector:predict" 
			image_content = image.astype('uint8').tolist()
			body = {"instances": [{"inputs": image_content}]}
			r = requests.post(URL, data=json.dumps(body), headers = headers) 

			
			text = r.text
			lis = text.strip().split('{')[2]
			l = lis.strip().split(',\n')

			for item in range(len(l)):
				name = l[item].strip().split(':')
				if name[0] =='"detection_boxes"' :
					value = name[-1].strip().split(':')[-1]
					val_list = value.strip().split('}')
					val_list = val_list[0].strip().split('\n')
					boxes_=val_list[0]

				if name[0] =='"detection_scores"':
					value = name[-1].strip().split(':')[-1]
					val_list = value.strip().split('}')
					val_list = val_list[0].strip().split('\n')
					scores_=val_list[0]
				if name[0] =='"detection_classes"' :
					value = name[-1].strip().split(':')[-1]
					val_list = value.strip().split('}')
					val_list = val_list[0].strip().split('\n')
					classes_=val_list[0]
			boxes =  ast.literal_eval(boxes_)
			scores =  ast.literal_eval(scores_)
			classes = ast.literal_eval(classes_)
			boxes = np.array(boxes)
			classes = np.array(classes)

			_, pred_boxes_labels,_ = vis_util.visualize_boxes_and_labels_on_image_array( 
					image, 
					np.squeeze(boxes), 
					np.squeeze(classes).astype(np.int32), 
					np.squeeze(scores), 
					category_index2,
					use_normalized_coordinates = True, 
					line_thickness = 1, 
					min_score_thresh = 0.9)

			if pred_boxes_labels!=[]:
				for box in pred_boxes_labels:
					ymin,xmin,ymax,xmax = box
					new_im = orig_images_list[j]
					im_width, im_height,_ = new_im.shape
					(left, right, top, bottom) = (int(xmin * im_height), int(xmax * im_height),
											  int(ymin * im_width), int(ymax * im_width))
					new_im =new_im[top:bottom,left:right]

					cv2.imwrite(os.path.join(FIN_PATH,img+'label'+str(j)+'.jpg'),new_im)

			end=time.time()
			print("Label detection in "+img+' done! in '+str(end-start)+' seconds')

	else:
		start = time.time()
		print("No label detected in void")
		orig_image = cv2.imread(os.path.join(ORIG_TEST_DATA,img))

		_,pred_boxes,strings=vis_util.visualize_boxes_and_labels_on_image_array( 
			orig_image, 
			np.squeeze(boxes1), 
			np.squeeze(classes1).astype(np.int32), 
			np.squeeze(scores1), 
			category_index1,
			use_normalized_coordinates = True, 
			line_thickness = 3, 
			min_score_thresh = 0.6)
		cv2.imwrite(os.path.join(FIN_PATH,img+'label.jpg'),orig_image)
		end=time.time()
		print("Label detection in "+img+' done! in '+str(end-start)+' seconds')
