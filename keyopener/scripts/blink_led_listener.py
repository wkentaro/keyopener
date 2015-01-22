#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rotate_servo_listener.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>
import os
import sys
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../code'))

import rospy
from std_msgs.msg import Bool

from blink_led import BlinkLed

PIN_CTRL = 13


bl = BlinkLed(PIN_CTRL)
def callback(msg):
    if msg.data is True:
        bl.on()
    else:
        bl.off()


def listener():
    rospy.init_node('blink_led_listener')
    rospy.Subscriber('/keyopener/blink_led', Bool, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
