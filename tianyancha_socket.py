# encoding=utf-8
import time
import re
import urllib
import json
import datetime
import MySQLdb
import codecs
import urllib
import urllib2
import mechanize
import cookielib
import os
import hashlib
import codecs
import requests
import json
import random
import socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
socket.setdefaulttimeout(5)

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

user = '13951662526'
pwd = 'a19900726'
proxy_list = list(set(urllib.urlopen(
    'http://60.205.92.109/api.do?name=4078F5836501D892477E27080A8D067E&status=1&type=static').read().split('\n')[:-1]))

conn = MySQLdb.connect(host="localhost", user="root", passwd="somao1129", db="tianyancha", charset="utf8")
cursor = conn.cursor()


def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return (text)


def detag(html):
    detag = re.subn('<[^>]*>', '', html)[0]
    detag = detag.replace('&nbsp;', ' ')
    detag = detag.replace("'", '|')
    detag = detag.replace('&ensp;', ';')
    detag = detag.replace('\t', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\r', '')
    return detag


utm_dict = {
    u'1': u'6',
    u'3': u'0',
    u'6': u'3',
    u'11': u'd',
    u'13': u'e',
    u'14': u'a',
    u'18': u'f',
    u'19': u'4',
    u'21': u'b',
    u'23': u'7',
    u'25': u'c',
    u'27': u'8',
    u'29': u'2',
    u'30': u'1',
    u'31': u'9',
    u'36': u'5'
}


def getJob(corp_name):
    page_no = 1
    counter = 0
    print corp_name.encode('gbk')
    while True:
        if counter >= 5:
            print 'Max times tried!'
            quit()
        index = random.randint(0, len(proxy_list) - 1)
        current_proxy = proxy_list[index]
        print "NEW PROXY:\t%s" % current_proxy
        proxies = {"http": "http://" + current_proxy, "https": "http://" + current_proxy, }
        timestamp = int(time.time() * 1000)
        head = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 'www.tianyancha.com',
            'Origin': 'https://www.tianyancha.com',
            'Referer': 'https://www.tianyancha.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'
        }
        tongji_url = "https://www.tianyancha.com/tongji/" + urllib.quote(corp_name.encode('utf8')) + ".json?_=" + str(
            timestamp)
        print (tongji_url + '\n' + str(datetime.datetime.now()))
        time.sleep(0.5)
        try:
            tongji_page = requests.get(tongji_url, proxies=proxies, headers=head, verify=False, )
        except Exception as e:
            print e
            continue
        cookie = tongji_page.cookies.get_dict()
        js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])
        print js_code
        """
        if js_code.find("return'")==-1:
            print 'Invalid tongji! Refresh...'
            counter += 1
            continue
        """
        try:
            utm_code = re.findall("return'([^']*?)'", js_code)[0]
        except Exception as e:
            print e
            continue
        try:
            token = re.findall(r"token=(\w+);", js_code)[0]
        except Exception as e:
            print e
            continue
        t = ord(corp_name[0])
        fw = open("d:/crawler/tianyancha/rsid.js", "wb+")
        fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
        fw.close()
        phantomResStr = execCmd('phantomjs D:\\crawler\\tianyancha\\rsid.js')
        print phantomResStr
        phantomRes = json.loads(phantomResStr)
        ssuid = phantomRes["ssuid"]
        utm = phantomRes["utm"]
        """
        head = {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Host': 'clkst.tianyancha.com',
                    'Referer': 'https://www.tianyancha.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Cookie' : 'ssuid='+ssuid,
                    'X-Requested-With': 'XMLHttpRequest'
                }

        resp = requests.get('https://clkst.tianyancha.com/pingd?srctype=getsret&lurl=https%3A//www.tianyancha.com/company/22822&ch=CompangyDetail.zhaopin&sc=person&ourl=&ssuid='+ssuid+'&mobi=undefined&rand=0.47675939766010433', headers=head, verify=False)
        """
        head = {
            'Host': 'www.tianyancha.com',
            # 'Referer': 'https://www.tianyancha.com/company/22822',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            # 'Cookie' : 'ssuid='+ssuid+'; token='+token+'; _utm='+utm+'; aliyungf_tc='+cookie["aliyungf_tc"]+'; TYCID='+cookie["TYCID"]+'; csrfToken='+cookie["csrfToken"]+'; uccid='+cookie["uccid"],
            'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
                "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie["csrfToken"] + '; uccid=' +
                      cookie["uccid"],
            'X-Requested-With': 'XMLHttpRequest'
        }
        url = 'https://www.tianyancha.com/pagination/recruit.xhtml?ps=10&pn=' + str(page_no) + '&name=' + urllib.quote(
            corp_name.encode('utf8')) + '&_=' + str(timestamp - 1)
        print (url)
        time.sleep(0.5)
        try:
            resp = requests.get(url, proxies=proxies, headers=head, verify=False)
        except Exception as e:
            print e
            continue
        # with codecs.open('d:/crawler/tianyancha_job.csv','wb+') as df:
        #    df.write(resp.text.encode('utf8'))
        # quit()
        # print (resp.text.encode('utf8'))
        if resp.text.find('<table class="table  companyInfo-table">') == -1 or resp.text.find('/forbidden3.png') >= 0:
            print url
            print 'Invalid job result'
            with codecs.open('d:/crawler/tianyancha_job.csv', 'wb+') as df:
                df.write(resp.text.encode('utf8'))
            continue
        html = resp.text
        blocks = re.findall("onclick='employePopup\(([\w\W]*?)\);", html)
        for block in blocks:
            # print block
            try:
                js = json.loads(block.replace('\\u002F', '\\\\\\\\'))
            except Exception as e:
                print e
                with codecs.open('d:/crawler/tianyancha_job_block.csv', 'wb+') as df:
                    df.write(block.encode('utf8'))
                continue
            sqlstr = "insert into tianyancha_job_detail values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            corp_name, js["id"], js["title"], js["city"], js["district"], js["companyName"], js["oriSalary"],
            js["urlPath"], js["startdate"], js["enddate"], js["source"], js["education"], js["employerNumber"],
            js["experience"], js["createTime"], js["updateTime"], js["description"].replace("'", "`"),
            str(datetime.datetime.now()))
            # print sqlstr
            cursor.execute(sqlstr)
        if len(blocks) < 10:
            print 'Last Page.'
            break
        page_no += 1
    cursor.execute(
        "insert into tianyancha_job_detail_log values ('%s','%s','%s')" % (corp_name, "", str(datetime.datetime.now())))
    conn.commit()


