#!/usr/bin/env python
# -*- coding:utf-8 -*-
# speak_raspi_listener.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>
import os
import sys
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../code'))

import rospy
from std_msgs.msg import String

from speak_raspi import SpeakRaspi


def callback(msg):
    print msg.data
    s = SpeakRaspi()
    s.speak(sentence=msg.data)


def listener():
    rospy.init_node('speak_raspi_listener')
    rospy.Subscriber('/jishupro/speak_raspi', String, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()