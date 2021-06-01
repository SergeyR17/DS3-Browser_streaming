#!/usr/bin/env python
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask
import cv2 
import urllib
import numpy as np
from processor import motion_detect

# take MJPEG stream and preprocess it

SOURCE_URL = "your link to video source"



class Receiver(object):
  

    def __init__(self):
        self.capture=cv2.VideoCapture(SOURCE_URL)

    def get_frame(self, min_area, channel):
        buf1 = self.capture.read()[1]
        buf2 = self.capture.read()[1]
        buf = motion_detect(buf1, buf2, min_area, channel)

        
        jpeg_frame = cv2.imencode('.jpg', buf.astype(np.uint8))[1].tobytes() # returns single-row matrix of type CV_8UC1 that contains encoded image as array of bytes.
        return jpeg_frame

