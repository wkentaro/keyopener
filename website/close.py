#!/usr/bin/env python
# -*- coding: utf-8 -*-
# close.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>
#
"""
Close the key from command line
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../code'))

from servo_2BBMG import Servo2BBMG


def main():
    servo = Servo2BBMG(pin=14)
    servo.rotate(90)


if __name__ == '__main__':
    main()
