#!/usr/bin/env python
# -*- coding: utf-8 -*-
# servo_SG90.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import time

from RPi import GPIO


def move_pos(pin, deg, speed):
    """
    (int)     deg:  0 - 60 [deg]
    (float) speed: -1 -  1
    """
    t_start = time.time()
    duration = 0.1 * deg / 60
    while time.time() - t_start < duration:
        high_duration = 0.0015 + speed * 0.0005
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(high_duration)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.02 - high_duration)


if __name__ == '__main__':
    PIN_CTRL = 21

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_CTRL, GPIO.OUT)

    move_pos(PIN_CTRL, deg=40, speed=1)

    GPIO.cleanup()