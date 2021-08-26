##########################################
## Author: Piotr Szczypta               ##
## Lidar L515 distance on image         ##
## Company: A4BEE                       ##
##########################################

from intel_class import *
import sys

# Show distance with mouse function
def show_distance(event, x, y, args, params):
    global point
    point = (x, y)


cv.namedWindow("Distance image")
cv.setMouseCallback("Distance image", show_distance)

# The starting point is the center of the image
point = (int(int(param['stream-width'])/2), int(int(param['stream-height'])/2))

# Initialize Camera Intel Realsense
try:
    ld = LidarDistance()
except RuntimeError as err:
    print("ERROR: ", err)
    print("You probably didn't connect a dedicated intel camera")
    cv.destroyAllWindows()
    sys.exit(0)
    
try:
    while True:
        
        
# =============================================================================
#         Comment out the method that you do not want to use at the moment.
#         get_frame_depth () - display distance in the depth image
#         get_frame_rgb () - get distance on rgb image
# =============================================================================

        # Wait for a depth frame
        # main_frame, frame_mm = ld.get_frame_depth()
        main_frame, frame_mm, depth_frame = ld.get_frame_rgb()
        
        # get distance   
        distance = ld.get_distance(frame_mm, point)
        
        # Create circle in mouse position and put the text with actuall distance in mm       
        cv.circle(main_frame, point, 3, (0, 0, 255), -1)
        cv.putText(main_frame, "{}mm".format(distance), (point[0], point[1] - 10), cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        # Show image
        cv.imshow('Distance image', main_frame)
        try:
            cv.imshow('Distance image d', depth_frame)
        except:
            pass
    
        key = cv.waitKey(1)
        k = cv.waitKey(1) & 0xff
        if k == 27:
            ld.stop_stream()
            cv.destroyAllWindows()
            break
        
except RuntimeError as err:
    print("ERROR: ", err)
    print("You probably haven't turned off streaming in the program Intel RealSense Viewer or you lost connection to the camera")
    cv.destroyAllWindows()
    sys.exit(0)
            