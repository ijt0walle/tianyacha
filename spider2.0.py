#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from multiprocessing import Pool
import json
import hashlib
import datetime
import MySQLdb
import time
from bs4 import BeautifulSoup
import requests
import urllib

url_result = []
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

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="tianyancha", charset="utf8")
cursor = conn.cursor()


def detag(html):
    detag = re.subn('<script[^>]*>([\w\W]*?)</script>', '', html)[0]
    detag = detag.replace('&nbsp;', '')
    detag = detag.replace('&amp;', '&')
    detag = detag.replace("'", '|')
    detag = detag.replace('&ensp;', ';')
    detag = detag.replace('\t', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\r', '')
    detag = detag.replace('\\', '')
    detag = detag.replace('"', '')
    detag = detag.replace('{', '')
    detag = detag.replace('}', '')
    detag = re.subn('<[^>]*>', '', detag)[0]
    return detag.strip()


def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return (text)


def re_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


# 从用户搜索获取公司信息
def do_search_keyword():
    #    北京百度网讯科技有限公司
    keyword = raw_input('请输入企业名称、人名、产品名称或其它关键词 ：')
    url = 'https://www.tianyancha.com/search?key=' + urllib.quote(keyword) + '&checkFrom=searchBox'
    print url
    headers = {
        'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    html = requests.get(url, headers=headers)

    urls_result = re_findall('<div class="search_right_item"><div><a href="(.*?)"',html.text)

    print urls_result
    return urls_result


# 从数据库中获取公司信息
def keyword_from_db():
    pass


# 得到soup
def get_page(url):
    headers = {
        'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup


## 获取公司名和cid
def basic_info(soup):
    global company_name
    # global cid
    #
    # cid = re_findall('https://www.tianyancha.com/company/(.*?)',url)
    company_name = soup.select(
        '#company_web_top > div.companyTitleBox55.pt30.pl30.pr30 > div.company_header_width.ie9Style > div:nth-of-type(1) > span.f18.in-block.vertival-middle.sec-c2')[
        0].text


## 工商信息
def get_business_info(soup):
    # 注册资本
    registered_capital = soup.select(
        '#_container_baseInfo > div > div.baseInfo_model2017 > table > tbody > tr > td:nth-of-type(2) > div:nth-of-type(1) > div.pb10 > div')[
        0].text
    print registered_capital

    # 注册时间
    registration_time = soup.select(
        '#_container_baseInfo > div > div.baseInfo_model2017 > table > tbody > tr > td:nth-of-type(2) > div.new-border-bottom.pt10 > div.pb10 > div')[
        0].text
    print registration_time

    # 企业状态
    company_status = soup.select(
        '#_container_baseInfo > div > div.baseInfo_model2017 > table > tbody > tr > td:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div')[
        0].text
    print company_status

    # 工商注册号
    business_registration_number = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(1) > td:nth-of-type(1) > div > span')[
        0].text
    print business_registration_number

    # 组织机构代码
    organization_code = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > div > span')
    print organization_code

    # 统一信用代码
    uniform_credit_code = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(2) > td:nth-of-type(1) > div > span')[
        0].text
    print uniform_credit_code

    # 企业类型
    enterprise_type = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > div > span')[
        0].text
    print enterprise_type

    # 纳税人识别号
    taxpayer_identification_number = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(3) > td > div > span')[
        0].text
    print taxpayer_identification_number

    # 行业
    industry = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(4) > td:nth-of-type(1) > div > span')[
        0].text
    print industry

    # 营业期限
    business_term = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2) > div > span')[
        0].text
    print business_term

    # 核准日期
    approval_date = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(5) > td:nth-of-type(1) > div > span')[
        0].text
    print approval_date

    # 登记机关
    registration_authority = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > div > span')[
        0].text
    print registration_authority

    # 注册地址
    registered_address = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(6) > td > div > span')[
        0].text
    print registered_address

    # 英文名称
    english_name = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(7) > td > div > span')[
        0].text
    print english_name

    # 经营范围
    scope_of_business = soup.select(
        '#_container_baseInfo > div > div.row.b-c-white.base2017 > table > tbody > tr:nth-of-type(8) > td > div > span > span > span.js-full-container')[
        0].text
    print scope_of_business


