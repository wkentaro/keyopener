#!/usr/bin/env python
# -*- coding: utf-8 -*-
# servo_2BBMG.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import time

from RPi import GPIO


def setup(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

def output_PWM(pin, pulse_width, cycle=0.02):
    """
    pulse_width : 0.00046 - 0.00222 [ms]
        0.00046[ms] : -90[deg]
        0.00135[ms] :   0[deg]
        0.00222[ms] :  90[deg]
    """
    if not 0.00045 < pulse_width < 0.00223:
        raise ValueError('Pulse width out of range.')

    try:
        while True:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(pulse_width)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(cycle - pulse_width)
    except KeyboardInterrupt:
        return

def end():
    GPIO.cleanup()
