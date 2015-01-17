#!/usr/bin/env python
# -*- coding: utf-8 -*-
# close.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>
#
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../code'))

from servo_2BBMG import Servo2BBMG

s = Servo2BBMG(pin=14)
s.rotate(-90)