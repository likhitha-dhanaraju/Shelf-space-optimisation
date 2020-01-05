**Pre-training**

1. Preparing the data
2. Preparing the pre-trained model

-------------------------------------------------------------------------------------------------------------------------------
Preparing the data to be fed to the model.

1. **Images_dir** -- Should have all the resized images.
2. **Annotation files** -- Contains the following data:<br/>
        1. The location of the image so that the annotations don’t get mixed up<br/>
        2. The coordinates of the bounding boxes.
3. **Anchors file** -- A file which contains initial set of bounding boxes to start off while training.<br/>
        a. It contains the the width and height of the bounding boxes for the set of images.<br/>
        b. This file can be obtained by using simple K-means clustering and it stores the dimensions of the bounding boxes in the ‘yolo_anchors.txt’ file.<br/>
        c. The appropriate bounding box is selected as the bounding box with highest IOU between the ground truth box and anchor box. <br/>
        ![Predicted anchor boxes by k-means](https://miro.medium.com/max/1159/1*8OAPNpqI92FM9S9lWH8AkA.png)
        
4. **.names file** -- Containing the labels of the objects.


**To-be done**<br/>
The images and annotations are created in the annotations folder<br/>
For generating the ***"anchors.txt"**** file, run the **kmeans.py** file.<br/>
For the ****.names file***, create a simple text file. Add each label in a new line and save it with ***.names*** extension<br/>

-----------------------------------------------------------------------------------------------------------------------------

Preparing the keras model.<br/>

Run the **convert.py** to obtain the keras model. Change the location of the .cfg ( configuration file ) and .weights file