sqlstr = "select a.corp_name from  lanxi.lanxi_tianyancha_job_corps a left join tianyancha_job_detail_log b on a.corp_name=b.corp_name where b.corp_name is null"
cursor.execute(sqlstr)
pairs = cursor.fetchall()
print '%s records found!' % len(pairs)
for pair in pairs:
    getJob(pair[0])
quit()

url = 'https://www.tianyancha.com/pagination/recruit.xhtml?ps=10&pn=2&name=' + urllib.quote(
    corp_name.encode('utf8')) + '&_=' + str(int(time.time() * 1000))
url = 'https://www.tianyancha.com/pagination/recruit.xhtml?ps=10&pn=2&name=%E5%8C%97%E4%BA%AC%E7%99%BE%E5%BA%A6%E7%BD%91%E8%AE%AF%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&_=1504505259819'
print url
if True:
    s = requests.Session()
    m = hashlib.md5()
    m.update(pwd)
    head = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'www.tianyancha.com',
        'Origin': 'https://www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/login',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = 'https://www.tianyancha.com/cd/login.json'
    data = {"mobile": user, "cdpassword": m.hexdigest(), "loginway": "PL", "autoLogin": True}
    response = requests.post(url, json.dumps(data), headers=head, verify=False)  # payload request
    print response.text
    auth_token = json.loads(response.text)["data"]["token"]
    print "Token:\t%s" % auth_token
    cookie = response.cookies.get_dict()
    cookie["auth_token"] = auth_token
    head = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'www.tianyancha.com',
        'Origin': 'https://www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Cookie' : 'auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk1MTY2MjUyNiIsImlhdCI6MTUwNDQwMjQxNywiZXhwIjoxNTE5OTU0NDE3fQ.t8y-2GaFhuw5PjyT5vfhPOSuXNhtOPn4kZ0igZLUgFbXfXD1pgFcnj11Ra05dVxX7Ka6Vnry0LEws8oohgOmjA; aliyungf_tc=AQAAAAa7sxOPlwsAMD3teVzFyle6Ry6W; csrfToken=_5LB0HVJa5BpllR2eHo7rbFM; _csrf=9SRgjhjGnHexZbzIdwUt1g==; OA=JNSj/VX9XKrwTcwpGqzruTKjGts6SB4IWOH1RI9ErBje279lyoMBp1Gz9DJI7e1V; _csrf_bk=5e14877058ba36ead13687743f28b560; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1504426059,1504426087,1504431017,1504505216; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504505260; token=7e1f6c24adb549fea603f3c242a110a3; _utm=eaf1cf245b9e4fada864a2ad08bec111; auth_token='+token ,
        'X-Requested-With': 'XMLHttpRequest'
    }
    resp = requests.get('https://www.tianyancha.com/company/22822', cookies=cookie, headers=head, verify=False)
    cookie = resp.cookies.get_dict()
    with codecs.open('d:/crawler/tianyancha.csv', 'wb+') as df:
        df.write(resp.text.encode('utf8'))

    resp = s.get(url, headers=head, verify=False)
    with codecs.open('d:/crawler/tianyancha_job.csv', 'wb+') as df:
        df.write(resp.text.encode('utf8'))
    if resp.text.find('<span id="ipContentIe">') >= 0:
        print 'Checking!'
    quit()

