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
def detag(html):
    detag = re.subn('<[^>]*>', ' ', html)[0]
    detag = detag.replace('\\u\w{4}', ' ')
    detag = detag.replace('{', ' ')
    detag = detag.replace('}', ' ')
    detag = detag.replace('"', ' ')
    # detag = detag.replace(' ','')
    detag = detag.replace('\n','')
    detag = detag.replace('\t','')

    return detag


def re_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


source='''
<html>
 <head></head>
 <body>
  <!-- <td><span class="serial-num" >{{initCompanyIndex((punishCurrentPage-1)*5+$index +1) }}</span></td>-->
  <span class=" text-dark-color ">2017-07-27</span>
  <span class=" text-dark-color ">未经备案网站提供互联网接入服务</span>
  <span class=" text-dark-color c-none"> </span>
  <div class="text-dark-color more-overflow2 " style="width: 100%;">
   北京市通信管理局
  </div>
  <span class="text-click-color point companyinfo_show_more_btn" event-name="company-detail-punishPopup" href-event="" ng-click="punishOpen(companyeq);" onclick="openPunishPopup({&quot;content&quot;:&quot;处1万元罚款&quot;,&quot;punishNumber&quot;:&quot;未经备案网站提供互联网接入服务&quot;,&quot;regNum&quot;:&quot;91110000802100433B&quot;,&quot;name&quot;:&quot;北京百度网讯科技有限公司&quot;,&quot;base&quot;:&quot;bj&quot;,&quot;decisionDate&quot;:&quot;2017-07-27&quot;,&quot;legalPersonName&quot;:&quot;梁志祥&quot;,&quot;type&quot;:&quot;&quot;,&quot;departmentName&quot;:&quot;北京市通信管理局&quot;,&quot;publishDate&quot;:&quot;2017-07-27&quot;})">详情 》</span> 
 </body>
</html>
'''


date = re_findall('<span class=".*?">(.*?)</span>', source )[0]
Judgment_document_url = re_findall('href="(.*?)" href-new-event', source )[0]
Judgment_document_name = re_findall('target="_blank">(.*?)</a>', source )[0]
cause = re_findall('<span class=".*?">(.*?)</span>', source )[1]
identity = detag(re_findall('<div class="text-dark-color">(.*?)</div>', source )[0])
docket_number = re_findall('<span class=".*?">(.*?)</span>', source )[2]

print date
print Judgment_document_name
print Judgment_document_url
print cause
print identity
print docket_number