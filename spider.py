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








def get_page():
    url = "https://www.tianyancha.com/company/12949891"
    br = mechanize.Browser()
    br.addheaders = [
        ('Accept', 'application/json, text/javascript, */*; q=0.01') \
        , ('Accept-Encoding', 'gzip, deflate, br') \
        , ('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6') \
        , ('Connection', 'keep-alive') \
        , ('Cookie', 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719;ssuid=6805162414; RTYCID=d6928b5fe88243489ad83678134a5e06; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODU1MTk4NjYyNSIsImlhdCI6MTUwNDE0NDg1MCwiZXhwIjoxNTE5Njk2ODUwfQ.ChipyAlCl7j08qBgYW8nsR46mIs91UTI80IftelNgjDf59KZ6JWWQm9BDonBKsl5UKyO44PtnzV1olf-RjUXMQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218551986625%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODU1MTk4NjYyNSIsImlhdCI6MTUwNDE0NDg1MCwiZXhwIjoxNTE5Njk2ODUwfQ.ChipyAlCl7j08qBgYW8nsR46mIs91UTI80IftelNgjDf59KZ6JWWQm9BDonBKsl5UKyO44PtnzV1olf-RjUXMQ; aliyungf_tc=AQAAAIrjRh3IugIAlaRf3sGFCOfYdqPV; csrfToken=sWaDXU2nJB0QKqUAV0D8XSzN; bannerFlag=true; OA=e+gaygcWZ84c32kAIH2c9feRsbYPaO9so59OI1hKLF4bER8rcljLYdw2EDQSPJZc; _csrf=HzN2RRmaxND842F/ICyCpQ==; _csrf_bk=e73360ec0593474650ab26dac3b35170; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504176400') \
        , ('Host', 'www.tianyancha.com') \
        , ('Referer', 'https://www.tianyancha.com/') \
        , ('User-Agent',
           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36') \
        , ('X-Requested-With', 'XMLHttpRequest')\
    ]

    html = br.open(url).read()
    soup = BeautifulSoup(html,'lxml')
    # print soup.prettify()
    return soup

def basic_info(soup):
    ### 开头四个信息
    ## 公司名
    print soup.find_all('span',class_="f18 in-block vertival-middle")[0].text
    ## 电话
    print soup.find_all('div', class_="in-block vertical-top overflow-width mr20")[0].text
    ## 网址
    print soup.find_all('div', class_="in-block vertical-top overflow-width mr20")[1].text
    ## 邮箱
    print soup.find_all('div', class_="in-block vertical-top")[0].text

    # print soup.find_all('div', id="_container_jingpin")[0].text

def get_jingpin(soup):
    ### 竞品信息
    ## 获取个数
    try:
        num = soup.select('#nav-main-companyJingpin > span')[0].text
        for i in  range(1,int(num)+1):
            ## 产品
            print soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td > img')[0]['alt']
            ## 图片地址
            print soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td > img')[0]['src']
            ## 地区
            print soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(2) > span')[0].text
            ## 当前轮次
            print soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(3) > span')[0].text
            ## 行业
            print soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(4) > span')[0].text
            ## 业务
            print soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(5) > span')[0].text
            ## 成立时间
            print soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(6) > span')[0].text
            ## 估值
            print soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td.val')[0].text
    except Exception,e:
        if str(e).find('list index out of range')>=0:
            print '页面中没有 -竞品信息- 的对应信息'
        else:
            print '竞品信息 ' + e




def get_companyRongzi(soup):
    ### 融资历史
    ## 获取个数
    try:
        num = soup.select('#nav-main-companyRongzi > span')[0].text
        for i in range(1,int(num)+1):
            ## 时间
            print soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(1) > span')[0].text
            ## 轮次
            print soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(2) > span')[0].text
            ## 估值
            print soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(3) > span')[0].text
            ## 金额
            print soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(4) > span')[0].text
            ## 比例
            print soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(5) > span')[0].text
            ## 投资方
            print soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(6)')[0].text
            ## 新闻来源
            print soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(7) > span')[0].text
    except Exception,e:
        if str(e).find('list index out of range')>=0:
            print '页面中没有 -融资历史- 的对应信息'
        else:
            print '融资历史 ' + e

def get_productinfo(soup):
    ### 产品信息
    ## 获取个数
    try:
        num = soup.select('#nav-main-productinfo > span')[0].text
        for i in range(1, int(num) + 1):
            ## 图标
            print soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(1) > img')[0]['src']
            ## 产品名称
            print soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(2) > span')[0].text
            ## 产品简称
            print soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(3) > span')[0].text
            ##产品分类
            print soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(4) > span')[0].text
            ## 领域
            print soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(5) > span')[0].text
            ## 操作
            print soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(6) > span')[0]['onclick']
    except Exception, e:
        if str(e).find('list index out of range') >= 0:
            print '页面中没有 -产品信息- 的对应信息'
        else:
            print '产品信息 ' + e



def get_icpCount(soup):
    ### 网站备案
    ## 获取个数
    try:
        num = soup.select('#nav-main-icpCount > span')[0].text
        for i in range(1, int(num) + 1):
            ## 审核时间
            print soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(1) > span')[0].text
            ## 网站名称
            print soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(2) > span')[0].text
            ## 网站首页
            print soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(3) > a')[0].text
            ## 域名
            print soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(4)')[0].text
            ## 备案号
            print soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(5) > span')[0].text
            ## 状态
            print soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(6) > span')[0].text
            ## 单位性质
            print soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(7) > span')[0].text
    except Exception, e:
        if str(e).find('list index out of range') >= 0:
            print '页面中没有 -网站备案- 的对应信息'
        else:
                print '网站备案 ' + e



if __name__=='__main__':
    soup = get_page()
    basic_info(soup)
    get_companyRongzi(soup)
    get_jingpin(soup)
    get_productinfo(soup)
    get_icpCount(soup)