## 主要人员
def staff_info(soup):
    num = soup.select('#nav-main-staffCount > span')[0].text
    print num
    for i in range(1, int(num) + 1):
        position = soup.select('#_container_staff > div > div > div:nth-of-type(' + str(
            i) + ') > div > div.in-block.f14.new-c5.pt9.pl10.overflow-width.vertival-middle > span')[0].text
        name = soup.select('#_container_staff > div > div > div:nth-of-type(' + str(i) + ') > div > a')[0].text
        ID = soup.select('#_container_staff > div > div > div:nth-of-type(' + str(i) + ') > div > a')[0]['href']

        print position, name, ID


## 股东信息
def shareholder_info(soup):
    num = soup.select('#nav-main-holderCount > span')[0].text
    for i in range(1, int(num) + 1):
        shareholder = soup.select(
            '#_container_holder > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(1) > a')[0].text
        ratio = \
            soup.select(
                '#_container_holder > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(2)')[
                0].text
        value = \
            soup.select(
                '#_container_holder > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(3)')[
                0].text
        print '股东: ', shareholder, ' 出资比例: ', ratio, ' 认缴出资:', value


## 对外投资
def outbound_investment(soup):
    num = soup.select('#nav-main-inverstCount > span')[0].text
    all_page_no = int(num) / 20 + 1
    last_page_no = int(num) % 20
    for i in range(1, int(all_page_no) + 1):
        if i < int(all_page_no):
            soup2 = get_invest_cookie(i)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])
                legal_representative_to_be_invested = re_findall('title="(.*?)"', source)
                span_part = re_findall('<span class=".*?">(.*?)</span>', source)
                print span_part[0]  # 被投资企业名称
                print legal_representative_to_be_invested[0]  # 被投资法定代表人
                print span_part[2]  # 注册资本
                print span_part[3]  # 投资数额
                print span_part[4]  # 投资占比
                print span_part[5]  # 注册时间
                print span_part[6]  # 状态
                print '--------------------------'
                cursor.execute(
                    'insert into tyc_outbound_investment values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                        company_name, span_part[0].decode('utf-8'),
                        legal_representative_to_be_invested[0].decode('utf-8'),
                        span_part[2].decode('utf-8'), span_part[3].decode('utf-8'), span_part[4].decode('utf-8'),
                        span_part[5].decode('utf-8'),
                        span_part[6].decode('utf-8'), str(datetime.datetime.now()), str(datetime.datetime.now())
                    ))
                conn.commit()
                print '对外投资---最后一页第'+str(x)+'条插入完成'

        else:

            for x in range(1, int(last_page_no) + 1):
                source = str(res[x])
                legal_representative_to_be_invested = re_findall('title="(.*?)"', source)
                span_part = re_findall('<span class=".*?">(.*?)</span>', source)
                print span_part[0]  # 被投资企业名称
                print legal_representative_to_be_invested[0]  # 被投资法定代表人
                print span_part[2]  # 注册资本
                print span_part[3]  # 投资数额
                print span_part[4]  # 投资占比
                print span_part[5]  # 注册时间
                print span_part[6]  # 状态
                print '--------------------------'
                return
                ('insert into tyc_outbound_investment values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                        company_name, span_part[0].decode('utf-8'),
                        legal_representative_to_be_invested[0].decode('utf-8'),
                        span_part[2].decode('utf-8'), span_part[3].decode('utf-8'), span_part[4].decode('utf-8'),
                        span_part[5].decode('utf-8'),
                        span_part[6].decode('utf-8'), str(datetime.datetime.now()), str(datetime.datetime.now())
                    ))
                conn.commit()
                print '对外投资---第'+str(x)+'条插入完成'


