#!/usr/bin/env python
# -*- coding: utf-8 -*-
# blink_led.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import rospy

from RPi import GPIO


class BlinkLED(object):
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def blink(self):
        GPIO.output(pin, GPIO.HIGH)


if __name__ == '__main__':
    PIN_CTRL = 17
    bl = BlinkLED(PIN_CTRL)
    bl.blink()