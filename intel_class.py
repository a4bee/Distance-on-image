##########################################
## Author: Piotr Szczypta               ##
## Lidar L515 distance on image         ##
## Company: A4BEE                       ##
##########################################

import cv2 as cv
import pyrealsense2 as rs
import numpy as np
import json

# Some of the parameters are set from the loaded configuration file
file = "Lidar_param_1.json"
param = json.load(open(file))

class LidarDistance:
    
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()
        
        # Set depth and color size, format and fps
        freq=int(param['stream-fps'])
        print("Loaded data from file: {}".format(file))
        print("Width: ", int(param['stream-width']))
        print("Height: ", int(param['stream-height']))
        print("FPS: ", int(param['stream-fps']))
        config.enable_stream(rs.stream.depth, int(param['stream-width']), int(param['stream-height']), rs.format.z16, freq)
        
        # Resolution of RGB is set manually. Available sizes {960x540, 1280x720, 1920x1080}
        config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, freq)

        # Start streaming
        profile = self.pipeline.start(config)
        
        # Get device
        dev = profile.get_device()
        depth_sensor = dev.query_sensors()[0]

        # Set laser power
        print("L Pow: ", float(param['Laser Power']))
        depth_sensor.set_option(rs.option.laser_power, float(param['Laser Power']))
        
        # Set minimal distance
        print("Min dist: ", float(param['Min Distance']))
        depth_sensor.set_option(rs.option.min_distance, float(param['Min Distance']))
        
        print("Noise f: ", float(param['Noise Filtering']))
        depth_sensor.set_option(rs.option.noise_filtering, float(param['Noise Filtering']))
        
        print("Post proc sharp: ", float(param['Post Processing Sharpening']))
        depth_sensor.set_option(rs.option.post_processing_sharpening, float(param['Post Processing Sharpening']))
        
        print("Pre proc sharp: ", float(param['Pre Processing Sharpening']))
        depth_sensor.set_option(rs.option.pre_processing_sharpening, float(param['Pre Processing Sharpening']))
        
        print("\n Press esc to exit")
    
    # Returns colorized depth frame and table with distances in mm
    def get_frame_depth(self):
        
        frameset = self.pipeline.wait_for_frames()
        depth_frame = frameset.get_depth_frame()
        # color_frame = frames.get_color_frame()

        #Initialize colorizer class
        colorizer = rs.colorizer()
        # Convert images to numpy arrays, using colorizer to generate appropriate colors
        depth_frame_c = np.asanyarray(colorizer.colorize(depth_frame).get_data())
        
        # Get depth table with distances
        depth_frame_1 = np.asanyarray(depth_frame.get_data())
        
        # Convert inches to mm and rounding to 2 decimal places
        depth_frame_mm = np.where(depth_frame_1 * 0.0254 * 10 < 2, depth_frame_1, depth_frame_1 * 0.0254 * 10 - 2).round(2)


        return depth_frame_c, depth_frame_mm
    
    # Returns rgb frame, table with distances in mm and align, colorized depth frame
    def get_frame_rgb(self):
        
        frameset = self.pipeline.wait_for_frames()
        color_frame = frameset.get_color_frame()
        depth_frame = frameset.get_depth_frame()
        
        #Initialize colorizer class
        colorizer = rs.colorizer()
        
        color = np.asanyarray(color_frame.get_data())
        res = color.copy()
        # hsv = cv.cvtColor(color, cv.COLOR_BGR2HSV)
        hsv = cv.cvtColor(color, cv.COLOR_BGR2HSV)

        l_b = np.array([24, 133, 48])
        u_b = np.array([39, 200, 181])

        mask = cv.inRange(hsv, l_b, u_b)
        color = cv.bitwise_and(color, color, mask=mask)
        
        # Align images
        align = rs.align(rs.stream.color)
        frameset = align.process(frameset)

        # Update color and depth frames:
        aligned_depth_frame = frameset.get_depth_frame()
        depth_frame_c = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data())
        
        depth_frame_1 = np.asanyarray(aligned_depth_frame.get_data())
        #Convert inches to mm
        depth_frame_mm = np.where(depth_frame_1 * 0.0254 * 10 < 2, depth_frame_1, depth_frame_1 * 0.0254 * 10 - 2).round(2)
        
        return res, depth_frame_mm, depth_frame_c
    
    # Returns the distance in millimeters from the acquired current mouse position
    def get_distance(self, frame_mm, point):
        
        distance = frame_mm[point[1], point[0]]
        
        return distance
    
    # Stop streaming
    def stop_stream(self):
        self.pipeline.stop()