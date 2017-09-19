#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from multiprocessing import Pool

import MySQLdb
import datetime
from bs4 import BeautifulSoup
import requests
import urllib

url_result = []


#
# conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="tianyancha", charset="utf8")
# cursor = conn.cursor()
#

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


# 从用户搜索获取公司信息
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

    return url_result


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


## 开头四个信息
def basic_info(soup):
    global company_name
    # soup = get_page(url)
    company_name = soup.find_all('span', class_="f18 in-block vertival-middle")[0].text
    print company_name


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
        soup.select('#_container_holder > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(2)')[
            0].text
        value = \
        soup.select('#_container_holder > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(3)')[
            0].text
        print '股东: ', shareholder, ' 出资比例: ', ratio, ' 认缴出资:', value


## 对外投资
def outbound_investment(soup):
    num = soup.select('#nav-main-inverstCount > span')[0].text
    if num < 11:
        for i in range(1, int(num) + 1):
            invested_enterprise = soup.select(
                '#_container_invest > div > div.out-investment-container > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(1) > a > span')
            legal_representative_to_be_invested = soup.select(
                '#_container_invest > div > div.out-investment-container > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(2) > span > a')
            registered_capital = soup.select(
                '#_container_invest > div > div.out-investment-container > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(3) > span')
            investment_amount = soup.select(
                '#_container_invest > div > div.out-investment-container > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(4) > span')
            investment_proportion = soup.select(
                '#_container_invest > div > div.out-investment-container > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(5) > span')
            registration_time = soup.select(
                '#_container_invest > div > div.out-investment-container > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(6) > span')
            state = soup.select(
                '#_container_invest > div > div.out-investment-container > table > tbody > tr:nth-of-type(' + str(
                    i) + ') > td:nth-of-type(7) > span')
    else:
        pass


## 变更记录
def change_record(soup):
    num = soup.select('#nav-main-changeCount > span')[0].text
    if num<11:
        for i in range(1,int(num)+1):
            change_time = soup.select('#_container_changeinfo > div > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(1) > div')[0].text
            change_projects = soup.select('#_container_changeinfo > div > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(2) > div')[0].text
            before_change = soup.select('#_container_changeinfo > div > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(3) > div')[0].text
            after_change = soup.select('#_container_changeinfo > div > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(4) > div')[0].text
    else:
        pass


## 产品信息
def product_info(soup):

    ## 获取个数
    num = soup.select('#nav-main-productinfo > span')[0].text
    for i in range(1, int(num) + 1):
        ## 图标
        product_icon = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(1) > img')[0]['src']

        ## 产品名称
        procduct_name = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(2) > span')[0].text

        ## 产品简称
        product_aka = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(3) > span')[0].text

        ## 产品分类
        product_category = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(4) > span')[0].text

        ## 领域
        product_field = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(5) > span')[0].text

        ## 操作
        product_action = soup.select('#_container_product > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(6) > span')[0]['onclick']


## 微信公众号
def wechat_subscription(soup):
    num = soup.select('#nav-main-weChatCount > span')[0].text
    if num<11:
        for i in range(1,int(num)+1):
            icon = soup.select('#_container_wechat > div > div:nth-of-type('+str(i)+') > div.in-block.vertical-top.wechatImg > img')[0]['src']
            wechat_name = soup.select('#_container_wechat > div > div:nth-of-type(3) > div.in-block.vertical-top.itemRight > div:nth-of-type(1)')[0].text
            wechat_num = soup.select('#_container_wechat > div > div:nth-of-type('+str(i)+') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > span:nth-of-type(2)')[0].text
            introduction = soup.select('#_container_wechat > div > div:nth-of-type('+str(i)+') > div.in-block.vertical-top.itemRight > div:nth-of-type(3) > span.overflow-width.in-block.vertical-top')[0].text
            print icon,wechat_name,wechat_num,introduction
    else:
        pass

## 网站备案
def website_backup(soup):

    ## 获取个数

    num = soup.select('#nav-main-icpCount > span')[0].text
    for i in range(1, int(num) + 1):
        ## 审核时间
        auditing_time = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(1) > span')[0].text

        ## 网站名称
        website_name = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(2) > span')[0].text

        ## 网站首页
        homepage = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(3) > a')[0].text


        ## 域名
        domain_name = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(4)')[0].text

        ## 备案号
        record_number = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(5) > span')[0].text


        ## 状态
        state = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(6) > span')[0].text


        ## 单位性质
        unit_character = soup.select('#_container_icp > div > div > table > tbody > tr:nth-of-type(' + str(i) + ') > td:nth-of-type(7) > span')[0].text


if __name__ == '__main__':
    url_result = ['https://www.tianyancha.com/company/22822']
    if url_result:
        # pool = Pool()
        # pool.map(get_business_info, url_result)
        # pool.map(basic_info,url_result)
        # soup=get_page(url)
        # basic_info(soup)
        # get_financing_history(soup)
        # get_conpetitive_product(soup)
        # get_productinfo(soup)
        # get_website_backup(soup)
        # get_business_info(soup)

        for url in url_result:
            soup = get_page(url)
            basic_info(soup)
            get_business_info(soup)
            staff_info(soup)
            shareholder_info(soup)
            outbound_investment(soup)
            change_record(soup)
            product_info(soup)
            wechat_subscription(soup)
            website_backup(soup)
            print '------------分割线------------'

    else:
        print '''没有找到相关结果
        1.输入准确的关键词，重新搜索
        2.更换筛选条件，重新搜索
        3.试试“深度搜索”
        4.输入的关键词过于宽泛'''
