**CWFID: A Crop/Weed Field Image Dataset** is a dataset for semantic segmentation, object detection, and instance segmentation tasks. It is used in the agriculture industry.

The dataset consists of 60 images with 492 labeled objects belonging to 2 different classes including *crop* and *weed*.

Each image in the CWFID dataset has pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. All images are labeled (i.e. with annotations). There is 1 split in the dataset: *ds* (60 images). The dataset was released in 2015.

Here is the visualized example grid with annotations:

<img src="https://github.com/dataset-ninja/cwfid/raw/main/visualizations/side_annotations_grid.png">
