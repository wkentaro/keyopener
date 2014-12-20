#!/usr/bin/env python
# -*- coding: utf-8 -*-
# servo_2BBMG.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import time

from RPi import GPIO


class Servo(object):
    def __init__(self, pin):
        self.pin = pin
        self.pos = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def _output_pulse(self, pulse_width, duration, cycle=0.02):
        """Standard Servo Control
        pulse_width : 0.00046 - 0.00222 [ms]
            0.00046[ms] :  90[deg]
            0.00135[ms] :   0[deg]
            0.00222[ms] : -90[deg]
        """
        if not 0.00045 < pulse_width < 0.00223:
            raise ValueError('Pulse width out of range.')

        t_start = time.time()
        while time.time() - t_start < duration:
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(pulse_width)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(cycle - pulse_width)

    def cleanup(self):
        GPIO.cleanup()


class Servo2BBMG(Servo):
    def rotate(self, deg):
        pulse_width = (0.00222 - 0.00046) / (-180.) * deg + 0.00134
        if self.pos is None:
            duration = 0.69
        else:
            duration = abs(deg - self.pos) / 60. * 0.23
        self._output_pulse(pulse_width=pulse_width, duration=duration)