# Search API
conn = MySQLdb.connect(host="localhost", user="root", passwd="somao1129", db="tianyancha", charset="utf8")
cursor = conn.cursor()
sqlstr = "select distinct distinct a.corp_name from lanxi_corps a left join tianyancha_search b on a.corp_name=b.corp_name where b.corp_name is null "
cursor.execute(sqlstr)
pairs = cursor.fetchall()
print '%s records found!' % len(pairs)
for pair in pairs:
    s = requests.Session()
    print pair[0]
    for i in range(0, 10):
        try:
            index = random.randint(0, len(proxy_list) - 1)
            current_proxy = proxy_list[index]
            print "NEW PROXY:\t%s" % current_proxy
            proxies = {"http": "http://" + current_proxy, "https": "http://" + current_proxy, }
            url = 'https://www.tianyancha.com/search?key=' + urllib.quote(pair[0].encode('utf8'))
            # url = 'https://www.baidu.com'
            print url
            # resp = s.get(url, proxies=proxies)
            time.sleep(0.5)
            resp = s.get(url, proxies=proxies, verify=False, timeout=5)
            if resp.text.find('b-c-white search_result_container') == -1 or resp.text.find(
                    'module module1 module2 loginmodule collapse in') >= 0:
                print 'NOT search PAGE!'
                continue
            break
        except Exception as e:
            print e
    corps = re.findall(
        '<a href="https://www\.tianyancha\.com/company/([^"]*?)"[^>]*>[^<]*<span ng-class="inClick[^>]*>([\w\W]*?)</span></a>',
        resp.text)
    print "%s corps found!" % len(corps)
    if len(corps) != 0:
        with codecs.open('d:/crawler/tianyancha.csv', 'wb+') as df:
            df.write(resp.text.encode('utf8'))
    for corp in corps:
        cursor.execute("insert into tianyancha_search values ('%s','%s','%s','%s')" % (
        pair[0], detag(corp[1]).strip(), corp[0], str(datetime.datetime.now())))
        cursor.execute("insert into tianyancha_search_log values ('%s','%s','%s')" % (
        detag(corp[1]).strip(), "", str(datetime.datetime.now())))
    sqlstr = "insert into tianyancha_search_log values ('%s','%s','%s')" % (pair[0], "", str(datetime.datetime.now()))
    # print sqlstr
    cursor.execute(sqlstr)
    conn.commit()
    # break

cursor.close()
conn.close()
print 'end'
quit()

s = requests.Session()
url = 'https://www.tianyancha.com/cd/login.json'
data = {"mobile": user, "cdpassword": m.hexdigest(), "loginway": "PL", "autoLogin": True}
response = s.post(url, json.dumps(data), headers=head, verify=False)
print response.text
token = json.loads(response.text)["data"]["token"]
head = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'www.tianyancha.com',
    'Origin': 'https://www.tianyancha.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    # Cookie可以只保留auth_token值，其他删除
    'Cookie': 'auth_token=' + token + '; aliyungf_tc=AQAAAFl/5FsNHA8AlaRf3qSqohKjpHng; TYCID=7816e0c08ecb11e7a46507f51ebfe434; csrfToken=HjcUN_l33t69609WkWzVdz3A; ssuid=9540458009; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk1MTY2MjUyNiIsImlhdCI6MTUwNDI0OTcwNSwiZXhwIjoxNTE5ODAxNzA1fQ.mDKZFyT2PPZF4brxKzPha-BgHrZQ3Y7ufYGsw8IxUDu-QQKhkqnrOTITiutAsKqjezmTjRCoOQhYTvvQb2v7bw%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213951662526%2522%257D; _csrf=Fmw5GzuhSy2/7UQtlqh+ZQ==; OA=AL9vz33KWhXLo3tkh1sB6YPIwFY//l/oj4PXb5r4ceVdEXUt1AUFcZ3STasQRrLk; _csrf_bk=10e31a467ce6cdc5d3dabd9828a9e36c; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1504061727,1504143346,1504171835,1504235689; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504249717',
    'X-Requested-With': 'XMLHttpRequest'
}

resp = s.get("https://www.tianyancha.com/usercenter/concern/1", headers=head, verify=False)
with codecs.open('d:/crawler/tianyancha/tianyancha.csv', 'wb+') as df:
    df.write(resp.text.encode('utf8'))
