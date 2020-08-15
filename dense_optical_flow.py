import cv2
import numpy as np


def resize_image(image, scale_percent=50):

    # Calculate the 50 percent of original dimensions
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)

    size = (width, height)

    result_image = cv2.resize(image, size)

    return result_image


video = cv2.VideoCapture("sample_video.mp4")
_, first_frame = video.read()
first_frame = resize_image(first_frame)
old_gray_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

# Mask is hsv and the direction orresponds to Hue value of the image
mask = np.zeros_like(first_frame)
mask[..., 1] = 255

while(video.isOpened()):
    _, frame = video.read()
    frame = resize_image(frame)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculates dense optical flow by Farneback method
    flow = cv2.calcOpticalFlowFarneback(old_gray_frame, gray_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    #  Magnitude corresponds to Value plane
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    
    # Sets image hue according to the optical flow direction
    mask[..., 0] = angle * 180 / np.pi / 2
    
    # Sets image value according to the optical flow magnitude (normalized)
    mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    
    # Converts HSV to RGB (BGR) color representation
    rgb_frame = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
    
    cv2.imshow("dense optical flow", rgb_frame)
    
    # Updates previous frame
    old_gray_frame = gray_frame

    key = cv2.waitKey(1)
    esc = 27
    if key == esc:
        break

# Ending
video.release()
cv2.destroyAllWindows()