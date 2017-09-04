#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import mechanize
import urllib
from bs4 import BeautifulSoup
import requests


url_result=[]



def do_search_keyword():
    keyword = raw_input('请输入企业名称、人名、产品名称或其它关键词 ：')
    url = 'https://www.tianyancha.com/search?key=' + urllib.quote(keyword) + '&checkFrom=searchBox'

    headers = {
        'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    soup_list = BeautifulSoup(html.text, 'lxml')

    urls = soup_list.select(
        '#web-content > div > div > div > div.col-9.search-2017-2.pr10.pl0 > div.b-c-white.search_result_container > div > div.search_right_item > div.row.pb5 > div.col-xs-10.search_repadding2.f18 > a')
    for url in urls:
        url_result.append(url['href'])
    print url_result
    return url_result


def keyword_from_db():
    pass



if __name__=='__main__':
    do_search_keyword()
    if url_result:
        print 'qwe'
    else:
        print '''没有找到相关结果
        1.输入准确的关键词，重新搜索
        2.更换筛选条件，重新搜索
        3.试试“深度搜索”
        4.输入的关键词过于宽泛        '''
    # print search_result