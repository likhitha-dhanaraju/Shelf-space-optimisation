Create a *training* folder, and copy the faster_rcnn_inception_v2_coco.config file into the folder.</br>

Change the contents of the contents of the *config* file accordingly.</br>

Use a text editor to open the config file and make the following changes to the faster_rcnn_inception_v2_coco.config file.</br>
Note: The paths must be entered with single forward slashes (NOT backslashes), or TensorFlow will give a file path error when trying to train the model! Also, the paths must be in double quotation marks ( ” ), not single quotation marks ( ‘ ). </br>

***Line 10****: Set the num_classes value to the number of objects your classifier is classifying. In my case, as I am classifying voids and non-voids it would be num_classes: 2.

***In Line 107***: Give the absolute path of model.ckpt file to the file_tuning_checkpoint parameter. model.ckpt file is present in the location object_detection/faster_rcnn_inception_v2_coco_2018_01_28. In my case,</br>
fine_tune_checkpoint: “/home/likhitha/*project-folder*/training/model/faster_rcnn_inception_v2_coco_2018_01_28/model.ckpt”</br>

link to the model.ckpt file -- [faster-rcnn](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) </br>

***train_input_reader section****: you can find this section in the line 120. In this section set the input_path parameter to your train.record file. In my case it is </br>
input_path: “/home/likhitha/*project-folder*/train.record”.</br>

Set the label_map_path parameter to the labelmap.pbtxt file. In my case it is:</br>
label_map_path: “/home/likhitha/*project-folder*/training/labelmap.pbtxt”</br>

***eval config section***: You can find this section in the line 128. set num_examples parameter to the number of images present in the test directory. In my case,</br>
num_examples: 10</br>
eval_input_reader section: You can find this section in the line 134. Similar to train_input_reader section, set the paths to test.record and labelmap.pbtxt files. In my case,</br>
input_path: “/home/likhitha/*project-folder*/val.record”</br>
label_map_path: “/home/likhitha/*project-folder*/training/labelmap.pbtxt”</br>


***Run the train.py file in the command line with the following arguments*** </br>

*python train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/fater_rcnn_inception_v2_coco.config*  </br>

