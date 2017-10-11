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

def get_proxy():
    proxy_list = list(set(urllib.urlopen(
        'http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static').read().split('\n')[
                          :-1]))
    index = random.randint(0, len(proxy_list) - 1)
    current_proxy = proxy_list[index]
    print "NEW PROXY:\t%s" % current_proxy
    proxies = {"http": "http://" + current_proxy, "https": "http://" + current_proxy, }
    return proxies


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


def re_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


def execCmd(cmd):
    text = os.popen(cmd).read()
    return (text)


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


def get_invest_cookie(page_no):
    while True:
        try:
            proxies1= get_proxy()
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
            print tongji_url

            tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)
            print tongji_page.text

            cookie = tongji_page.cookies.get_dict()
            js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
            print cookie

            token = re.findall(r"token=(\w+);", js_code)[0]
            utm_code = re.findall("return'([^']*?)'", js_code)[0]
            t = ord(cid[0])
            print token
            print utm_code

            fw = open("/Users/huaiz/PycharmProjects/tianyacha/rsid.js", "wb+")
            fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
            fw.close()
            phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/tianyacha/rsid.js')
            # --print phantomResStr
            # print "phantomResStr: %s" % phantomResStr
            phantomRes = json.loads(phantomResStr)
            ssuid = phantomRes["ssuid"]
            utm = phantomRes["utm"]
            print ssuid
            print utm

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

            url = 'https://www.tianyancha.com/pagination/invest.xhtml?ps=20&pn=' + str(
                page_no) + '&id=' + cid + '&_=' + str(timestamp - 1)
            print url
            resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
            # print resp
            html = resp.text
            soup2 = BeautifulSoup(html,'lxml')
            return soup2
            break
        except Exception,e:
            print str(e)
            if str(e).find('list index out of range')>=0:
                print u'get_invest_cookie 代理失效 换一个试试'
            continue


def get_invest_info(html):
    print u'获取对外投资信息  ' + str(datetime.datetime.now())

    if html.text.__contains__('nav-main-inverst'):
        soup = BeautifulSoup(html.text,'lxml')
        num = soup.select('#nav-main-inverstCount > span')[0].text
        all_page_no = int(num) / 20 +1
        # 一共有多少页
        last_page_no = int(num) % 20
        # 最后一页有多少个
        for i in range(1,int(all_page_no)+1):
            soup2 = get_invest_cookie(i)
            res = soup2.select('tr')
            for x in range(1, len(res)):
                source = str(res[x])
                invested_person = re_findall('title="(.*?)',source)
                span_part = re_findall('<span class=".*?">(.*?)</span>',source)
                print span_part[0]  # 被投资企业名称
                print invested_person[0]  # 被投资法定代表人
                print span_part[2]  # 注册资本
                print span_part[3]  # 投资数额
                print span_part[4]  # 投资占比
                print span_part[5]  # 注册时间
                print span_part[6]  # 状态
                print '--------------------------'



    else:
        print '没有对外投资信息'

def main():
    while True:
        try:
            global proxies
            proxies = get_proxy()
            url = 'https://www.tianyancha.com/company/22822'
            global cid
            cid = url.split('/')[-1]
            html = get_page(url)
            get_invest_info(html)
            break
        except Exception,e:
            print 'error is ' +str(e)
            if str(e).find('HTTPSConnectionPool'):
                print 'get_page 的 HTTPSConnectionPool 有问题 再试一次'
            continue


if __name__ == "__main__":
    main()


