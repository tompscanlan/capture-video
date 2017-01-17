# testing in  tompscanlan/capture-motion
# docker run  -i -t -v `pwd`:/ext capture-video  /bin/bash


import sys
import time
import datetime
import cv2
import numpy as np
from pprint import pprint
import collections


def openWriter( reader, fileName, fourcc, fps ):
    "open a VideoStream writer based on the reader dimensions"

    ret, frame = reader.read()
    if ret != True:
        throw("missed capturing a frame")

    (h,w) = frame.shape[:2]
    frameSize = (w, h)
    writer = cv2.VideoWriter(fileName, fourcc, fps, frameSize, True)
    if not writer.isOpened():
        raise Exception("failed to open writer")
    return writer

def openWriterDim( frameSize, fileName, fourcc, fps ):
    "open a VideoStream writer based on the reader dimensions"

    writer = cv2.VideoWriter(fileName, fourcc, fps, frameSize, True)
    if not writer.isOpened():
        raise Exception("failed to open writer")
    return writer

def openReader( url ):
    "open a VideoStream reader"

    reader = cv2.VideoCapture(url)

    if reader and reader.isOpened() == True:
        return reader
    else:
        raise Exception("failed to open capture")