## 对外投资cookie部分
def get_invest_cookie(page_no):
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
    # --# print (tongji_url + '\n' + str(datetime.datetime.now()))
    tongji_page = requests.get(tongji_url, headers=head1, verify=False, )

    cookie = tongji_page.cookies.get_dict()
    js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
    # --# print js_code

    token = re.findall(r"token=(\w+);", js_code)[0]
    utm_code = re.findall("return'([^']*?)'", js_code)[0]
    t = ord(cid[0])

    fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
    fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
    fw.close()
    phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
    # --# print phantomResStr
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
    # print head2
    url = 'https://www.tianyancha.com/pagination/invest.xhtml?ps=20&pn=' + str(
        page_no) + '&id=' + cid + '&_=' + str(
        timestamp - 1)

    # print url

    resp = requests.get(url, headers=head2, verify=False)
    # print resp
    html = resp.text
    soup2 = BeautifulSoup(html, 'lxml')
    return soup2


## 变更记录
def change_record(soup):
    num = soup.select('#nav-main-changeCount > span')[0].text
    if num < 11:
        for i in range(1, int(num) + 1):
            change_time = soup.select(
                '#_container_changeinfo > div > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(1) > div')[0].text
            change_projects = soup.select(
                '#_container_changeinfo > div > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(2) > div')[0].text
            before_change = soup.select(
                '#_container_changeinfo > div > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(3) > div')[0].text
            after_change = soup.select(
                '#_container_changeinfo > div > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(4) > div')[0].text
    else:
        pass


## 产品信息
def product_info(soup):
    ## 获取个数
    num = soup.select('#nav-main-productinfo > span')[0].text
    for i in range(1, int(num) + 1):
        ## 图标
        product_icon = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type(' + str(
            i) + ') > td:nth-of-type(1) > img')[0]['src']

        ## 产品名称
        procduct_name = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type(' + str(
            i) + ') > td:nth-of-type(2) > span')[0].text

        ## 产品简称
        product_aka = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type(' + str(
            i) + ') > td:nth-of-type(3) > span')[0].text

        ## 产品分类
        product_category = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type(' + str(
            i) + ') > td:nth-of-type(4) > span')[0].text

        ## 领域
        product_field = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type(' + str(
            i) + ') > td:nth-of-type(5) > span')[0].text

        ## 操作
        product_action = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type(' + str(
            i) + ') > td:nth-of-type(6) > span')[0]['onclick']


## 微信公众号
def wechat_subscription(soup):
    num = soup.select('#nav-main-weChatCount > span')[0].text
    if num < 11:
        for i in range(1, int(num) + 1):
            icon = soup.select('#_container_wechat > div > div:nth-of-type(' + str(
                i) + ') > div.in-block.vertical-top.wechatImg > img')[0]['src']
            wechat_name = soup.select(
                '#_container_wechat > div > div:nth-of-type(3) > div.in-block.vertical-top.itemRight > div:nth-of-type(1)')[
                0].text
            wechat_num = soup.select('#_container_wechat > div > div:nth-of-type(' + str(
                i) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > span:nth-of-type(2)')[0].text
            introduction = soup.select('#_container_wechat > div > div:nth-of-type(' + str(
                i) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(3) > span.overflow-width.in-block.vertical-top')[
                0].text
            print icon, wechat_name, wechat_num, introduction
    else:
        pass


## 网站备案
def website_backup(soup):
    ## 获取个数

    num = soup.select('#nav-main-icpCount > span')[0].text
    for i in range(1, int(num) + 1):
        ## 审核时间
        auditing_time = soup.select(
            '#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(1) > span')[
            0].text

        ## 网站名称
        website_name = soup.select(
            '#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(2) > span')[
            0].text

        ## 网站首页
        homepage = soup.select(
            '#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(3) > a')[
            0].text

        ## 域名
        domain_name = \
        soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(4)')[
            0].text

        ## 备案号
        record_number = soup.select(
            '#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(5) > span')[
            0].text

        ## 状态
        state = soup.select(
            '#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(6) > span')[
            0].text

        ## 单位性质
        unit_character = soup.select(
            '#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(7) > span')[
            0].text





if __name__ == '__main__':
    urls_result=do_search_keyword()
    # url_result = ['https://www.tianyancha.com/company/22822']
    if urls_result:

        for url in urls_result:

            print url
            global cid

            soup=get_page(url)
            cid = url.split('/')[-1]
            basic_info(soup)
            print cid
            print company_name
            outbound_investment(soup)



