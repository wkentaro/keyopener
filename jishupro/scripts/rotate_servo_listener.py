#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rotate_servo_listener.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>
import os
import sys
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../code'))

import rospy
from std_msgs.msg import Float32

from servo_2BBMG import Servo2BBMG

PIN_CTRL = 21


def callback(msg):
    s = Servo2BBMG(PIN_CTRL)
    s.rotate(msg.data)
    s.cleanup()


def listener():
    rospy.init_node('rotate_servo_listener')
    rospy.Subscriber('/jishupro/rotate_servo', Float32, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
