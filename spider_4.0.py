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

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

static_js_code = """
var ne = "2633141825201321121345332721524273528936811101916293117022304236|1831735156281312241132340102520529171363214283321272634162219930|2332353860219720155312141629130102234183691124281413251227261733|2592811262018293062732141927100364232411333831161535317211222534|9715232833130331019112512913172124126035262343627321642220185148|3316362031032192529235212215274341412306269813312817111724201835|3293412148301016132183119242311021281920736172527353261533526224|3236623313013201625221912357142415851018341117262721294332103928|2619332514511302724163415617234183291312001227928218353622321031|3111952725113022716818421512203433241091723133635282932601432216";
var base64chars = "abcdefghijklmnopqrstuvwxyz1234567890-~!";
var _0x4fec = "f9D1x1Z2o1U2f5A1a1P1i7R1u2S1m1F1,o2A1x2F1u5~j1Y2z3!p2~r3G2m8S1c1,i3E5o1~d2!y2H1e2F1b6`g4v7,p1`t7D3x5#w2~l2Z1v4Y1k4M1n1,C2e3P1r7!s6U2n2~p5X1e3#,g4`b6W1x4R1r4#!u5!#D1f2,!z4U1f4`f2R2o3!l4I1v6F1h2F1x2!,b2~u9h2K1l3X2y9#B4t1,t5H1s7D1o2#p2#z1Q3v2`j6,r1#u5#f1Z2w7!r7#j3S1";
rs_decode = function(e) {
    return ne.split("|")[e]
};
    var r = t+"";
    r = r.length > 1 ? r[1] : r;
    for (var i = rs_decode(r), o = _0x4fec.split(",")[r], a = [], s = 0, u = 0; u < o.length; u++) {
        if ("`" != o[u] && "!" != o[u] && "~" != o[u] || (a.push(i.substring(s, s + 1)), s++), "#" == o[u] && (a.push(i.substring(s, s + 1)), a.push(i.substring(s + 1, s + 3)), a.push(i.substring(s + 3, s + 4)), s += 4), o.charCodeAt(u) > 96 && o.charCodeAt(u) < 123) for (var l = o[u + 1], c = 0; c < l; c++) a.push(i.substring(s, s + 2)),
        s += 2;
        if (o.charCodeAt(u) > 64 && o.charCodeAt(u) < 91) for (var l = o[u + 1], c = 0; c < l; c++) a.push(i.substring(s, s + 1)),
        s++
    }
    rsid = a;
for (var chars = "",  i = 0; i < rsid.length; i++) chars += base64chars[rsid[i]];
for (var fxck = wtf.split(","), fxckStr = "", i = 0; i < fxck.length; i++) fxckStr += chars[fxck[i]];
var utm = fxckStr;
console.log("{\\"utm\\":\\""+utm+"\\",\\"ssuid\\":\\""+Math.round(2147483647 * Math.random()) * (new Date).getUTCMilliseconds() % 1e10+"\\"}")
phantom.exit();
"""


# 清洗数据(去除文本中的<em><br/>
def detag(html):
    detag = re.subn('<[^>]*>', ' ', html)[0]
    detag = re.subn('\\\\u\w{4}', ' ', detag)[0]
    detag = detag.replace('{', '')
    detag = detag.replace('}', '')
    detag = detag.replace('"', '')
    detag = detag.replace(' ', '')
    detag = detag.replace('\n', '.')
    detag = detag.replace('\t', '')

    return detag


# 获取代理
def get_proxy():
    proxy_list = list(set(urllib.urlopen(
        'http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static').read().split('\n')[
                          :-1]))
    index = random.randint(0, len(proxy_list) - 1)
    current_proxy = proxy_list[index]
    print "NEW PROXY:\t%s" % current_proxy
    proxies = {"http": "http://" + current_proxy, "https": "http://" + current_proxy, }
    return proxies


def re_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


def execCmd(cmd):
    text = os.popen(cmd).read()
    return (text)


# ==================================
# ------------各个模块获取------------
# ==================================


## 工商信息
def business_info(html):
    print u'爬取工商信息  ' + str(datetime.datetime.now())
    soup = BeautifulSoup(html.text, 'lxml')
    # 注册资本
    registered_capital = soup.select(
        '#_container_baseInfo > div > div.baseInfo_model2017 > table > tbody > tr > td:nth-of-type(2) > div:nth-of-type(1) > div.pb10 > div')[
        0].text
    # print registered_capital

    # 注册时间
    registration_time = soup.select(
        '#_container_baseInfo > div > div.baseInfo_model2017 > table > tbody > tr > td:nth-of-type(2) > div.new-border-bottom.pt10 > div.pb10 > div')[
        0].text
    # print registration_time

    # 企业状态
    company_status = soup.select(
        '#_container_baseInfo > div > div.baseInfo_model2017 > table > tbody > tr > td:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div')[
        0].text
    # print company_status

    # 工商注册号
    business_registration_number = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2)')[0].text
    # print business_registration_number

    # 组织机构代码
    organization_code = soup.select(

        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(1) > td:nth-of-type(4)')[0].text
    # print organization_code

    # 统一信用代码
    uniform_credit_code = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2)')[0].text
    # print uniform_credit_code

    # 企业类型
    enterprise_type = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(2) > td:nth-of-type(4)')[0].text
    # print enterprise_type

    # 纳税人识别号
    taxpayer_identification_number = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2)')[0].text
    # print taxpayer_identification_number

    # 行业
    industry = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(3) > td:nth-of-type(4)')[0].text
    # print industry

    # 营业期限
    business_term = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2) > span')[
        0].text
    # print business_term

    # 核准日期
    approval_date = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(4) > td:nth-of-type(4)')[0].text
    # print approval_date

    # 登记机关
    registration_authority = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2)')[0].text
    # print registration_authority

    # 注册地址
    registered_address = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(5) > td:nth-of-type(4)')[0].text
    # print registered_address

    # 英文名称
    english_name = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2)')[0].text
    # print english_name

    # 经营范围
    scope_of_business = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(7) > td:nth-of-type(2) > span > span > span.js-full-container')[
        0].text
    # print scope_of_business

    return (
        'insert into tyc_business_info values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            keyword,
            company_name,
            registered_capital,
            registration_time,
            company_status,
            business_registration_number,
            organization_code,
            uniform_credit_code,
            enterprise_type,
            taxpayer_identification_number,
            industry,
            business_term,
            approval_date,
            registration_authority,
            registered_address,
            english_name,
            scope_of_business,
            str(datetime.datetime.now()),
            str(datetime.datetime.now())[:10])
    )


## 主要人员
def staff_info(html, cursor):
    print u'爬取主要人员信息  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-staffCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-staffCount > span')[0].text

        for i in range(1, int(num) + 1):
            position = soup.select('#_container_staff > div > div > div:nth-of-type(' + str(
                i) + ') > div > div.in-block.f14.new-c5.pt9.pl10.overflow-width.vertival-middle ')[0].text
            name = soup.select('#_container_staff > div > div > div:nth-of-type(' + str(i) + ') > div > a')[0].text
            ID = soup.select('#_container_staff > div > div > div:nth-of-type(' + str(i) + ') > div > a')[0]['href']

            cursor.execute('insert into tyc_staff_info values ("%s","%s","%s","%s","%s","%s","%s")' % (
                keyword, company_name, position, name, ID, str(datetime.datetime.now()),
                str(datetime.datetime.now())[:10]))


    else:
        print u' 没有主要人员的相关内容'
        cursor.execute('insert into tyc_staff_info values ("%s","%s","%s","%s","%s","%s","%s")' % (
            keyword, company_name, 'no_staff_info', 'no_staff_info', 'no_staff_info',
            str(datetime.datetime.now()),
            str(datetime.datetime.now())[:10]))


