Preparing the data to be fed to the model.

1. **Images_dir** -- Should have all the resized images.
2. **Annotation files** -- Contains the following data:
        1. The location of the image so that the annotations don’t get mixed up
        2. The coordinates of the bounding boxes.
3. **Anchors file** -- A file which tells set of bounding boxes it should start off while training.
        It contains the the width and height of the bounding boxes for the set of images.
        This file can be obtained by training the using simple K-means classifier and it stores the dimensions of the bounding boxes in the ‘yolo_anchors.txt’ file which has the very less IoU (Intersection over union) scores.
4. **.names file** -- Containing the labels of the objects.


