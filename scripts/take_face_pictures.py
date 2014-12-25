#!/usr/bin/env python
# -*- coding: utf-8 -*-
# take_face_pictures.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import cv2


class TakeFacePictures(object):
    def __init__(self):
        """Initialize camera"""
        self.cap = cv2.VideoCapture(0)
        self.end_flag = False
        self.frame = None

    def capture_loop(self, mirror=True, size=None):
        """Capturing camera loop"""
        while True:
            # Capture frame-by-frame
            ret, self.frame = self.cap.read()
            # Act like mirror or not
            if mirror is True:
                self.frame = self.frame[:,::-1]
            # Resize frame
            if size is not None and len(size) == 2:
                self.frame = cv2.resize(self.frame, size)
            # Display the resulting frame
            cv2.imshow('camera capture', self.frame)
            # Key event
            self._key_event(cv2.waitKey(1))
            # end flag
            if self.end_flag is True:
                break

    def _key_event(self, k):
        if k == 27:
            self.end_flag = True
        elif k == ord('s'):
            cv2.imwrite('capture.png', self.frame)

    def __del__(self):
        """When everything done, release the capture"""
        cap.release()
        cv2.destroyAllWindows()