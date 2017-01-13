# testing in  tompscanlan/capture-motion
# docker run  -i -t -v `pwd`:/ext capture-video  /bin/bash

import sys
import time
import datetime
import cv2
#import imutils
import numpy as np
from pprint import pprint
import collections

inMotionMin = 15
fps =10
MIN_CONTOUR_SIZE = 450
SCALE_IMAGE_X = 500
FPS_SMOOTH_RATE = 0.9
WRITE_BUFFER_LENGTH = int(inMotionMin*fps/3)

SAVE_DIR = "/ext/video_events"
url = "rtsp://admin:banggumb0@192.168.1.189:554/h264Preview_01_main"


def openWriter( reader, fileName, fourcc, fps ):
    "open a VideoStream writer based on the reader dimensions"

    ret, frame = reader.read()
    if ret != True:
        throw("missed capturing a frame")

    (h,w) = frame.shape[:2]
    frameSize = (w, h)
    #print ("opening writer shape: %s" % str(frameSize))
    #print ("opening writer fourcc: %s" % str(fourcc))
    writer = cv2.VideoWriter(fileName, fourcc, fps, frameSize, True)
    if not writer.isOpened():
        throw("failed to open writer")
    return writer

def openWriterDim( frameSize, fileName, fourcc, fps ):
    "open a VideoStream writer based on the reader dimensions"

    writer = cv2.VideoWriter(fileName, fourcc, fps, frameSize, True)
    if not writer.isOpened():
        throw("failed to open writer")
    return writer

def openReader( url ):
    "open a VideoStream reader"
    print("connect to video %s" % url)
    reader = cv2.VideoCapture(url)

    if not reader.isOpened():
        throw("failed to open capture")
    return reader

debug = False

inMotionEvent = False # is motion hapening right now?
inMotionStartTime = 0

writeBuffer = collections.deque(maxlen=WRITE_BUFFER_LENGTH)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

capture = openReader(url)
vWriter = None

# initialize the first frame in the video stream
initialFrame = None
i=0
try:
    while(True):
        t1 = cv2.getTickCount()
        i=i+1
        #Gprint(i)
        ret, frame = capture.read()
        if ret != True:
            print("missed capturing a frame");
            next


        # resize the frame, convert it to grayscale, and blur it
        x = SCALE_IMAGE_X / frame.shape[1]
        dimentions = (SCALE_IMAGE_X, int(frame.shape[0] * x))
        smallFrame = cv2.resize(frame, dimentions, interpolation = cv2.INTER_AREA)

        writeBuffer.append(smallFrame)
#        writeBuffer.append(frame)

        gray = cv2.cvtColor(smallFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if initialFrame is None:
            initialFrame = gray

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(initialFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        im2, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < MIN_CONTOUR_SIZE:
                print("found undersized countour %f" % cv2.contourArea(c))
                continue

            print("found countour %f" % cv2.contourArea(c))
            # when hitting new motion event, start timer
            #open writer, with current FPS
            if inMotionEvent == False:
                inMotionStartTime = time.perf_counter()
                print("starting motion timer: %f" % inMotionStartTime)
                inMotionEvent = True
                #vWriter = openWriter(capture, SAVE_DIR + '/savevid-' +str(i) + '.mov', fourcc, fps)
                vWriter = openWriterDim(dimentions, SAVE_DIR + '/savevid-' +str(i) + '.mov', fourcc, fps)

            # compute the bounding box for the contour, draw it on the frame,
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(smallFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if inMotionEvent == True:
            timenow = time.perf_counter()
            if ((timenow - inMotionStartTime) < inMotionMin):
                print("still in motion: %f" % (timenow - inMotionStartTime) )

                # write buffer and write frames
                print("appending %d frames of video to motion event" % len(writeBuffer))
                for f in writeBuffer:
                    vWriter.write(f)
                writeBuffer.clear()
#                vWriter.write(frame)
                #vWriter.write(smallFrame)
            else:
                # close the writer, and
                print("exiting motion event")
                vWriter.release()
                inMotionEvent = False
                initialFrame = None



        t2 = cv2.getTickCount()
        t = (t2 - t1)/cv2.getTickFrequency()
        fps = (fps * FPS_SMOOTH_RATE) + (1.0/t *(1.0 - FPS_SMOOTH_RATE))

        #print("time: %f fps: %f" % (t, fps))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

finally:
    if capture != None and capture.isOpened():
        capture.release()
    if vWriter != None and vWriter.isOpened():
        vWriter.release()
    print("released capture")


