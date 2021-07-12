# Aquadrone YOLO Training
## Setup
### Repo setup for Windows
The data augmentation app must be run on a Windows platform.
To install required packages, use `pip install -r requirements.txt` in the root of the repo.
### YOLO setup for Linux
* Install OpenCV from [here](https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html), following the **detailed process** steps.
*  Install Darknet from [here](https://pjreddie.com/darknet/install/).
* To compile with OpenCV, edit the `Makefile` by:
    * changing `OPENCV=0` to `OPENCV=1`
    * changing line 45 from ``LDFLAGS+= `pkg-config --libs opencv` -lstdc++`` to ``LDFLAGS+= `pkg-config --libs opencv4` -lstdc++``
    * changing line 46 from ``COMMON+= `pkg-config --cflags opencv` `` to ``COMMON+= `pkg-config --cflags opencv4` ``
* Finally, `cd src` and modify `image_opencv.cpp` by:
    * adding in missing header files
    ```cpp
    #include "opencv2/core/core_c.h"
    #include "opencv2/videoio/legacy/constants_c.h"
    #include "opencv2/highgui/highgui_c.h"
    ```
    * changing the line `IplImage ipl = m;` to `IplImage ipl = cvIplImage(m);`
## Data collection
* Videos for training can be found on the Aquadrone google drive.
* The Timestamps folder contains csv files that contain start and end times as well as labels for objects that appear in the videos.
* The timestamps are used by the `Data Collection/split_video.py` (from the original aquadrone-vision repo) to produce images of objects from the videos that can be used to train the neural network.

> `python split_video.py  --directory <directory path to store frames> --video <path to video file> --file <path to timestamp file> [--compress] [-n <number of frames per second>]`

<!--gate1, gate2, gate3 videos are from ARVP 2019--> 
## Data annotation
Before training, images must be annotated with the following information in a corresponding `.txt` file.

> `<object class> <x_center> <y_center> <width> <height>`

* `object_class` will be a number between 0 and total number of classes - 1, which identifies which object the metadata belongs to.
* `x_center` is the x coordinate of the center of the object divided by the image width.
* `y_center` is the y coordinate of the center of the object divided by the image height.
* `width` is the width of the object.
* `height` is the height of the object.

[Yolo_mark](https://github.com/AlexeyAB/Yolo_mark) and [LabelImg](https://github.com/tzutalin/labelImg) are two good options.
## Data augmentation
A GUI has been made to facilitate the process of augmenting images. The [Albumentations](https://albumentations.ai/) library was used; demoes of data augmentation techniques can be found [here](https://albumentations-demo.herokuapp.com/).

The GUI supports the following data augmentation techniques:
* Horizontal Flip
* Motion Blur
* Iso Noise
* Rotate
* CutOut
* Crop
* Rgb Shift

To run the app, navigate to the Data Augmentation folder and run `python aug_app.py`.