import cv2
import numpy as np


def resize_image(image, scale_percent=50):

    # Calculate the 50 percent of original dimensions
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)

    size = (width, height)

    result_image = cv2.resize(image, size)

    return result_image


# Lucas kanade params
lk_params = dict(winSize = (15, 15),
		 		 maxLevel = 4,
				 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


def initialize_optical_flow(event, x, y, flags, params):
	global points, calculate_optical_flow, old_points, keypoints
	
	if event == cv2.EVENT_LBUTTONDOWN:
		
		calculate_optical_flow = True
		points = []
		
		for features in keypoints:
			points.append((features.pt[0],features.pt[1]))
		
		old_points = np.array(points, dtype=np.float32)
		print (len(old_points))


def select_features(frame):	
	global keypoints
	
	fast_feaure_detector = cv2.FastFeatureDetector_create()
	fast_feaure_detector.setThreshold(100)
	keypoints = fast_feaure_detector.detect(frame,None)
	frame = cv2.drawKeypoints(frame, keypoints, frame, (255,0,0))
	

# Initializing
video = cv2.VideoCapture('sample_video.mp4')

_, frame = video.read()
frame = resize_image(frame)
old_gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cv2.namedWindow("Frame")

# Everytime someone clicks on the window this will run
cv2.setMouseCallback("Frame", initialize_optical_flow)

calculate_optical_flow = False
points = []
keypoints = ()
old_points = np.array([[]])

select_features(frame)


# Reading the Video
while True:
	_, frame = video.read()
	frame = resize_image(frame)
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# if point_selected is False:
	select_features(frame)

	if calculate_optical_flow is True:
		new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray_frame, gray_frame, old_points, None, **lk_params)
		old_gray_frame = gray_frame.copy()
		
		# Index to optimaze the for loop
		index = 0
		for new_point in new_points:

			# New points
			x, y = new_point.ravel()
			x = int(x)
			y = int(y)

			# Selected Points when you click the mouse
			xp = int(points[index ][0])
			yp = int(points[index ][1])
			
			# Euclidian distance between the new points and the selected points so it can control the arrow's size
			if(np.sqrt((x-xp) * (x-xp) + (y-yp) * (y-yp)) > 100):
				points[index ]=(x,y)

			# Opticalflow representation
			cv2.arrowedLine(frame,(xp,yp),(x,y),(0, 0, 255),2)
			cv2.circle(frame, (x, y), 5, (255, 0, 0), 0)
			
			old_points = new_points
			index  = index  + 1

	cv2.imshow("Frame", frame)

	key = cv2.waitKey(1)
	esc = 27
	if key == esc:
		break

# Ending
video.release()
cv2.destroyAllWindows()