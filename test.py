#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import mechanize
import urllib
from bs4 import BeautifulSoup
import requests

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def detag(html):
    detag = re.subn('<script[^>]*>([\w\W]*?)</script>','',html)[0]
    detag = detag.replace('&nbsp;','')
    detag = detag.replace('&amp;','&')
    detag = detag.replace("'",'|')
    detag = detag.replace('&ensp;',';')
    detag = detag.replace('\t','')
    detag = detag.replace('\n','')
    detag = detag.replace('\r','')
    detag = detag.replace('\\','/')
    detag = re.subn('<[^>]*>','',detag)[0]
    return detag.strip()

def re_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


def do_search_keyword():
    keyword = raw_input('请输入企业名称、人名、产品名称或其它关键词 ：')
    # keyword = u'user_input'
    # keyword = '北京智齿'
    # url='https://www.tianyancha.com/search?key=' +str(keyword)+ '&checkFrom=searchBox'
    url = 'https://www.tianyancha.com/search?key='+urllib.quote(keyword)+'&checkFrom=searchBox'

    headers = {
        'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    # print soup.prettify()
    urls= soup.select('#web-content > div > div > div > div.col-9.search-2017-2.pr10.pl0 > div.b-c-white.search_result_container > div > div.search_right_item > div.row.pb5 > div.col-xs-10.search_repadding2.f18 > a')
    for url in urls:
        print url['href']
if __name__=='__main__':
    do_search_keyword()
