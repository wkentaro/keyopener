#!/usr/bin/env python
# -*- coding: utf-8 -*-
# raspi.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import rospy

from std_msgs.msg import (
    Float32,
    String,
)


class Raspi(object):
    def __init__(self):
        rospy.init_node('raspi_interface')
        self.pb_rotate_servo = rospy.Publisher('/jishu_pro/rotate_servo', Float32, queue_size=10)
        self.pb_speak = rospy.Publisher('/jishu_pro/speak_raspi', String, queue_size=10)
        rospy.sleep(1)

    def speak(self, sentence):
        self.pb_speak.publish(String(sentence))
        rospy.sleep(3)

    def rotate_servo(self, deg):
        self.pb_rotate_servo.publish(Float32(deg))
        rospy.sleep(1)


if __name__ == '__main__':
    raspi = Raspi()
    raspi.speak('Hello, Raspi!')
    raspi.rotate_servo(50)
    raspi.rotate_servo(-50)