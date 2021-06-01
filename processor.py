#!/usr/bin/env python
import imutils
import cv2 
import numpy as np


frame_buf = None

def motion_detect(frame, firstFrame,min_area, channel):
    #print('min_area ', min_area)
    text = "Unoccupied"
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    gray2 = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
	# compute the absolute difference between the current frame and
	# first frame
    
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
       #continue

    frameDelta = cv2.absdiff(gray2, gray)
    thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
	# loop over the contours
    for c in cnts:
		# if the contour is too small, ignore it
	    if cv2.contourArea(c) < int(min_area):
		    continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
	    (x, y, w, h) = cv2.boundingRect(c)
	    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	    text = "Occupied"

    	# draw the text  on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 255), 2)

    out_frame = frame

    if channel == 0: out_frame = frame 
  
    if channel == 1: out_frame = frameDelta
  
    if channel == 2: out_frame = thresh 


    return out_frame