### 股东信息
def shareholder_info(html, cursor):
    print u'爬取股东信息   ' + str(datetime.datetime.now())
    # def shareholder_info(html, cursor):
    if html.text.__contains__('nav-main-holderCount'):
        soup = BeautifulSoup(html.text, 'lxml')

        num = soup.select('#nav-main-holderCount > span')[0].text
        if num > 20:
            all_page_no = int(num) / 20 + 1
            last_page_no = int(num) % 20
            for i in range(1, int(all_page_no) + 1):
                if i < int(all_page_no):
                    soup2 = get_cookie_by_cid('holder', i, 20)

                    shareholder = re.findall('title="(.*?)"', soup2)
                    ratio = re.findall('<span class="c-money-y">(.*?)</span>', soup2)
                    value = re.findall('<span class="">(.*?)</span>', soup2)
                    for i in range(0, 20):
                        cursor.execute(
                            'insert into tyc_shareholder_info values ("%s","%s","%s","%s","%s","%s","%s")' % (
                                keyword, company_name, shareholder[i], ratio[i], value[i],
                                str(datetime.datetime.now()),
                                str(datetime.datetime.now())[:10]))



                else:
                    re_html = get_shareholder_cookie(i)
                    shareholder = re.findall('title="(.*?)"', re_html)
                    ratio = re.findall('<span class="c-money-y">(.*?)</span>', re_html)
                    value = re.findall('<span class="">(.*?)</span>', re_html)

                    for i in range(0, int(last_page_no)):
                        # print shareholder[i]
                        # print ratio[i]
                        # print value[i]
                        cursor.execute(
                            'insert into tyc_shareholder_info values ("%s","%s","%s","%s","%s","%s","%s")' % (
                                keyword, company_name, shareholder[i],
                                ratio[i], value[i], str(datetime.datetime.now()),
                                str(datetime.datetime.now())[:10]))



    else:
        print u' 没有股东信息的相关内容'
        cursor.execute('insert into tyc_shareholder_info values ("%s","%s","%s","%s","%s","%s","%s")' % (
            keyword, company_name, 'no_shareholder_info', 'no_shareholder_info', 'no_shareholder_info',
            str(datetime.datetime.now()),
            str(datetime.datetime.now())[:10]))


