# YOLOv3-aquadrone
## Setup
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