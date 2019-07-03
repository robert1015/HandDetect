# HandPose Net

## Requirement
- Python 3.7

## Annotation tool
If you want to run the annotation tool, get into folder 'annotation/' and run:
'''
$ python3 Annotation_tool.py
'''
The serial number of last annotated image is saved in **checkpoint.txt**. If you want change the start serial number of images when openning the annotation tool, please change the number in **checkpoint.txt**

## Model

### Training
If you want to training a new model, please get into the root folder and run:
'''
$ python3 main.py
'''
The training result is saved in 'result/' by default.
### Predicting
If you want to load an existed model and predict the handpose, please run:
'''
$ python3 predict.py --model_path path_of_model
'''
**path_of_model** is the path of the model you want to load. The value of --model_path is 'hand.model' by default, which is a model already generated.

After that, please input the serial number of image in the terminal, and the image with keypoints predicted will be shown.