### 对外投资信息
def out_invest_info(html):
    print u'获取对外投资信息  ' + str(datetime.datetime.now())

    if html.text.__contains__('nav-main-inverst'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-inverstCount > span')[0].text
        all_page_no = int(num) / 20 + 1
        # 一共有多少页
        # last_page_no = int(num) % 20
        # 最后一页有多少个
        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_cid('invest', i, 20)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])
                invested_person = re_findall('title="(.*?)', source)
                span_part = re_findall('<span class=".*?">(.*?)</span>', source)
                print span_part[0]  # 被投资企业名称
                print invested_person[0]  # 被投资法定代表人
                print span_part[2]  # 注册资本
                print span_part[3]  # 投资数额
                print span_part[4]  # 投资占比
                print span_part[5]  # 注册时间
                print span_part[6]  # 状态
                print '--------------------------'
                cursor.execute(
                    'insert tyc_outbound_investment values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,
                     span_part[0].decode('utf-8'),
                     invested_person[0].decode('utf-8'),
                     span_part[2].decode('utf-8'),
                     span_part[3].decode('utf-8'),
                     span_part[4].decode('utf-8'),
                     span_part[5].decode('utf-8'),
                     span_part[6].decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10])
                )


    else:
        print '没有对外投资信息'
        cursor.execute(
            'insert into tyc_outbound_investment values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


### 变更记录信息
def change_info(html):
    print u'获取变更记录信息  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-changeCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-changeCount > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_cid('changeinfo', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])
                part_one = re_findall('<div>(.*?)</div>', source)
                part_two = re_findall('<div class="textJustFy changeHoverText">(.*?)</div>', source)
                change_time = part_one[0]
                change_projects = part_one[1]
                before_change = part_two[0]
                after_change = part_two[1]

                cursor.execute(
                    'insert into tyc_change_record values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,
                     change_time.decode('utf-8'),
                     change_projects.decode('utf-8'),
                     detag(before_change).decode('utf-8'),
                     detag(after_change).decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10])
                )

    else:
        print u'没有变更信息的内容'
        cursor.execute(
            'insert into tyc_change_record values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_change_info',
             'no_change_info',
             'no_change_info',
             'no_change_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 产品信息
def product_info(html):
    print u'获取产品信息  ' + str(datetime.datetime.now())

    if html.text.__contains__('nav-main-productinfo'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-productinfo > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            print '第 ' + str(i) + ' 页'
            soup2 = get_cookie_by_cid('product', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])
                image = re_findall('src="(.*?)"', source)
                part_one = re_findall('<span>(.*?)</span>', source)
                detail_info = re_findall('<td><script type="text/html">(.*?)</script>', source)
                print image[0]
                print part_one[0]
                print part_one[1]
                print part_one[2]
                print part_one[3]
                print detail_info[0]
                print '--------------------'
                cursor.execute(
                    'insert into tyc_product_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,
                     image[0],
                     part_one[0].decode('utf-8'),
                     part_one[1].decode('utf-8'),
                     part_one[2].decode('utf-8'),
                     part_one[3].decode('utf-8'),
                     detag(detail_info[0]).decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10]
                     )
                )
    else:
        print u'没有产品信息的内容'
        cursor.execute(
            'insert into tyc_product_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_product_info',
             'no_product_info',
             'no_product_info',
             'no_product_info',
             'no_product_info',
             'no_product_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 微信公众号信息
def wechat_info(html):
    print u'获取微信公众号信息  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-weChatCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-weChatCount > span')[0].text
        all_page_no = int(num) / 10 + 1
        last_page_no = int(num) % 10
        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_cid('wechat', i, 10)
            if i < int(all_page_no):

                for n in range(1, 11):
                    wechat_icon = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.wechatImg > img')[0]['src']

                    wechat_name = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(1)')[0].text

                    wechat_num = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > span:nth-of-type(2)')[
                        0].text

                    wechat_introduce = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(3) > span.overflow-width.in-block.vertical-top')[
                        0].text

                    QR_code = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > div > div > img')[0][
                        'src']

                    cursor.execute(
                        'insert into tyc_wechat_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                        (keyword,
                         company_name,
                         wechat_icon,
                         wechat_name,
                         wechat_num,
                         wechat_introduce,
                         QR_code,
                         str(datetime.datetime.now()),
                         str(datetime.datetime.now())[:10])
                    )

            else:
                for n in range(1, int(last_page_no) + 1):
                    wechat_icon = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.wechatImg > img')[0]['src']

                    wechat_name = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(1)')[0].text

                    wechat_num = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > span:nth-of-type(2)')[
                        0].text

                    wechat_introduce = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(3) > span.overflow-width.in-block.vertical-top')[
                        0].text

                    QR_code = soup2.select(
                        'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                            n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > div > div > img')[0][
                        'src']

                    cursor.execute(
                        'insert into tyc_wechat_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                        (keyword,
                         company_name,
                         wechat_icon,
                         wechat_name,
                         wechat_num,
                         wechat_introduce,
                         QR_code,
                         str(datetime.datetime.now()),
                         str(datetime.datetime.now())[:10])
                    )
    else:
        print u'没有微信公众号的内容'
        cursor.execute(
            'insert into tyc_wechat_info values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_wechat_info',
             'no_wechat_info',
             'no_wechat_info',
             'no_wechat_info',
             'no_wechat_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 网站备案信息
def website_record(html):
    print u'获取网站备案信息  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-icpCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-icpCount > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_cid('icp', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])
                part_one = re_findall('<td><span>(.*?)</span></td>', source)
                part_two = re_findall('target="_blank">(.*?)</a></td>', source)
                check_time = part_one[0]
                website_name = part_one[1]
                homepage = part_two[0]
                domain = re_findall('<td>(.*?)</td>', source)[3]
                record_number = part_one[2]
                state = part_one[3]
                unit_character = part_one[4]
                print part_one
                print part_two
                print check_time
                print website_name
                print homepage
                print domain
                print record_number
                print state
                print unit_character
                print '--------------------------'
                cursor.execute(
                    'insert into tyc_website_record values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,
                     check_time.decode('utf-8'),
                     website_name.decode('utf-8'),
                     homepage.decode('utf-8'),
                     domain.decode('utf-8'),
                     record_number.decode('utf-8'),
                     state.decode('utf-8'),
                     unit_character.decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10])
                )



    else:
        print '没有 网站备案信息'
        cursor.execute(
            'insert into tyc_website_record values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_website_record',
             'no_website_record',
             'no_website_record',
             'no_website_record',
             'no_website_record',
             'no_website_record',
             'no_website_record',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 法律诉讼部分
def lawsuit(html):
    print u'获取法律诉讼信息  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-lawsuitCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-lawsuitCount > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            print u'爬第' + str(i) + u'页'
            soup2 = get_cookie_by_name('lawsuit', i, 5)
            # print soup2
            res = soup2.select('tr')

            for x in range(1, len(res)):
                source = str(res[x])
                print source

                date = re_findall('<span class=".*?">(.*?)</span>', source)[0]
                Judgment_document_url = re_findall('href="(.*?)" href-new-event', source)[0]
                Judgment_document_name = re_findall('target="_blank">(.*?)</a>', source)[0]
                cause = re_findall('<span class=".*?">(.*?)</span>', source)[1]
                identity = detag(re_findall('<div class="text-dark-color">(.*?)</div>', source)[0])
                docket_number = re_findall('<span class=".*?">(.*?)</span>', source)[2]

                print date
                print Judgment_document_name
                print Judgment_document_url
                print cause
                print identity
                print docket_number
                cursor.execute(
                    'insert into tyc_lawsuit_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,
                     date.decode('utf-8'),
                     Judgment_document_name.decode('utf-8'),
                     Judgment_document_url.decode('utf-8'),
                     cause.decode('utf-8'),
                     identity.decode('utf-8'),
                     docket_number.decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10]
                     )
                )
    else:
        print '没有 法律诉讼部分'
        cursor.execute(
            'insert into tyc_lawsuit_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_lawsuit_info',
             'no_lawsuit_info',
             'no_lawsuit_info',
             'no_lawsuit_info',
             'no_lawsuit_info',
             'no_lawsuit_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 法院公告部分
def court(html):
    print u'获取法院公告信息  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-courtCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-courtCount > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_name('court', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])

                date = re_findall('"publishdate":"(.*?)"', source)[0]
                appellant = re_findall('"party1":"(.*?)"', source)[0]
                defendant = re_findall('"party2":"(.*?)"', source)[0]
                type = re_findall('"bltntypename":"(.*?)"', source)[0]
                court = re_findall('"courtcode":"(.*?)"', source)[0]
                detail = re_findall('"content":"(.*?)"', source)[0]

                print date
                print appellant
                print defendant
                print type
                print court
                print detail

                cursor.execute(
                    'insert into tyc_court_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,
                     date.decode('utf-8'),
                     appellant.decode('utf-8'),
                     defendant.decode('utf-8'),
                     type.decode('utf-8'),
                     court.decode('utf-8'),
                     detail.decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10]
                     )
                )
    else:
        print '没有 法院公告部分'
        cursor.execute(
            'insert into tyc_court_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_court_info',
             'no_court_info',
             'no_court_info',
             'no_court_info',
             'no_court_info',
             'no_court_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )
        # ==================================


## 执行人部分
def zhixing(html):
    print u'获取被执行人信息  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-zhixing'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-zhixing > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_cid('zhixing', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])
                part = re_findall('<span class=".*?">(.*?)</span>', source)
                print part[0]
                print part[1]
                print part[2]
                print part[3]
                cursor.execute(
                    'insert into tyc_zhixing_info values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,
                     part[0].decode('utf-8'),
                     part[1].decode('utf-8'),
                     part[2].decode('utf-8'),
                     part[3].decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10]
                     )
                )

    else:
        print u'没有 被执行人信息部分'
        cursor.execute(
            'insert into tyc_zhixing_info values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_zhixing_info',
             'no_zhixing_info',
             'no_zhixing_info',
             'no_zhixing_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10]

             )
        )


## 开庭公告部分
def announcement(html):
    print u'获取开庭公告部分  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-announcementCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-announcementCount > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_cid('announcementCount', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])

                date = re_findall('<td>(.*?)</td>', source)[0]
                type = re_findall('<span class="text-dark-color">(.*?)</span>', source)[0]
                appellant = re_findall('"name":"(.*?)",', source)[0]
                defendant = re_findall('"name":"(.*?)",', source)[1]
                case_no = re_findall('"caseNo":"\t(.*?)",', source)[0]

                print date
                print type
                print appellant
                print defendant
                print case_no

                cursor.execute(
                    'insert into tyc_announcement_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,
                     date.decode('utf-8'),
                     type.decode('utf-8'),
                     appellant.decode('utf-8'),
                     defendant.decode('utf-8'),
                     case_no.decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10])
                )
    else:
        print  u'没有 开庭公告部分'
        cursor.execute(
            'insert into tyc_announcement_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_announcement_info',
             'no_announcement_info',
             'no_announcement_info',
             'no_announcement_info',
             'no_announcement_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 惩罚部分
def punish(html):
    print u'获取惩罚部分  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-punishment'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-punishment > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_name('punish', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])
                print source

                date = re_findall('<span class=".*?">(.*?)</span>', source)[0]
                document_no = re_findall('<span class=".*?">(.*?)</span>', source)[1]
                type = re_findall('<span class=".*?">(.*?)</span>', source)[2]
                decision_organ = re_findall('<div class=".*?">(.*?)</div>', source)[0]

                print date
                print document_no
                print type
                print decision_organ
                cursor.execute(
                    'insert into tyc_punish_info values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,
                     date.decode('utf-8'),
                     document_no.decode('utf-8'),
                     type.decode('utf-8'),
                     decision_organ.decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10])
                )
    else:
        print u'没有 行政处罚部分'
        cursor.execute(
            'insert into tyc_punish_info values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_punish_info',
             'no_punish_info',
             'no_punish_info',
             'no_punish_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 招聘部分
def recruit(html):
    print u'获取招聘部分  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-recruitCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-recruitCount > span')[0].text
        all_page_no = int(num) / 10 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_name('recruit', i, 10)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])
                date = re_findall('<span.*?>(.*?)</span>', source)[0]
                job = re_findall('<span.*?>(.*?)</span>', source)[1]
                exper = re_findall('<span.*?>(.*?)</span>', source)[2]
                num = re_findall('<span.*?>(.*?)</span>', source)[3]
                location = re_findall('<span.*?>(.*?)</span>', source)[4]
                salary = re_findall('oriSalary&quot;:&quot;(.*?)&quot;,', source)[0]
                detail = detag(re_findall('description&quot;:&quot;(.*?)&quot;', source)[0])
                fromWeb = re_findall('source&quot;:&quot;(.*?)&quot;,', source)[0]

                print date
                print job
                print exper
                print num
                print location
                print salary
                print detail
                print fromWeb
                cursor.execute('insert into tyc_recruit_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                               (keyword,
                                company_name,
                                'no_announcement_info',
                                'no_announcement_info',
                                'no_announcement_info',
                                'no_announcement_info',
                                'no_announcement_info',
                                str(datetime.datetime.now()),
                                str(datetime.datetime.now())[:10])
                               )


