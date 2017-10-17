#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import re
import os
from multiprocessing import Pool
import json
import hashlib
import datetime
import MySQLdb
import time
import csv
from bs4 import BeautifulSoup
import requests
import urllib

from requests.packages.urllib3.exceptions import InsecureRequestWarning

corp_name = u'春节'
tongji_url = "https://www.tianyancha.com/tongji/" + urllib.quote(corp_name.encode('utf8')) + ".json?_="
print tongji_url