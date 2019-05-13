import cv2
import numpy as np
import time
import argparse

#Group Member: Jullio Aguirre, Ras Hipolito, David Duong
#Date: 5/13/2019
#CST205 Final Project

"""
This code removes both blue and red from the video
and then shows the pixels that was caputered when the video
first opened when the code ran.
"""
parser = argparse.ArgumentParser()
# Input argument
parser.add_argument("--video", help = "Path to input video file. Skip this argument to capture frames from a camera.")
args = parser.parse_args()
print("Please wait while we set up camera")

# Accessing and setting up camera
video = cv2.VideoCapture(args.video if args.video else 0)

# Gives camera time to set up code
time.sleep(3)
count = 0
background = 0

# Capturing background and storing into a frame
for i in range(60):
	ret, background = video.read()

while(video.isOpened()):
	ret, webcam = video.read()
	if not ret:
		break
	count+=1

	# Converting the color space from BGR to HSV
	hsv = cv2.cvtColor(webcam, cv2.COLOR_BGR2HSV)

	# Creating filters for red and blue using BGR to HSV
	blue_hsv = np.array([30,150,50])
	blue_rgb = np.array([255,255,180])
	filter1 = cv2.inRange(hsv,blue_hsv,blue_rgb)

	red_hsv = np.array([170,120,70])
	red_rgb = np.array([180,255,255])
	filter2 = cv2.inRange(hsv,red_hsv,red_rgb)
	filter1 += filter2

	# Refining the filters to accurately find red and blue
	filter1 = cv2.morphologyEx(filter1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
	filter1 = cv2.dilate(filter1,np.ones((3,3),np.uint8),iterations = 1)
	filter2 = cv2.bitwise_not(filter2)

	# Combining res1 + res2 to generate result
	res1 = cv2.bitwise_and(background,background,mask=filter1)
	res2 = cv2.bitwise_and(webcam,webcam,mask=filter2)
	result = cv2.addWeighted(res1,1,res2,1,0)
    # To close window, press 'esc'
	cv2.imshow('CST205 Project',result)
	k = cv2.waitKey(10)
	if k == 27:
		break