## 专利部分
def patent(html):
    print u'获取专利部分  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-patentCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-patentCount > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_cid('patent', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])

                date = re_findall('<span.*?>(.*?)</span>', source)[0]
                name = re_findall('<span.*?>(.*?)</span>', source)[1]
                application_num = re_findall('<span.*?>(.*?)</span>', source)[2]
                application_for_pubnum = re_findall('<span.*?>(.*?)</span>', source)[3]
                location = re_findall('address&quot;:&quot;(.*?)&quot;,', source)[0]
                inventor = re_findall('inventor&quot;:&quot;(.*)&quot;,&quot;agent', source)[0]
                applicant = re_findall('applicantName&quot;:&quot;(.*?)&quot;', source)[0]
                agent = re_findall('agent&quot;:&quot;(.*?)&quot;,&quot;', source)[0]
                agency = re_findall('agency&quot;:&quot;(.*?)&quot;,&quot;', source)[0]
                detail = re_findall('abstracts&quot;:&quot;(.*?)&quot;,&quot;', source)[0]

                print date
                print name
                print application_num
                print application_for_pubnum
                print location
                print inventor
                print applicant
                print agent
                print agency
                print detail
                cursor.execute(
                    'insert into tyc_patent_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s" )' %
                    (keyword,
                     company_name,
                     date.decode('utf-8'),
                     name.decode('utf-8'),
                     application_num.decode('utf-8'),
                     application_for_pubnum.decode('utf-8'),
                     location.decode('utf-8'),
                     inventor.decode('utf-8'),
                     applicant.decode('utf-8'),
                     agent.decode('utf-8'),
                     agency.decode('utf-8'),
                     detail.decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10])
                )
    else:
        print u'专利部分无内容'
        cursor.execute(
            'insert into tyc_patent_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s" )' %
            (keyword,
             company_name,
             'no_patent_info',
             'no_patent_info',
             'no_patent_info',
             'no_patent_info',
             'no_patent_info',
             'no_patent_info',
             'no_patent_info',
             'no_patent_info',
             'no_patent_info',
             'no_patent_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 竞品部分
def jingpin(html):
    print u'获取竞品部分  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-companyJingpin'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-companyJingpin > span')[0].text
        all_page_no = int(num) / 10 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_name('jingpin', i, 10)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])

                icon = re_findall('src="(.*?)"', source)[0]
                name = re_findall('img alt="(.*?)"', source)[0]
                location = re_findall('span class=".*?">(.*?)</span>', source)[0]
                current_round = re_findall('span class=".*?">(.*?)</span>', source)[1]
                industry = re_findall('span class=".*?">(.*?)</span>', source)[2]
                business = re_findall('span class=".*?">(.*?)</span>', source)[3]
                create_time = re_findall('span class=".*?">(.*?)</span>', source)[4]
                valuation = re_findall('span class=".*?">(.*?)</span>', source)[5]

                print icon
                print name
                print location
                print current_round
                print industry
                print business
                print create_time
                print valuation
                cursor.execute(
                    'insert into tyc_jingpin_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s" )' %
                    (keyword,
                     company_name,
                     icon.decode('utf-8'),
                     name.decode('utf-8'),
                     location.decode('utf-8'),
                     current_round.decode('utf-8'),
                     industry.decode('utf-8'),
                     business.decode('utf-8'),
                     create_time.decode('utf-8'),
                     valuation.decode('utf-8'),
                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10])
                )
    else:
        print u'竞品部分无内容'
        cursor.execute(
            'insert into tyc_jingpin_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s" )' %
            (keyword,
             company_name,
             'no_jingpin_info',
             'no_jingpin_info',
             'no_jingpin_info',
             'no_jingpin_info',
             'no_jingpin_info',
             'no_jingpin_info',
             'no_jingpin_info',
             'no_jingpin_info',
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 软件著作权部分 copy他拼错了 以后可能会改回来 爬不到优先检查这里
def copyR(html):
    print u'获取软件著作权部分  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-cpoyRCount'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-cpoyRCount > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_cid('copyright', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])

                obj = re_findall('<span>(.*?)</span>', source)
                date = obj[0]
                name = obj[1]
                brief_name = obj[2]
                registration_no = obj[3]
                classification_no = obj[4]
                version_no = obj[5]

                print date
                print name
                print brief_name
                print registration_no
                print classification_no
                print version_no
                cursor.execute(
                    'insert into tyc_copyR_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s" )' %
                    (keyword,
                     company_name,

                     date.decode('utf-8'),
                     name.decode('utf-8'),
                     brief_name.decode('utf-8'),
                     registration_no.decode('utf-8'),
                     classification_no.decode('utf-8'),
                     version_no.decode('utf-8'),

                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10])
                )
    else:
        print u'没有软件著作权部分信息'
    cursor.execute(
        'insert into tyc_copyR_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s" )' %
        (keyword,
         company_name,

         'no_copyR_info',
         'no_copyR_info',
         'no_copyR_info',
         'no_copyR_info',
         'no_copyR_info',
         'no_copyR_info',

         str(datetime.datetime.now()),
         str(datetime.datetime.now())[:10])
    )


## 作品著作权部分
def copyrightWorks(html):
    print u'获取作品著作权部分  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-copyrightWorks'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-copyrightWorks > span')[0].text
        all_page_no = int(num) / 5 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_cid('copyrightWorks', i, 5)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])

                obj = re_findall('<span>(.*?)</span>', source)
                name = obj[0]
                register_no = obj[1]
                category = obj[2]
                finish_date = obj[3]
                register_date = obj[4]
                publish_date = obj[5]

                print name
                print register_no
                print category
                print finish_date
                print register_date
                print publish_date
                cursor.execute(
                    'insert into tyc_copyRworks_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s" )' %
                    (keyword,
                     company_name,

                     name.decode('utf-8'),
                     register_no.decode('utf-8'),
                     category.decode('utf-8'),
                     finish_date.decode('utf-8'),
                     register_date.decode('utf-8'),
                     publish_date.decode('utf-8'),

                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10])

                )

    else:
        print u'没有作品著作权部分'
        cursor.execute(
            'insert into tyc_copyRworks_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s" )' %
            (keyword,
             company_name,

             'no_copyRworks_info',
             'no_copyRworks_info',
             'no_copyRworks_info',
             'no_copyRworks_info',
             'no_copyRworks_info',
             'no_copyRworks_info',

             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])

        )


