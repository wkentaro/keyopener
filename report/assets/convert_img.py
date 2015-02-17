#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os

files = os.listdir('.')
for file in files:
    base, ext = os.path.splitext(file)
    if ext in ['.png', '.jpeg', '.jpg']:
        os.system('convert {0} {1}.eps'.format(file, base))