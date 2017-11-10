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
import threading

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


# 清洗数据
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
# ------------ 模块获取  ------------
# ==================================


## 工商信息
def business_info(html, company_name):
    print html.text
    print u'爬取工商信息  ' + str(datetime.datetime.now())
    soup = BeautifulSoup(html.text, 'lxml')
    # 注册资本
    registered_capital = soup.select(
        '#_container_baseInfo > div > div.baseInfo_model2017 > table > tbody > tr > td:nth-of-type(2) > div:nth-of-type(1) > div.pb10 > div')[
        0].text

    # 注册时间
    registration_time = soup.select(
        '#_container_baseInfo > div > div.baseInfo_model2017 > table > tbody > tr > td:nth-of-type(2) > div.new-border-bottom.pt10 > div.pb10 > div')[
        0].text

    # 企业状态
    company_status = soup.select(
        '#_container_baseInfo > div > div.baseInfo_model2017 > table > tbody > tr > td:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div')[
        0].text

    # 工商注册号
    business_registration_number = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2)')[0].text

    # 组织机构代码
    organization_code = soup.select(

        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(1) > td:nth-of-type(4)')[0].text

    # 统一信用代码
    uniform_credit_code = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2)')[0].text

    # 企业类型
    enterprise_type = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(2) > td:nth-of-type(4)')[0].text

    # 纳税人识别号
    taxpayer_identification_number = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2)')[0].text

    # 行业
    industry = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(3) > td:nth-of-type(4)')[0].text

    # 营业期限
    business_term = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2) > span')[
        0].text

    # 核准日期
    approval_date = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(4) > td:nth-of-type(4)')[0].text

    # 登记机关
    registration_authority = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2)')[0].text

    # 注册地址
    registered_address = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(5) > td:nth-of-type(4)')[0].text

    # 英文名称
    english_name = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2)')[0].text

    # 经营范围
    scope_of_business = soup.select(
        '#_container_baseInfo > div > div.base0910 > table > tbody > tr:nth-of-type(7) > td:nth-of-type(2) > span > span > span.js-full-container')[
        0].text

    return[
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
        str(datetime.datetime.now())[:10]]

    # cursor.execute(
    #     'insert into tyc_business_info values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
    #         keyword,
    #         company_name,
    #         registered_capital,
    #         registration_time,
    #         company_status,
    #         business_registration_number,
    #         organization_code,
    #         uniform_credit_code,
    #         enterprise_type,
    #         taxpayer_identification_number,
    #         industry,
    #         business_term,
    #         approval_date,
    #         registration_authority,
    #         registered_address,
    #         english_name,
    #         scope_of_business,
    #         str(datetime.datetime.now()),
    #         str(datetime.datetime.now())[:10])
    # )


# ===================================
# ------------主逻辑功能区-------------
# ===================================


def get_need_word():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="tianyancha", charset="utf8")
    cursor = conn.cursor()
    searched_list = []
    keyword_list = []
    to_search_list = []
    with open("D:\\PycharmProjects\\tianyacha\\label.csv", "r") as csvFile:
        reader = csv.reader(csvFile)
        for crop_name in reader:
            item = crop_name[0].decode('utf-8')
            keyword_list.append(item)
    csvFile.close()

    cursor.execute('select keyword from tyc_business_info union select keyword from tyc_log_nofound')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    for x in range(len(data)):
        searched_list.append(data[x][0])

    for item in keyword_list:
        if item not in searched_list:
            to_search_list.append(item)
    return to_search_list[1:]


def main(keywords):
    global keyword

    keyword = keywords

    do_keyword(keyword)


def do_keyword(keyword):
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="tianyancha", charset="utf8")
    cursor = conn.cursor()
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
            #conn.commit()
            continue
        if urls_result:
            if urls_result[0] == '-1':
                print keyword + ' has no found'
                cursor.execute('insert into tyc_log_nofound values ("%s","%s","%s")' % (
                    keyword, str(datetime.datetime.now()),
                    str(datetime.datetime.now())[:10]))
                #conn.commit()
                print u'插入nofound表'

            else:
                for url in urls_result:
                    proxies = get_proxy()
                    print url

                    try:

                        html = get_page(url)

                        soup = BeautifulSoup(html.text, 'lxml')
                        company_name = soup.find_all('span', class_="f18 in-block vertival-middle sec-c2")[0].text
                        print company_name
                        print urllib.quote(company_name.encode('utf8'))
                        cursor.execute('insert into tyc_business_info values('
                                       '"%s","%s","%s","%s","%s","%s","%s","%s","%s",'
                                       '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                                       % tuple([keyword]+business_info(html, company_name))
                                       )
                        # for  x in business_info(html, company_name):
                        #     print x
                        # business_info(html, company_name)

                        #conn.commit()

                        print u'***************插入完成**************'
                        break
                    except Exception, e:
                        print u'error 2 with info: ' + str(e)
                        cursor.execute('insert tyc_log_nofound values ("%s","%s","%s")' % (
                            keyword, str(datetime.datetime.now()),
                            str(datetime.datetime.now())[:10]))
                        #conn.commit()
                        print keyword + u' 跳过----------------------'
                        continue
        break
    conn.commit()
    cursor.close()
    conn.close()

def get_page(url):
    headers = {
        'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    html = requests.get(url, proxies=proxies, timeout=60, headers=headers)
    return html


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
            html = requests.get(url, proxies=proxies2, timeout=60, headers=headers)
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


if __name__ == "__main__":

    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="tianyancha", charset="utf8")
    cursor = conn.cursor()
    # =========测试时用的清表==========
    # cursor.execute('truncate table tyc_log_nofound')
    # cursor.execute('truncate table tyc_business_info')
    # conn.commit()
    # cursor.close()
    # conn.close()
    # print '清表 '
    # =========测试时用的清表==========

    keywords = get_need_word()
    print type(keywords)
    print '%s keywords found!' % str(len(keywords))
    thread_num = 10
    start_no = 0

    while start_no < (len(keywords) - thread_num):
        threads = []
        for inner_index in range(0, thread_num):
            threads.append(
                threading.Thread(target=main, args=(keywords[start_no + inner_index],))
            )
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        start_no += thread_num
    print 'end'

    # main(keywords)