## 获取企业业务部分
def firmProduct(html):
    print u'获取企业业务部分  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-companyProduct'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-companyProduct > span')[0].text
        all_page_no = int(num) / 15 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_name('firmProduct', i, 15)
            res = soup2.select('div[class="product-item"]')
            for x in range(1, len(res)):
                source = str(res[x])
                name = re_findall('img alt="(.*?)"', source)[0]
                img = re_findall('src="(.*?)"', source)[0]
                category = detag(re_findall('<div class=".*?">(.*?)</div>', source)[2])
                brief = detag(re_findall('<div class=".*?">(.*?)</div>', source)[3])

                print name
                print img
                print category
                print brief
                cursor.execute('insert into tyc_companyProduct_info values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
                               (keyword,
                                company_name,

                                name.decode('utf-8'),
                                img.decode('utf-8'),
                                category.decode('utf-8'),
                                brief.decode('utf-8'),

                                str(datetime.datetime.now()),
                                str(datetime.datetime.now())[:10])
                               )

    else:
        print u'没有企业业务部分'
        cursor.execute(
            'insert into tyc_companyProduct_info values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,

             'no_companyProduct_info',
             'no_companyProduct_info',
             'no_companyProduct_info',
             'no_companyProduct_info',

             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )


## 获取投资事件部分
def investment_info(html):
    print u'获取投资事件部分  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-jigouTzanli'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-jigouTzanli > span')[0].text
        all_page_no = int(num) / 10 + 1

        for i in range(1, int(all_page_no) + 1):
            soup2 = get_cookie_by_name('touzi', i, 10)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])

                date = re_findall('<span class=".*?">(.*?)</span>', source)[0]
                round = re_findall('<span class=".*?">(.*?)</span>', source)[1]
                amount = re_findall('<span class=".*?">(.*?)</span>', source)[2]
                investor = detag(re_findall('<div>(.*?)<img alt', source)[0])
                product_name = re_findall('img alt="(.*?)"', source)[0]
                product_icon = re_findall('src="(.*?)"', source)[0]
                location = re_findall('<span class=".*?">(.*?)</span>', source)[3]
                industry = re_findall('<span class=".*?">(.*?)</span>', source)[4]
                business = re_findall('<span class=".*?">(.*?)</span>', source)[5]

                print date
                print round
                print amount
                print investor
                print product_name
                print product_icon
                print location
                print industry
                print business
                cursor.execute(
                    'insert into tyc_investment_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (keyword,
                     company_name,

                     date.decode('utf-8'),
                     round.decode('utf-8'),
                     amount.decode('utf-8'),
                     investor.decode('utf-8'),
                     product_name.decode('utf-8'),
                     product_icon.decode('utf-8'),
                     location.decode('utf-8'),
                     industry.decode('utf-8'),
                     business.decode('utf-8'),

                     str(datetime.datetime.now()),
                     str(datetime.datetime.now())[:10]))
    else:
        print u'没有投资事件部分'
        cursor.execute(
            'insert into tyc_investment_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
            (keyword,
             company_name,
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',
             'no_invest_info',

             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10]))


## 获取失信人部分
def dishonest(html):
    print u'爬取失信人信息  ' + str(datetime.datetime.now())
    if html.text.__contains__('nav-main-dishonest'):
        soup = BeautifulSoup(html.text, 'lxml')
        num = soup.select('#nav-main-dishonest > span')[0].text
        for i in range(1, int(num) + 1):
            date = soup.select(
                '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(1) > span')[0].text
            case_no = soup.select(
                '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(2) > span')[0].text
            court = soup.select(
                '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(3) > span')[0].text
            state = soup.select(
                '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(4) > span')[0].text
            reference = soup.select(
                '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(5) > span')[0].text
            print date
            print case_no
            print court
            print state
            print reference
            cursor.execute('insert into tyc_dishonest_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                keyword, company_name, date, case_no, court, state, reference, str(datetime.datetime.now()),
                str(datetime.datetime.now())[:10]))

    else:
        print u'没有失信人信息'
        cursor.execute('insert into tyc_dishonest_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            keyword, company_name, 'no_dishonest_info', 'no_dishonest_info', 'no_dishonest_info', 'no_dishonest_info', 'no_dishonest_info', str(datetime.datetime.now()),
        str(datetime.datetime.now())[:10]))


# ==================================
# --------各模块对应cookie获取区-------
# ==================================


### 股东信息cookie
def get_shareholder_cookie(page_no):
    timestamp = int(time.time() * 1000)
    head1 = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'www.tianyancha.com',
        'Origin': 'https://www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    }
    tongji_url = "https://www.tianyancha.com/tongji/" + cid + ".json?_=" + str(timestamp)

    tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies, verify=False)

    cookie = tongji_page.cookies.get_dict()
    js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])

    token = re.findall(r"token=(\w+);", js_code)[0]
    utm_code = re.findall("return'([^']*?)'", js_code)[0]
    t = ord(cid[0])

    fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
    fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
    fw.close()
    phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
    # --print phantomResStr
    # print "phantomResStr: %s" % phantomResStr
    phantomRes = json.loads(phantomResStr)
    ssuid = phantomRes["ssuid"]
    utm = phantomRes["utm"]

    head2 = {
        'Host': 'www.tianyancha.com',
        # 'Referer': 'https://www.tianyancha.com/company/22822',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
            "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
                  cookie["uccid"],
        'X-Requested-With': 'XMLHttpRequest'
    }

    url = 'https://www.tianyancha.com/pagination/holder.xhtml?ps=20&pn=' + str(
        page_no) + '&id=' + cid + '&_=' + str(
        timestamp - 1)

    resp = requests.get(url, headers=head2, proxies=proxies, verify=False)
    # print resp
    html = resp.text
    return html
    # quit()
    # soup2 = BeautifulSoup(html, 'lxml')
    # return soup2


