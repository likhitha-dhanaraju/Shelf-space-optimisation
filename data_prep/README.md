**Pre-training*

1. Preparing the data
2. Preparing the pre-trained model

-------------------------------------------------------------------------------------------------------------------------------
Preparing the data to be fed to the model.

1. **Images_dir** -- Should have all the resized images.
2. **Annotation files** -- Contains the following data:
        1. The location of the image so that the annotations don’t get mixed up
        2. The coordinates of the bounding boxes.
3. **Anchors file** -- A file which tells set of bounding boxes it should start off while training.
        It contains the the width and height of the bounding boxes for the set of images.
        This file can be obtained by training the using simple K-means classifier and it stores the dimensions of the bounding boxes in the ‘yolo_anchors.txt’ file which has the very less IoU (Intersection over union) scores.
        ![Predicted anchor boxes by k-means](https://miro.medium.com/max/1159/1*8OAPNpqI92FM9S9lWH8AkA.png)
        
4. **.names file** -- Containing the labels of the objects.


**To-be done**
The images and annotations are created in the annotations folder
For generating the ***"anchors.txt"**** file, run the **kmeans.py** file.
For the ****.names file***, create a simple text file. Add each label in a new line and save it with ***.names*** extension

-------------------------------------------------------------------------------------------------------------------------------

Preparing the keras model.

Run the **convert.py** to obtain the keras model. Change the location of the .cfg ( configuration file ) and .weights file




