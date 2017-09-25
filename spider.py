#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os

import MySQLdb
import datetime
from bs4 import BeautifulSoup
import requests
import urllib

url_result=[]

conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="tianyancha", charset="utf8")
cursor = conn.cursor()


def detag(html):
    detag = re.subn('<script[^>]*>([\w\W]*?)</script>','',html)[0]
    detag = detag.replace('&nbsp;','')
    detag = detag.replace('&amp;','&')
    detag = detag.replace("'",'|')
    detag = detag.replace('&ensp;',';')
    detag = detag.replace('\t','')
    detag = detag.replace('\n','')
    detag = detag.replace('\r','')
    detag = detag.replace('\\','')
    detag = detag.replace('"','')
    detag = detag.replace('{', '')
    detag = detag.replace('}', '')
    detag = re.subn('<[^>]*>','',detag)[0]
    return detag.strip()


# 从用户搜索获取公司信息
def do_search_keyword():
    keyword = raw_input('请输入企业名称、人名、产品名称或其它关键词 ：')
    url = 'https://www.tianyancha.com/search?key='+urllib.quote(keyword)+'&checkFrom=searchBox'

    headers = {
        'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    soup_list = BeautifulSoup(html.text, 'lxml')

    urls= soup_list.select('#web-content > div > div > div > div.col-9.search-2017-2.pr10.pl0 > div.b-c-white.search_result_container > div > div.search_right_item > div.row.pb5 > div.col-xs-10.search_repadding2.f18 > a')
    for url in urls:
        url_result.append(url['href'])

    return url_result


# 从数据库中获取公司信息
def keyword_from_db():
    pass


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


### 开头四个信息
def basic_info(soup):
    global company_name
    try:
        ## 公司名
        company_name = soup.find_all('span',class_="f18 in-block vertival-middle")[0].text
        print company_name+str(datetime.datetime.now())
        ## 电话
        phone = soup.find_all('div', class_="in-block vertical-top overflow-width mr20")[0].text
        print phone
        ## 网址
        website = soup.find_all('div', class_="in-block vertical-top overflow-width mr20")[1].text
        print website
        ## 邮箱
        email = soup.find_all('div', class_="in-block vertical-top")[0].text
        print email

        cursor.execute(
            'insert into tianyancha_basic values("%s","%s","%s","%s","%s")' % (
                detag(company_name), detag(phone), detag(website), detag(email),str(datetime.datetime.now())))
        conn.commit()
    except Exception,e:
        print '四项基本信息获取失败'
        cursor.execute(
            'insert into tianyancha_error_log values("%s","%s","%s","%s")' % (
                detag(company_name), 'basic_info',e, str(datetime.datetime.now())))
        conn.commit()


### 竞品信息
def get_conpetitive_product(soup):
    ## 获取个数

    try:
        num = soup.select('#nav-main-companyJingpin > span')[0].text
        for i in  range(1,int(num)+1):
            ## 产品
            name = soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td > img')[0]['alt']

            print name
            ## 图片地址
            img_url = soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td > img')[0]['src']

            print img_url
            ## 地区
            location = soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(2) > span')[0].text

            print location
            ## 当前轮次
            round = soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(3) > span')[0].text

            print round
            ## 行业
            industry = soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(4) > span')[0].text

            print industry
            ## 业务
            bussiness = soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(5) > span')[0].text

            print bussiness
            ## 成立时间
            found_time = soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(6) > span')[0].text

            print found_time
            ## 估值
            valuation = soup.select('#_container_jingpin > div > table > tbody > tr:nth-of-type('+str(i)+') > td.val')[0].text

            print valuation

            cursor.execute(
                'insert into tianyancha_conpetitive_product values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                    detag(company_name),detag(name), detag(img_url), detag(location), detag(round),detag(industry),detag(bussiness), detag(found_time),detag(valuation),str(datetime.datetime.now())))
            conn.commit()


    except Exception,e:
        if str(e).find('list index out of range')>=0:
            print '页面中没有 -竞品信息- 的对应信息'
        else:
            print '竞品信息 出错 详情查阅日志  --  ' + str(datetime.datetime.now())
            cursor.execute(
                'insert into tianyancha_error_log values("%s","%s","%s","%s")' % (
                    detag(company_name),'get_conpetitive_product',e,
                    str(datetime.datetime.now())))
            conn.commit()


### 融资历史
def get_financing_history(soup):

    ## 获取个数
    try:
        num = soup.select('#nav-main-companyRongzi > span')[0].text
        for i in range(1,int(num)+1):
            ## 时间
            time = soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(1) > span')[0].text
            print time
            ## 轮次
            round = soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(2) > span')[0].text
            print round
            ## 估值
            valuation = soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(3) > span')[0].text
            print valuation
            ## 金额
            amount = soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(4) > span')[0].text
            print amount
            ## 比例
            scale = soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(5) > span')[0].text
            print scale
            ## 投资方
            investor = soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(6)')[0].text
            print investor
            ## 新闻来源
            news_sources = soup.select('#_container_rongzi > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(7) > span')[0].text
            print news_sources

            cursor.execute(
                'insert into tianyancha_financing_history values("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                    detag(company_name), detag(time), detag(round), detag(valuation), detag(amount), detag(scale), detag(investor), detag(news_sources),
                    str(datetime.datetime.now())))
            conn.commit()

    except Exception,e:
        if str(e).find('list index out of range')>=0:
            print '页面中没有 -融资历史- 的对应信息'
        else:
            print '融资历史 出错 详情查阅日志  --  ' + str(datetime.datetime.now())
            cursor.execute(
                'insert into tianyancha_error_log values("%s","%s","%s","%s")' % (
                detag(company_name),'get_financing_history',e,
                str(datetime.datetime.now())))
            conn.commit()


### 产品信息
def get_productinfo(soup):

    ## 获取个数
    try:
        num = soup.select('#nav-main-productinfo > span')[0].text
        for i in range(1, int(num) + 1):
            ## 图标
            product_icon = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(1) > img')[0]['src']

            print product_icon
            ## 产品名称
            procduct_name = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(2) > span')[0].text

            print procduct_name
            ## 产品简称
            product_aka = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(3) > span')[0].text

            print product_aka
            ## 产品分类
            product_category = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(4) > span')[0].text

            print product_category
            ## 领域
            product_field = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(5) > span')[0].text

            print product_field
            ## 操作
            product_action = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(6) > span')[0]['onclick']

            print detag(product_action)

            cursor.execute(
                'insert into tianyancha_productinfo values("%s","%s","%s","%s","%s","%s","%s","%s")' % (
                    detag(company_name), detag(product_icon), detag(procduct_name), detag(product_aka), detag(product_category), detag(product_field), detag(product_action),
                    str(datetime.datetime.now())))
            conn.commit()

    except Exception, e:
        if str(e).find('list index out of range') >= 0:
            print '页面中没有 -产品信息- 的对应信息'

        else:
            cursor.execute(
                'insert into tianyancha_error_log values("%s","%s","%s","%s")' % (
                    detag(company_name), 'get_productinfo', e,
                    str(datetime.datetime.now())))
            conn.commit()
            print '产品信息 出错 详情查阅日志  --  ' + str(datetime.datetime.now())


### 网站备案
def get_website_backup(soup):

    ## 获取个数
    try:
        num = soup.select('#nav-main-icpCount > span')[0].text
        for i in range(1, int(num) + 1):
            ## 审核时间
            auditing_time = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(1) > span')[0].text

            print auditing_time
            ## 网站名称
            name = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(2) > span')[0].text

            print name
            ## 网站首页
            homepage = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(3) > a')[0].text

            print homepage
            ## 域名
            domain_name = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(4)')[0].text

            print domain_name
            ## 备案号
            record_number = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(5) > span')[0].text

            print record_number
            ## 状态
            state = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(6) > span')[0].text

            print state
            ## 单位性质
            unit_character = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(7) > span')[0].text

            print unit_character

            cursor.execute(
                'insert into tianyancha_website_backup values("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                    detag(company_name), detag(auditing_time), detag(name), detag(homepage), detag(domain_name), detag(record_number),detag(state),detag(unit_character),
                    str(datetime.datetime.now())))
            conn.commit()


    except Exception, e:
        if str(e).find('list index out of range') >= 0:
            print '页面中没有 -网站备案- 的对应信息'
        else:
            print e
            print '网站备案 出错 详情查阅日志  --  ' + str(datetime.datetime.now())
            cursor.execute(
                'insert into tianyancha_error_log values("%s","%s","%s","%s")' % (
                    detag(company_name), 'get_website_backup', e,
                    str(datetime.datetime.now())))
            conn.commit()


if __name__== '__main__':
    url_result=do_search_keyword()
    if url_result :
        for url in url_result:
            soup=get_page(url)
            basic_info(soup)
            get_financing_history(soup)
            get_conpetitive_product(soup)
            get_productinfo(soup)
            get_website_backup(soup)
            print '------------分割线------------'

    else:
        print '''没有找到相关结果
        1.输入准确的关键词，重新搜索
        2.更换筛选条件，重新搜索
        3.试试“深度搜索”
        4.输入的关键词过于宽泛'''