#
#
# ### 对外投资信息cookie
# def get_invest_cookie(page_no):
#     while True:
#         try:
#             proxies1 = get_proxy()
#             timestamp = int(time.time() * 1000)
#             head1 = {
#                 'Content-Type': 'application/json; charset=UTF-8',
#                 'Host': 'www.tianyancha.com',
#                 'Origin': 'https://www.tianyancha.com',
#                 'Referer': 'https://www.tianyancha.com',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept': 'application/json, text/javascript, */*; q=0.01',
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#             tongji_url = "https://www.tianyancha.com/tongji/" + cid + ".json?_=" + str(timestamp)
#
#             tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)
#
#             cookie = tongji_page.cookies.get_dict()
#             js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
#
#             token = re.findall(r"token=(\w+);", js_code)[0]
#             utm_code = re.findall("return'([^']*?)'", js_code)[0]
#             t = ord(cid[0])
#
#             fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
#             fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
#             fw.close()
#             phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
#             # --print phantomResStr
#             # print "phantomResStr: %s" % phantomResStr
#             phantomRes = json.loads(phantomResStr)
#             ssuid = phantomRes["ssuid"]
#             utm = phantomRes["utm"]
#
#             head2 = {
#                 'Host': 'www.tianyancha.com',
#                 # 'Referer': 'https://www.tianyancha.com/company/22822',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept-Language': 'zh-CN,zh;q=0.8',
#                 'Connection': 'keep-alive',
#                 'Accept': '*/*',
#                 'Accept-Encoding': 'gzip, deflate, sdch, br',
#                 'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
#                     "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
#                           cookie["uccid"],
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#
#             url = 'https://www.tianyancha.com/pagination/invest.xhtml?ps=20&pn=' + str(
#                 page_no) + '&id=' + cid + '&_=' + str(timestamp - 1)
#             resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
#             # print resp
#             html = resp.text
#             soup2 = BeautifulSoup(html, 'lxml')
#             return soup2
#             break
#         except Exception, e:
#             print str(e)
#             if str(e).find('list index out of range') >= 0:
#                 print u'get_invest_cookie 代理失效 换一个试试'
#             continue
#
#
# ### 变更记录信息cookie
# def get_change_cookie(page_no):
#     while True:
#         try:
#             proxies1 = get_proxy()
#             timestamp = int(time.time() * 1000)
#             head1 = {
#                 'Content-Type': 'application/json; charset=UTF-8',
#                 'Host': 'www.tianyancha.com',
#                 'Origin': 'https://www.tianyancha.com',
#                 'Referer': 'https://www.tianyancha.com',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept': 'application/json, text/javascript, */*; q=0.01',
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#             tongji_url = "https://www.tianyancha.com/tongji/" + cid + ".json?_=" + str(timestamp)
#
#             tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)
#
#             cookie = tongji_page.cookies.get_dict()
#             js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
#
#             token = re.findall(r"token=(\w+);", js_code)[0]
#             utm_code = re.findall("return'([^']*?)'", js_code)[0]
#             t = ord(cid[0])
#
#             fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
#             fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
#             fw.close()
#             phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
#             # --print phantomResStr
#             # print "phantomResStr: %s" % phantomResStr
#             phantomRes = json.loads(phantomResStr)
#             ssuid = phantomRes["ssuid"]
#             utm = phantomRes["utm"]
#
#             head2 = {
#                 'Host': 'www.tianyancha.com',
#                 # 'Referer': 'https://www.tianyancha.com/company/22822',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept-Language': 'zh-CN,zh;q=0.8',
#                 'Connection': 'keep-alive',
#                 'Accept': '*/*',
#                 'Accept-Encoding': 'gzip, deflate, sdch, br',
#                 'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
#                     "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
#                           cookie["uccid"],
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#
#             url = 'https://www.tianyancha.com/pagination/changeinfo.xhtml?ps=5&pn=' + str(
#                 page_no) + '&id=' + cid + '&_=' + str(timestamp - 1)
#             print url
#             resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
#             # print resp
#             html = resp.text
#             soup2 = BeautifulSoup(html, 'lxml')
#             return soup2
#             break
#         except Exception, e:
#             print str(e)
#             if str(e).find('list index out of range') >= 0:
#                 print u'get_change_cookie 代理失效 换一个试试'
#             continue
#
#
# ### 产品信息cookie
# def get_product_info_cookie(page_no):
#     while True:
#         try:
#             proxies1 = get_proxy()
#             timestamp = int(time.time() * 1000)
#             head1 = {
#                 'Content-Type': 'application/json; charset=UTF-8',
#                 'Host': 'www.tianyancha.com',
#                 'Origin': 'https://www.tianyancha.com',
#                 'Referer': 'https://www.tianyancha.com',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept': 'application/json, text/javascript, */*; q=0.01',
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#             tongji_url = "https://www.tianyancha.com/tongji/" + cid + ".json?_=" + str(timestamp)
#
#             tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)
#
#             cookie = tongji_page.cookies.get_dict()
#             js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
#
#             token = re.findall(r"token=(\w+);", js_code)[0]
#             utm_code = re.findall("return'([^']*?)'", js_code)[0]
#             t = ord(cid[0])
#
#             fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
#             fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
#             fw.close()
#             phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
#             # --print phantomResStr
#             # print "phantomResStr: %s" % phantomResStr
#             phantomRes = json.loads(phantomResStr)
#             ssuid = phantomRes["ssuid"]
#             utm = phantomRes["utm"]
#
#             head2 = {
#                 'Host': 'www.tianyancha.com',
#                 # 'Referer': 'https://www.tianyancha.com/company/22822',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept-Language': 'zh-CN,zh;q=0.8',
#                 'Connection': 'keep-alive',
#                 'Accept': '*/*',
#                 'Accept-Encoding': 'gzip, deflate, sdch, br',
#                 'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
#                     "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
#                           cookie["uccid"],
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#
#             url = 'https://www.tianyancha.com/pagination/product.xhtml?ps=5&pn=' + str(
#                 page_no) + '&id=' + cid + '&_=' + str(timestamp - 1)
#             print url
#             resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
#             # print resp
#             html = resp.text
#             soup2 = BeautifulSoup(html, 'lxml')
#             return soup2
#             break
#         except Exception, e:
#             print str(e)
#             if str(e).find('list index out of range') >= 0:
#                 print u'get_product_info_cookie 代理失效 换一个试试'
#             continue
#
#
# ### 微信信息cookie
# def get_wechat_cookie(page_no):
#     while True:
#         try:
#             proxies1 = get_proxy()
#             timestamp = int(time.time() * 1000)
#             head1 = {
#                 'Content-Type': 'application/json; charset=UTF-8',
#                 'Host': 'www.tianyancha.com',
#                 'Origin': 'https://www.tianyancha.com',
#                 'Referer': 'https://www.tianyancha.com',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept': 'application/json, text/javascript, */*; q=0.01',
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#             tongji_url = "https://www.tianyancha.com/tongji/" + cid + ".json?_=" + str(timestamp)
#
#             tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)
#
#             cookie = tongji_page.cookies.get_dict()
#             js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
#
#             token = re.findall(r"token=(\w+);", js_code)[0]
#             utm_code = re.findall("return'([^']*?)'", js_code)[0]
#             t = ord(cid[0])
#
#             fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
#             fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
#             fw.close()
#             phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
#             # --print phantomResStr
#             # print "phantomResStr: %s" % phantomResStr
#             phantomRes = json.loads(phantomResStr)
#             ssuid = phantomRes["ssuid"]
#             utm = phantomRes["utm"]
#
#             head2 = {
#                 'Host': 'www.tianyancha.com',
#                 # 'Referer': 'https://www.tianyancha.com/company/22822',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept-Language': 'zh-CN,zh;q=0.8',
#                 'Connection': 'keep-alive',
#                 'Accept': '*/*',
#                 'Accept-Encoding': 'gzip, deflate, sdch, br',
#                 'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
#                     "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
#                           cookie["uccid"],
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#
#             url = 'https://www.tianyancha.com/pagination/wechat.xhtml?ps=10&pn=' + str(
#                 page_no) + '&id=' + cid + '&_=' + str(timestamp - 1)
#             print url
#             resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
#             # print resp
#             html = resp.text
#             soup2 = BeautifulSoup(html, 'lxml')
#             return soup2
#             break
#         except Exception, e:
#             print str(e)
#             if str(e).find('list index out of range') >= 0:
#                 print u'get_wechat_cookie 代理失效 换一个试试'
#             continue
#
#
# ### 网站备案信息cookie
# def get_website_record_cookie(page_no):
#     while True:
#         try:
#             proxies1 = get_proxy()
#             timestamp = int(time.time() * 1000)
#             head1 = {
#                 'Content-Type': 'application/json; charset=UTF-8',
#                 'Host': 'www.tianyancha.com',
#                 'Origin': 'https://www.tianyancha.com',
#                 'Referer': 'https://www.tianyancha.com',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept': 'application/json, text/javascript, */*; q=0.01',
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#             tongji_url = "https://www.tianyancha.com/tongji/" + cid + ".json?_=" + str(timestamp)
#
#             tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)
#
#             cookie = tongji_page.cookies.get_dict()
#             js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
#
#             token = re.findall(r"token=(\w+);", js_code)[0]
#             utm_code = re.findall("return'([^']*?)'", js_code)[0]
#             t = ord(cid[0])
#
#             fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
#             fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
#             fw.close()
#             phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
#             # --print phantomResStr
#             # print "phantomResStr: %s" % phantomResStr
#             phantomRes = json.loads(phantomResStr)
#             ssuid = phantomRes["ssuid"]
#             utm = phantomRes["utm"]
#
#             head2 = {
#                 'Host': 'www.tianyancha.com',
#                 # 'Referer': 'https://www.tianyancha.com/company/22822',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept-Language': 'zh-CN,zh;q=0.8',
#                 'Connection': 'keep-alive',
#                 'Accept': '*/*',
#                 'Accept-Encoding': 'gzip, deflate, sdch, br',
#                 'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
#                     "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
#                           cookie["uccid"],
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#
#             url = 'https://www.tianyancha.com/pagination/icp.xhtml?ps=5&pn=' + str(
#                 page_no) + '&id=' + cid + '&_=' + str(timestamp - 1)
#             print url
#             resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
#             # print resp
#             html = resp.text
#             soup2 = BeautifulSoup(html, 'lxml')
#             return soup2
#             break
#         except Exception, e:
#             print str(e)
#             if str(e).find('list index out of range') >= 0:
#                 print u'get_website_record_cookies 代理失效 换一个试试'
#             continue
#
#
# ### 法律诉讼部分cookie
# def get_lawsuit_cookie(page_no):
#     while True:
#         try:
#             proxies1 = get_proxy()
#             timestamp = int(time.time() * 1000)
#             head1 = {
#                 'Content-Type': 'application/json; charset=UTF-8',
#                 'Host': 'www.tianyancha.com',
#                 'Origin': 'https://www.tianyancha.com',
#                 'Referer': 'https://www.tianyancha.com',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept': 'application/json, text/javascript, */*; q=0.01',
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#             tongji_url = "https://www.tianyancha.com/tongji/" + urllib.quote(
#                 company_name.encode('utf8')) + ".json?_=" + str(timestamp)
#
#             tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)
#
#             cookie = tongji_page.cookies.get_dict()
#             js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
#
#             token = re.findall(r"token=(\w+);", js_code)[0]
#             utm_code = re.findall("return'([^']*?)'", js_code)[0]
#             t = ord(company_name[0])
#
#             fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
#             fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
#             fw.close()
#             phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
#             # --print phantomResStr
#             # print "phantomResStr: %s" % phantomResStr
#             phantomRes = json.loads(phantomResStr)
#             ssuid = phantomRes["ssuid"]
#             utm = phantomRes["utm"]
#
#             head2 = {
#                 'Host': 'www.tianyancha.com',
#                 # 'Referer': 'https://www.tianyancha.com/company/22822',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept-Language': 'zh-CN,zh;q=0.8',
#                 'Connection': 'keep-alive',
#                 'Accept': '*/*',
#                 'Accept-Encoding': 'gzip, deflate, sdch, br',
#                 'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
#                     "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
#                           cookie["uccid"],
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#
#             url = 'https://www.tianyancha.com/pagination/lawsuit.xhtml?ps=5&pn=' + str(
#                 page_no) + '&name=' + urllib.quote(company_name.encode('utf8')) + '&_=' + str(timestamp - 1)
#             print url
#             resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
#             # print resp
#             html = resp.text
#             soup2 = BeautifulSoup(html, 'lxml')
#             return soup2
#             break
#         except Exception, e:
#             print str(e)
#             if str(e).find('list index out of range') >= 0:
#                 print u'get_lawsuit_info_cookie 代理失效 换一个试试'
#             continue
#
#
# def get_court_cookie(page_no):
#     while True:
#         try:
#             proxies1 = get_proxy()
#             timestamp = int(time.time() * 1000)
#             head1 = {
#                 'Content-Type': 'application/json; charset=UTF-8',
#                 'Host': 'www.tianyancha.com',
#                 'Origin': 'https://www.tianyancha.com',
#                 'Referer': 'https://www.tianyancha.com',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept': 'application/json, text/javascript, */*; q=0.01',
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#             tongji_url = "https://www.tianyancha.com/tongji/" + urllib.quote(
#                 company_name.encode('utf8')) + ".json?_=" + str(timestamp)
#
#             tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)
#
#             cookie = tongji_page.cookies.get_dict()
#             js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
#
#             token = re.findall(r"token=(\w+);", js_code)[0]
#             utm_code = re.findall("return'([^']*?)'", js_code)[0]
#             t = ord(company_name[0])
#
#             fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
#             fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
#             fw.close()
#             phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
#             # --print phantomResStr
#             # print "phantomResStr: %s" % phantomResStr
#             phantomRes = json.loads(phantomResStr)
#             ssuid = phantomRes["ssuid"]
#             utm = phantomRes["utm"]
#
#             head2 = {
#                 'Host': 'www.tianyancha.com',
#                 # 'Referer': 'https://www.tianyancha.com/company/22822',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
#                 'Accept-Language': 'zh-CN,zh;q=0.8',
#                 'Connection': 'keep-alive',
#                 'Accept': '*/*',
#                 'Accept-Encoding': 'gzip, deflate, sdch, br',
#                 'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
#                     "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
#                           cookie["uccid"],
#                 'X-Requested-With': 'XMLHttpRequest'
#             }
#
#             url = 'https://www.tianyancha.com/pagination/court.xhtml?ps=5&pn=' + str(
#                 page_no) + '&name=' + urllib.quote(company_name.encode('utf8')) + '&_=' + str(timestamp - 1)
#             print url
#             resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
#             # print resp
#             html = resp.text
#             soup2 = BeautifulSoup(html, 'lxml')
#             return soup2
#             break
#         except Exception, e:
#             print str(e)
#             if str(e).find('list index out of range') >= 0:
#                 print u'get_court_info_cookie 代理失效 换一个试试'
#             continue


