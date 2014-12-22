#!/usr/bin/env python
# -*- coding:utf-8 -*-
# speak_raspi_listener.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>
import rospy
import speak_raspi

def callback(msg):
    print msg


def listener():
    rospy.init_node('speak_raspi_listener')
    rospy.Subscriber('/jishu_pro/speak_raspi', str)
    rospy.spin()


if __name__ == '__main__':
    listener()