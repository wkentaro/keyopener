#!/usr/bin/env python
# -*- coding: utf-8 -*-
# blink_led.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import time

from RPi import GPIO


class BlinkLed(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        time.sleep(1)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()


if __name__ == '__main__':
    PIN_CTRL = 13
    bl = BlinkLed(PIN_CTRL)
    bl.on()
    time.sleep(1)
    bl.off()
    bl.cleanup()