def get_cookie_by_cid(name, page_no, per_page):
    while True:
        try:
            proxies1 = get_proxy()
            timestamp = int(time.time() * 1000)
            head1 = {
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': 'www.tianyancha.com',
                'Origin': 'https://www.tianyancha.com',
                'Referer': 'https://www.tianyancha.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest'
            }
            tongji_url = "https://www.tianyancha.com/tongji/" + cid + ".json?_=" + str(timestamp)

            tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)

            cookie = tongji_page.cookies.get_dict()
            js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])

            token = re.findall(r"token=(\w+);", js_code)[0]
            utm_code = re.findall("return'([^']*?)'", js_code)[0]
            t = ord(cid[0])

            fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
            fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
            fw.close()
            phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
            # --print phantomResStr
            # print "phantomResStr: %s" % phantomResStr
            phantomRes = json.loads(phantomResStr)
            ssuid = phantomRes["ssuid"]
            utm = phantomRes["utm"]

            head2 = {
                'Host': 'www.tianyancha.com',
                # 'Referer': 'https://www.tianyancha.com/company/22822',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
                    "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
                          cookie["uccid"],
                'X-Requested-With': 'XMLHttpRequest'
            }

            url = 'https://www.tianyancha.com/pagination/' + name + '.xhtml?ps=' + str(per_page) + '&pn=' + str(
                page_no) + '&id=' + cid + '&_=' + str(timestamp - 1)
            resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
            # print resp
            html = resp.text
            soup2 = BeautifulSoup(html, 'lxml')
            return soup2
            break
        except Exception, e:
            print str(e)
            if str(e).find('list index out of range') >= 0:
                print u'get cookie 代理失效 换一个试试'
            continue


