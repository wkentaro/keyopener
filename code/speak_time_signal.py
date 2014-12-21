#!/usr/bin/env python
# -*- coding: utf-8 -*-
# speak_time_signal.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import datetime

import num2words

from speak_raspi import SpeakRaspi


def speak_time_signal():
    # get time
    now = datetime.datetime.now()
    hour = num2words.num2words(int(now.strftime('%H')))
    minute = num2words.num2words(int(now.strftime('%M')))
    # compose the sentence
    sentence = 'The time is {hour} {minute}.'.format(hour=hour, minute=minute)
    filename = 'time_signal.mp3'
    # speak raspi
    s = SpeakRaspi(sentence=sentence, filename=filename)
    s.speak()


if __name__ == '__main__':
    speak_time_signal()
