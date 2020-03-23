# Running the models on a server with docker

### **Installing docker and tensorflow/serving**
1. Install docker according to the instructions in the official docker website [Docker installation](https://docs.docker.com/install/) </br>
2. Run the command to ***docker pull tensorflow/serving*** in the command line  </br>


**Link to the trained modelsof Void Detector(DetectionModel), LabelDetector and void detector model for far images (FarVoid_Detector)** </br> 
[Trained models](https://drive.google.com/open?id=1I0Ey3kGSOjUn3HBk7iC0BWi5t_XaedN4)

Download the folders from the drive link and save it in your project folder

### **To run as a server**
Run the following command in the commandline to host as a server</br>

EXAMPLE:</br>
```
sudo docker run -p 8500:8500 -p 8501:8501   --mount type=bind,source=/home/likhitha/Documents/Projects/object-detection/DetectionModel/1,target=/models/detection_model/0001   --mount type=bind,source=/home/likhitha/Documents/Projects/object-detection/LabelDetector/1,target=/models/label_detector/0001  --mount type=bind,source=/home/likhitha/Documents/Projects/object-detection/config.conf,target=/models/config.conf   -t tensorflow/serving --model_config_file=/models/config.conf
```
**Change the following:** </br>
1. source - *Path to the folders downloaded from drive* for both void detector and label detector </br>
2. Make a config file with the follwing contents and add the path accordingly </br> 

```
model_config_list: {
  config: {
    name:  "detection_model",
    base_path:  "/models/detection_model",
    model_platform: "tensorflow",
    model_version_policy: {
        all: {}
    }
  },
  config: {
    name:  "label_detector",
    base_path:  "/models/label_detector",
    model_platform: "tensorflow",
    model_version_policy: {
        all: {}
    }
  }
}
```

Change the name to the target name given, and mention the base_path without the '0001' </br>
```
If successfully hosted you will see the following output:
[evhttp_server.cc : 238] NET_LOG: Entering the event loop ...
2020-03-23 15:06:45.396900: I tensorflow_serving/model_servers/server.cc:378] Exporting HTTP/REST API at:localhost:8501 ...
```
### ***Program to run from the client side***
**client_request.py*** </br>

Make sure to keep the file **visualization_utils.py** in the same folder as the **client_request.py*** program.</br>

Change the paths of the resized_test_data, original test data, destination path for the inference labels as well as the category indices.</br>
