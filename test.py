#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import mechanize
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
    # keyword = raw_input('请输入企业名称、人名、产品名称或其它关键词 ：')
    keyword = '北京智齿'
    # url='https://www.tianyancha.com/search?key=' +str(keyword)+ '&checkFrom=searchBox'
    url = 'https://www.tianyancha.com/search?key='+keyword+'&checkFrom=searchBox'

    br = mechanize.Browser()
    br.addheaders = [
        ('Accept', 'application/json, text/javascript, */*; q=0.01') \
        , ('Accept-Encoding', 'gzip, deflate, br') \
        , ('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6') \
        , ('Connection', 'keep-alive') \
        , ('Cookie',
           'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719;ssuid=6805162414; RTYCID=d6928b5fe88243489ad83678134a5e06; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODU1MTk4NjYyNSIsImlhdCI6MTUwNDE0NDg1MCwiZXhwIjoxNTE5Njk2ODUwfQ.ChipyAlCl7j08qBgYW8nsR46mIs91UTI80IftelNgjDf59KZ6JWWQm9BDonBKsl5UKyO44PtnzV1olf-RjUXMQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218551986625%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODU1MTk4NjYyNSIsImlhdCI6MTUwNDE0NDg1MCwiZXhwIjoxNTE5Njk2ODUwfQ.ChipyAlCl7j08qBgYW8nsR46mIs91UTI80IftelNgjDf59KZ6JWWQm9BDonBKsl5UKyO44PtnzV1olf-RjUXMQ; aliyungf_tc=AQAAAIrjRh3IugIAlaRf3sGFCOfYdqPV; csrfToken=sWaDXU2nJB0QKqUAV0D8XSzN; bannerFlag=true; OA=e+gaygcWZ84c32kAIH2c9feRsbYPaO9so59OI1hKLF4bER8rcljLYdw2EDQSPJZc; _csrf=HzN2RRmaxND842F/ICyCpQ==; _csrf_bk=e73360ec0593474650ab26dac3b35170; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504176400') \
        , ('Host', 'www.tianyancha.com') \
        , ('Referer', 'https://www.tianyancha.com/search?key='+keyword+'&checkFrom=searchBox') \
        , ('User-Agent',
           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36') \
        , ('X-Requested-With', 'XMLHttpRequest') \
        ]

    html = br.open(url).read()
    soup = BeautifulSoup(html, 'lxml')

    print soup.prettify()

    # for i in range(1,21):
    #
    #     txt = soup.select(
    #         '#web-content > div > div > div > div.col-9.search-2017-2.pr10.pl0 > div.b-c-white.search_result_container > div:nth-of-type('+str(i)+')  > div.search_right_item > div.row.pb5 > div.col-xs-10.search_repadding2.f18 > a')[
    #         0]['href']
    #     print txt
    #     # if txt:
        #     print 'you'
        # else:
        #     print 'no'
    # for result_list in result_lists :
    #     for i in result_list:
    #         print i

if __name__=='__main__':
    do_search_keyword()
