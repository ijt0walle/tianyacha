#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from bs4 import BeautifulSoup
import requests
import urllib

url_result=[]


# def execCmd(cmd):
#     r = os.popen(cmd)
#     text = r.read()
#     r.close()
#     return text

# def detag(html):
#     detag = re.subn('<script[^>]*>([\w\W]*?)</script>','',html)[0]
#     detag = detag.replace('&nbsp;','')
#     detag = detag.replace('&amp;','&')
#     detag = detag.replace("'",'|')
#     detag = detag.replace('&ensp;',';')
#     detag = detag.replace('\t','')
#     detag = detag.replace('\n','')
#     detag = detag.replace('\r','')
#     detag = detag.replace('\\','/')
#     detag = re.subn('<[^>]*>','',detag)[0]
#     return detag.strip()

# def re_findall(pattern, html):
#     if re.findall(pattern, html, re.S):
#         return re.findall(pattern, html, re.S)
#     else:
#         return 'N'


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
    url_result=do_search_keyword()
    if url_result :
        for url in url_result:
            soup=get_page(url)
            basic_info(soup)
            get_companyRongzi(soup)
            get_jingpin(soup)
            get_productinfo(soup)
            get_icpCount(soup)
            print '------------分割线------------'

    else:
        print '''没有找到相关结果
        1.输入准确的关键词，重新搜索
        2.更换筛选条件，重新搜索
        3.试试“深度搜索”
        4.输入的关键词过于宽泛        '''
