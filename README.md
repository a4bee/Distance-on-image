# Lidar L515 distance on image 
## Overview
The repository contains a class and a control program written in python for checking the distance in mm in the image using the Intel RealSense LiDAR L515 camera. Using the mouse cursor, move the mouse over one and the next value directly at the cursor. This is possible because the camera has access to a depth camera which is used to use a beam radius that has the actual distance from the object. 

## Requirements
- Installing the appropriate libraries (OpenCV, pyrealsense2, numpy, json)
- The Intel RealSense LiDAR Camera L515 connection (tested on Windows 10)

## Preparatory Steps
1. Clone repository
2. Copy the intel_class.py, intel_class.py, Lidar_param_1.json to the one folder
3. You can set your own parameters in the json file, or download the settings file through the dedicated Intel RealSense Viewer program. The current settings are for close-up targets and may not capture more targets.
4. At the beginning of a while loop, comment out the method that you do not want to use at the moment.

## Program description
1. The **```intel_class.py```** A class for taking frames from an intel camera and returning properly processed information from them. The constructor reads some of the most important parameters from the json file.

2. The **```intel_object.py```** The program creates an object of the class and takes the appropriately selected method in the main while loop, depending on the choice. The image is displayed with point and distance depending on the position of the mouse.

## Class methods:

- ``get_frame_depth()`` - Returns an array of depth map pixels to display, also returns an array of distances converted to mm.
- ``get_frame_rgb()`` - Returns an array of rgb pixels to display, returns an array of distances converted to mm, and also returns an array of depth map pixels for possible comparison. **IMPORTANT!**
Depth image and RGB are displayed from two separate cameras. Cameras, due to the fact that they are shifted from each other, do not give the same image, in addition, they have different resolutions.
The align function built into the realsense library comes with a slight help here, which adjusts the resolution of the image depth to the rgb image and aligns the pixels. The disadvantage of this solution is the transformation of the depth image, especially in places with large details. With this solution, you have to take into account that in some places in the image, the distances may be slightly distorted.
- ``get_distance(frame_mm, point)`` - Returns the distance in millimeters from the acquired current mouse position
- ``def stop_stream()`` - Stop streaming

## Example usage:
When you run the program, make sure you have your camera running, you can get one of the two output images depending on which method in your code is uncommented.

![depth_image](depth_image.gif)
![rgb_image](rgb_image.gif)



