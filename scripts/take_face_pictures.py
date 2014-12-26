#!/usr/bin/env python
# -*- coding: utf-8 -*-
# take_face_pictures.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import cv2


class TakePictures(object):
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
            # # Display the resulting frame
            # cv2.imshow('camera capture', self.frame)
            # Some event
            self._event_handle()
            # End flag
            if self.end_flag is True:
                break

    def _event_handle(self):
        k = cv2.waitKey(1)
        if k == 27:
            self.end_flag = True
        elif k == ord('s'):
            cv2.imwrite('capture.png', self.frame)

    def __del__(self):
        """When everything done, release the capture"""
        self.cap.release()
        cv2.destroyAllWindows()


def main():
    t = TakePictures()
    t.capture_loop()


if __name__ == '__main__':
    main()