def get_cookie_by_name(name, page_no, per_page):
    while True:
        try:
            proxies1 = get_proxy()
            timestamp = int(time.time() * 1000)
            head1 = {
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': 'www.tianyancha.com',
                'Origin': 'https://www.tianyancha.com',
                'Referer': 'https://www.tianyancha.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest'
            }
            tongji_url = "https://www.tianyancha.com/tongji/" + urllib.quote(
                company_name.encode('utf8')) + ".json?_=" + str(timestamp)

            tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)

            cookie = tongji_page.cookies.get_dict()
            js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])

            token = re.findall(r"token=(\w+);", js_code)[0]
            utm_code = re.findall("return'([^']*?)'", js_code)[0]
            t = ord(company_name[0])

            fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
            fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
            fw.close()
            phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
            # --print phantomResStr
            # print "phantomResStr: %s" % phantomResStr
            phantomRes = json.loads(phantomResStr)
            ssuid = phantomRes["ssuid"]
            utm = phantomRes["utm"]

            head2 = {
                'Host': 'www.tianyancha.com',
                # 'Referer': 'https://www.tianyancha.com/company/22822',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
                    "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
                          cookie["uccid"],
                'X-Requested-With': 'XMLHttpRequest'
            }

            url = 'https://www.tianyancha.com/pagination/' + name + '.xhtml?ps=' + str(per_page) + '&pn=' + str(
                page_no) + '&name=' + urllib.quote(company_name.encode('utf8')) + '&_=' + str(timestamp - 1)
            print url
            resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
            # print resp
            html = resp.text
            soup2 = BeautifulSoup(html, 'lxml')
            return soup2
            break
        except Exception, e:
            print str(e)
            if str(e).find('list index out of range') >= 0:
                print 'get cookie 代理失效 换一个试试'
            continue


# ===================================
# ------------主逻辑功能区-------------
# ===================================


def get_page(url):
    headers = {
        'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    html = requests.get(url, proxies=proxies, headers=headers)
    return html


def do_keyword(keyword):
    while True:

        global proxies

        try:
            urls_result = do_search_keyword(keyword)
        except Exception, e:
            print u'222:' + str(e)
            if str(e).find('HTTPSConnectionPool') >= 0:
                print u'MMMMax retries exceeded with url with do_search_keyword'

            else:
                print u'unknown error with do_search_keyword' + str(e)
            cursor.execute('insert into tyc_log_nofound values ("%s","%s","%s")' % (
                keyword, str(datetime.datetime.now()),
                str(datetime.datetime.now())[:10]))
            conn.commit()
            continue
        if urls_result:
            if urls_result[0] == '-1':
                print keyword + ' has no found'
                cursor.execute('insert into tyc_log_nofound values ("%s","%s","%s")' % (
                    keyword, str(datetime.datetime.now()),
                    str(datetime.datetime.now())[:10]))
                conn.commit()
                print u'插入nofound表'

            else:
                for url in urls_result:
                    proxies = get_proxy()
                    print url

                    try:
                        global cid
                        html = get_page(url)
                        cid = url.split('/')[-1]

                        global company_name
                        soup = BeautifulSoup(html.text, 'lxml')
                        company_name = soup.find_all('span', class_="f18 in-block vertival-middle sec-c2")[0].text
                        print company_name
                        print urllib.quote(company_name.encode('utf8'))
                        # cursor.execute(business_info(html))
                        # staff_info(html, cursor)
                        # shareholder_info(html, cursor)
                        # ==========上面的在跑了=========
                        # out_invest_info(html)
                        # change_info(html)
                        # product_info(html)
                        # wechat_info(html)
                        # website_record(html)
                        # lawsuit(html)
                        # court(html)
                        # zhixing(html)
                        # punish(html)
                        # recruit(html)
                        # patent(html)
                        # jingpin(html)
                        # copyR(html)
                        # copyrightWorks(html)
                        # firmProduct(html)
                        # investment_info(html)
                        # dishonest(html)

                        conn.commit()

                        print u'***************插入完成**************'
                        break

                    except Exception, e:

                        print u'error 2 with info: ' + str(e)
                        cursor.execute('insert tyc_log_nofound values ("%s","%s","%s")' % (
                            keyword, str(datetime.datetime.now()),
                            str(datetime.datetime.now())[:10]))
                        conn.commit()
                        print keyword + u' 跳过----------------------'
                        continue
        break


def do_search_keyword(keyword):
    while True:
        try:
            proxies2 = get_proxy()
            url = 'https://www.tianyancha.com/search?key=' + urllib.quote(
                keyword.encode('utf8')) + '&checkFrom=searchBox'
            print url
            headers = {
                'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
                'Host': 'www.tianyancha.com',
                'Referer': 'https://www.tianyancha.com/',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
            }
            html = requests.get(url, proxies=proxies2, headers=headers)
            # print html.text
            if html.text.__contains__('https://static.tianyancha.com/wap/images/notFound.png'):
                urls_result = ['-1']
                print u'nofound.img'
            else:
                urls_result = re.findall('<div class="search_right_item"><div><a href="(.*?)"', html.text, re.S)
            return urls_result
            break
        except Exception, e:
            print str(e)
            continue


def get_need_word():
    searched_list = []
    keyword_list = []
    to_search_list = []
    # with open("zhaopin_not_in_jsgsj_basic_info.csv", "r") as csvFile:
    with open("/Users/huaiz/PycharmProjects/tianyacha/label2.csv", "r") as csvFile:
        reader = csv.reader(csvFile)
        for crop_name in reader:
            item = crop_name[0].decode('utf-8')
            keyword_list.append(item)
    csvFile.close()

    cursor.execute('select keyword from tyc_business_info union select keyword from tyc_log_nofound')
    data = cursor.fetchall()

    for x in range(len(data)):
        searched_list.append(data[x][0])

    for item in keyword_list:
        if item not in searched_list:
            to_search_list.append(item)

    return to_search_list


def main(to_search_list):
    global keyword

    for keyword in to_search_list[1:]:
        print keyword

        do_keyword(keyword)


if __name__ == "__main__":
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="tianyancha", charset="utf8")
    cursor = conn.cursor()
#=========测试时用的清表==========
    # cursor.execute('truncate table tyc_log_nofound')
    # cursor.execute('truncate table tyc_business_info')
    # cursor.execute('truncate table tyc_lawsuit_info')
    # cursor.execute('truncate table tyc_shareholder_info')
    # cursor.execute('truncate table tyc_staff_info')
    # cursor.execute('truncate table tyc_webrecord_info')
    # cursor.execute('truncate table tyc_out_investment_info')
    # cursor.execute('truncate table tyc_change_record_info')
    # cursor.execute('truncate table tyc_product_info')
    # cursor.execute('truncate table tyc_wechat_info')
    # print '清表 tyc_log_nofound,tyc_business_info,tyc_outbound_investment,tyc_change_record,tyc_product_info,tyc_wechat_info'
# =========测试时用的清表==========

    keywords = get_need_word()
    main(keywords)
