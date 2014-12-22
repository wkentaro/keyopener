#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rotate_servo_listener.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>
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
    rospy.Subscriber('/jishu_pro/rotate_servo', Float32, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
