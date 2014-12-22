#!/usr/bin/env python
# -*- coding: utf-8 -*-
# raspi.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import rospy

from std_msgs.msg import (
    Float32,
    String,
)

from servo_2BBMG import Servo2BBMG
from speak_raspi import SpeakRaspi


class Raspi(object):
    def __init__(self):
        pb_rotate_servo = rospy.Publisher('/jishu_pro/rotate_servo', Float32)
        pb_speak = rospy.Publisher('/jishu_pro/speak_raspi', String)

    def speak(self, sentence):
        pb_speak.publish(String(sentence))

    def rotate_servo(self, deg):
        pb_rotate_servo.publish(Float32(deg))


if __name__ == '__main__':
    raspi = Raspi()
    raspi.speak('Hello, Raspi!')
    raspi.rotate_servo(50)
    raspi.rotate_servo(-50)