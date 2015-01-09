#!/usr/bin/env python
# -*- coding: utf-8 -*-
# servo_2BBMG.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import time
from RPi import GPIO

from servo import Servo


class Servo2BBMG(Servo):
    def rotate(self, deg):
        pulse_width = (0.00222 - 0.00046) / (-180.) * deg + 0.00134

        if self.pos is None:
            duration = 0.69
        else:
            duration = abs(deg - self.pos) / 60. * 0.23

        self._output_pulse(pulse_width=pulse_width, duration=duration)
        self.pos = deg


if __name__ == '__main__':
    s = Servo2BBMG(pin=21)
    while True:
        try:
            s.rotate(-90)
            time.sleep(2)
            s.rotate(90)
            time.sleep(2)
        except KeyboardInterrupt:
            s.cleanup()
            break
