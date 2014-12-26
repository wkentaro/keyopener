#!/usr/bin/env python
# -*- coding: utf-8 -*-
# detect_face.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import os
import sys
import time

import cv2

from take_photos import TakePhotos


class TakeFacePhotos(TakePhotos):
    def __init__(self):
        super(TakeFacePhotos, self).__init__()
        self.face_exists = False

    def _event_handle(self):
        faces = self.detect_face(self.frame)
        if len(faces) > 1:
            self.face_exists = True
        vis = self._draw_face_rect(faces)
        if self.face_exists is True:
            self._save_frame()
        cv2.imshow('detect_face', vis)
        k = cv2.waitKey(100)
        if k == 27:
            self.end_flag = True

    def _draw_face_rect(self, faces):
        # draw rectangle around the face
        vis = self.frame.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(vis, (x,y), (x+w,y+h), (0,255,0), 1)
        return vis

    @classmethod
    def detect_face(self, img):
        # load cascade
        cascade_files = [
            '/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml',
            '/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml',
            '/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml',
            '/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml',
            ]
        filename = cascade_files[0]
        face_cascade = cv2.CascadeClassifier(filename=filename)
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # detect face
        faces = face_cascade.detectMultiScale(
                imgray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
            )
        return faces


def main():
    t = TakeFacePhotos()
    t.capture_loop()


if __name__ == '__main__':
    main()