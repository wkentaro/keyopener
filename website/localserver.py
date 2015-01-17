#!/usr/bin/env python
# -*- coding: utf-8 -*-
# localserver.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>
#
from main import *

def localserver():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    localserver()