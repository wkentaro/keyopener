#!/usr/bin/env sh
# speak_pc.sh

wget -q -U Mozilla -O audio.mp3 "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q=hello+world"
mpg123 audio.mp3