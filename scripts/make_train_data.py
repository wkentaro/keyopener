#!/usr/bin/env python
# -*- coding: utf-8 -*-
# make_train_data.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import os
import sys
import time

import cv2

from take_face_photos import TakeFacePhotos


def make_train_data():
    raw_dir = '../data/raw'
    for fl in os.listdir(raw_dir):
        if not fl.endswith('.png'):
            continue
        img = cv2.imread(os.path.join(raw_dir, fl))
        faces = TakeFacePhotos.detect_face(img)
        if len(faces) != 1:
            continue
        x, y, w, h = faces[0]
        cropped = img[y:y+h, x:x+w]
        # save cropped
        filename = os.path.join('../data/positive', fl)
        cv2.imwrite(filename, cropped)


if __name__ == '__main__':
    make_train_data()