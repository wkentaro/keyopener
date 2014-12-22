#!/usr/bin/env python
# -*- coding: utf-8 -*-
# speak_raspi.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import os


class SpeakRaspi(object):
    def __init__(self, sentence, filename):
        self.sentence = sentence
        self.filename = filename

    def _get_audio(self):
        """get mp3 audio"""
        q = '+'.join(self.sentence.split(' '))
        os.system('wget -q -U Mozilla -O {0} "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q={1}"'.format(self.filename, q))

    def _play_audio(self):
        """play audio"""
        os.system('mpg123 -q {0}'.format(self.filename))

    def _cleanup(self):
        os.system('rm {0}'.format(self.filename))

    def speak(self):
        """main function"""
        self._get_audio()
        self._play_audio()
        self._cleanup()