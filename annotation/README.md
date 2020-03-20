To pre-process the data to feed it for training.


Step 1: *Resizing the training images* - **resizedata.py** uses OpenCV. The resulting images are unrotated and resized.When PIL is used to resize the images, the resulting images are rotated by 90 degree. 

*Change the original data path and the resized images data path accordingly.*

Step 2: Start annotation using imglab

Imglab is an open source annotation tool. 
It is a shell script file. Link to the repository [dlib repository](https://github.com/davisking/dlib)

*Make sure to install it according to the instructions mentioned in the GitHub ReadME of the dlib repository*

To create annotation:<br/>
  In folder ../dlib/tools/imglab/build run the following commands:<br/>
    1. ./imglab -c filename.xml path_to_the_resized_data_folder<br/>
    2. ./imglab filename.xml  <br/>
          A application opens which lets you annotate.<br/>
         
*In case of any issues use, ./imglab -h ( It shows the options ) or Help in the application opened*
    
Create 2 training files, one having annotations of voids and the other not having voids.<br/>
Classes are **'0'** for **voids** and **'1'** for **not voids**

*Keep the ratio of number of voids to number of non-voids to 3;1 for best results*<br/>

Step 3: **pre-processing.py** - Pre-processing the data to generate tensorflow record files to feed it for training.<br/>
*Change the path of the resized images path, the file name of the xml files and Class_mapping accordingly.*

