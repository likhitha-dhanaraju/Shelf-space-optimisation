***Installing docker and tensorflow/serving***
1. Install docker according to the instructions in the official docker website [Docker installation](https://docs.docker.com/install/) </br>
2. Run the command to ***docker pull tensorflow/serving*** in the command line  </br>

Run the following command in the commandline.</br>

Change the following: </br>
1. source - *Path to the inference graph obtained* for both void detector and label detector </br>
2. Make a config file with the follwing contents and add the path accordingly</br> a

*
model_config_list: {</br>
  config: {</br>
    name:  "detection_model",</br>
    base_path:  "/models/detection_model",</br>
    model_platform: "tensorflow",</br>
    model_version_policy: {</br>
        all: {}</br>
    }</br>
  },</br>
  config: {</br>
    name:  "label_detector",</br>
    base_path:  "/models/label_detector",</br>
    model_platform: "tensorflow",</br>
    model_version_policy: {</br>
        all: {}</br>
    }</br>
  }</br>
}</br>

*

Change the name to the target name given, and mention the base_path without the '0001'

sudo docker run -p 8500:8500 -p 8501:8501   --mount type=bind,source=/home/likhitha/Documents/Projects/Dumla/flask/DetectionModel/1,target=/models/detection_model/0001   --mount type=bind,source=/home/likhitha/Documents/Projects/Dumla/flask/LabelDetector/1,target=/models/label_detector/0001  --mount type=bind,source=/home/likhitha/Documents/Projects/Dumla/flask/config.conf,target=/models/config.conf   -t tensorflow/serving --model_config_file=/models/config.conf
