#!/usr/bin/env python
# -*- coding: utf-8 -*-
# face_classifier.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import os
import sys
import collections

from sklearn import svm
import cv2


class FaceClassifier(object):
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.img_dict = collections.defaultdict(list)
        self._lookup_imgs()

    def _lookup_imgs(self):
        face_dirs = os.listdir(self.data_dir)
        for face_dir in face_dirs:
            face_dir_abs = os.path.join(self.data_dir, face_dir)
            if not os.path.isdir(face_dir_abs):
                continue
            for img in os.listdir(face_dir_abs):
                base, ext = os.path.splitext(img)
                if ext not in ['.png', '.pgm']:
                    continue
                self.img_dict[face_dir].append(
                        os.path.join(self.data_dir, face_dir, img))


def main():
    data_dir = '../data/cropped'
    face_clf = FaceClassifier(data_dir=data_dir)
    for person, img_path in face_clf.img_dict.items():
        img = cv2.imread(img_path[0])
        print img_path[0]
        cv2.imshow('cropped img', img)
        k = cv2.waitKey(0)
        if k == 27:
            continue
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
