#!/usr/bin/env python
# -*- coding: utf-8 -*-
# make_cropped.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import os
import sys
import time

import cv2

from take_face_photos import TakeFacePhotos

RAW_DIR = '../data/raw'
CROPPED_DIR = '../data/cropped'
CROP_SQUARE_SIZE = 100


def make_cropped(raw_path):
    cropped_path = os.path.join(CROPPED_DIR,
            os.path.basename(raw_path))
    print 'cropped_path', cropped_path
    # confirm cropped dir is exists
    if not os.path.isdir(cropped_path):
        os.mkdir(cropped_path)
    # crop all images in the raw dir
    for fl in os.listdir(raw_path):
        # about file extentions
        base, ext = os.path.splitext(fl)
        if ext not in ['.pgm', '.png']:
            continue
        # load img and detect face
        img = cv2.imread(os.path.join(raw_path, fl))
        faces = TakeFacePhotos.detect_face(img)
        if len(faces) != 1:
            continue
        x, y, w, h = faces[0]
        cropped = img[y:y+h, x:x+w]  # crop the face part
        cropped_gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        # pass too small face and resize others
        if cropped_gray.shape[0] < CROP_SQUARE_SIZE or \
           cropped_gray.shape[1] < CROP_SQUARE_SIZE:
            continue
        else:
            cropped_gray = cv2.resize(cropped_gray,
                    (CROP_SQUARE_SIZE, CROP_SQUARE_SIZE))
        # save cropped
        filename = os.path.join(cropped_path, base+'.png')
        cv2.imwrite(filename, cropped_gray)
        print "saved to", filename


if __name__ == '__main__':
    for raw_dir in os.listdir(RAW_DIR):
        raw_path = os.path.join(RAW_DIR, raw_dir)
        if not os.path.isdir(raw_path):
            continue
        print 'raw_path', raw_path
        make_cropped(raw_path)