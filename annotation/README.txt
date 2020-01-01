Step 1: To resize the images to perform annotation.

**resizedata.py** uses OpenCV. The resulting images are unrotated and resized.When PIL is used to resize the images, the resulting images are rotated by 90 degree. 

Step 2: Start annotation using imglab

Imglab is an open source annotation tool. 
It is a shell script file. Link to the repository [dlib repository](https://github.com/davisking/dlib)

To create annotation:
  In folder ../dlib/tools/imglab/build run the following commands:
    1. ./imglab -c filename.xml path_to_the_data_folder
    2. ./imglab filename.xml  
          A application opens which lets you annotate.
         
*In case of any issues use, ./imglab -h ( It shows the options ) or Help in the application opened*
    
Create 2 training files, one having annotations of voids and the other not having voids.
Classes are **'0'** for **voids** and **'1'** **not voids**
