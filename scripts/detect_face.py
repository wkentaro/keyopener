#!/usr/bin/env python
# -*- coding: utf-8 -*-
# detect_face.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import sys
import time

import cv2

from take_face_pictures import TakePictures


def detect_face(frame):
    # load cascade
    cascade_files = [
        '/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml',
        '/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml',
        '/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml',
        '/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml',
        ]
    filename = cascade_files[0]
    face_cascade = cv2.CascadeClassifier(filename=filename)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect face
    faces = face_cascade.detectMultiScale(
            frame_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
        )
    print("detect {0} faces!".format(len(faces)))
    # draw rectangle around the face
    vis = frame.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(vis, (x,y), (x+w,y+h), (0,255,0), 1)
    return vis


class TakeFacePictures(TakePictures):
    def __init__(self):
        super(TakeFacePictures, self).__init__()

    def _event_handle(self):
        vis = detect_face(self.frame)
        cv2.imshow('detect_face', vis)
        cv2.waitKey(100)


def main():
    t = TakeFacePictures()
    t.capture_loop()


if __name__ == '__main__':
    main()