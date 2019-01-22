# Installation Instructions

## On Raspberry Pi

After logging in the raspberry pi, run the following
```
$ sudo raspi-config
```
This should open the configuration file and choose **Expand Filesystem** from the same. 

Again open the configuration and select **Interfacing Options** and navigate to SSH and select enable.

Following a similar approch, navigate to **Camera** and enable it.

Reboot
```
$ sudo reboot
```

## Installing OpenCV on Raspberry Pi

1. Remove unnecessary packages

```
$ sudo apt-get purge wolfram-engine
$ sudo apt-get purge libreoffice*
$ sudo apt-get clean
$ sudo apt-get autoremove
```

2. Installing dependencies
```
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install build-essential cmake pkg-config
$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
$ sudo apt-get install libxvidcore-dev libx264-dev
$ sudo apt-get install libgtk2.0-dev libgtk-3-dev
$ sudo apt-get install libcanberra-gtk*
$ sudo apt-get install libatlas-base-dev gfortran
$ sudo apt-get install python2.7-dev python3-dev
```

3. Download the OpenCV

```
$ cd ~
$ wget -O opencv.zip https://github.com/opencv/opencv/archive/3.3.0.zip
$ unzip opencv.zip
$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
$ unzip opencv_contrib.zip
```

4. Installing python package manager

```
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python get-pip.py
$ sudo python3 get-pip.py
$ sudo pip install numpy
```

5. Optimizing the OpenCV installation with NEON GPUs


```
$ nano /etc/dphys-swapfile
```
change the parameter of CONF_SWAPSIZE to 1024, and,

```
$ sudo /etc/init.d/dphys-swapfile stop
$ sudo /etc/init.d/dphys-swapfile start
```

```
$ cd ~/opencv-3.3.0/
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..
```

```
make -j4
```

## Running the program

Clone the sdp repo (master branch)

```
$ git clone https://github.com/HBRS-SDP/sdp_2018wt_P6_Raspi_Event_Detection
```

** If you are on Master machine** navigate to communication module and run master.py

```
$ cd sdp_2018wt_P6_Raspi_Event_Detection/communication/

$ python master.py
```

** If you are on Raspberry Pi** navigate to src module and run main.py

```
$ cd sdp_2018wt_P6_Raspi_Event_Detection/src
$ python main.py
```

This will give you a list of options and you may select the suitable flag for the same.