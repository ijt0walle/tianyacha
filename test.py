#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

print str(datetime.datetime.now())[:10]

print type(str(datetime.datetime.now())[:10])

print str(datetime.datetime.now()).decode('utf-8')

# print type(str(datetime.datetime.now()))