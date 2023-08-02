**CWFID: A Crop/Weed Field Image Dataset** is a dataset for semantic segmentation, object detection, and instance segmentation tasks. It is used in the agricultural industry, and in the biological research. 

The dataset consists of 60 images with 492 labeled objects belonging to 2 different classes including *crop* and *weed*.

Images in the CWFID dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. All images are labeled (i.e. with annotations). There are no pre-defined <i>train/val/test</i> splits in the dataset. The dataset was released in 2015 by the Bosch Research and Leibniz Universitat Hannover.

Here is the visualized example grid with animated annotations:

[animated grid](https://github.com/dataset-ninja/cwfid/raw/main/visualizations/horizontal_grid.webm)
