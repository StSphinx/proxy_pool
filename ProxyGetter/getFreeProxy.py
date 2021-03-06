# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 
-------------------------------------------------
"""
import re
import sys

import requests

reload(sys)
# sys.setdefaultencoding('utf-8')

from Util.utilFunction import robustCrawl, getHtmlTree, getHtmlSoup

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()


class GetFreeProxy(object):
    """
    proxy getter
    """

    def __init__(self):
        pass

    @staticmethod
    @robustCrawl
    def freeProxyFirst(page=10):
        """
        抓取快代理IP http://www.kuaidaili.com/
        :param page: 翻页数
        :return:
        """
        url_list = ('http://www.kuaidaili.com/proxylist/{page}/'.format(page=page) for page in range(1, page + 1))
        # 页数不用太多， 后面的全是历史IP， 可用性不高
        header = {
            'Host': 'www.kuaidaili.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }

        for url in url_list:
            # tree = getHtmlTree(url, header=header)
            # proxy_list = tree.xpath('/html/body/*')
            html = requests.get(url=url, headers=header).content
            print html
            soap = getHtmlSoup(url=url, header=header)
            print soap
            index_free_list = soap.table
            print index_free_list
            # print proxy_list
            #
            # '//[@id="index_free_list"]/table/tbody/tr[1]/td[1]/text()'
            # for proxy in proxy_list:
            #     yield ':'.join(proxy.xpath('./td/text()')[0:2])
        print 'finish kuaidaili fetching proxy ip'

    @staticmethod
    @robustCrawl
    def freeProxySecond(proxy_number=100):
        """
        抓取代理66 http://www.66ip.cn/
        :param proxy_number: 代理数量
        :return:
        """
        url = "http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
            proxy_number)
        html = requests.get(url).content
        for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy
        print 'finish 66ip fetching proxy ip'

    @staticmethod
    @robustCrawl
    def freeProxyThird(days=1):

        """
        抓取有代理 http://www.youdaili.net/Daili/http/
        :param days:
        :return:
        """
        url = "http://www.youdaili.net/Daili/http/"
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'Hm_lvt_f8bdd88d72441a9ad0f8c82db3113a84=1487640273; Hm_lpvt_f8bdd88d72441a9ad0f8c82db3113a84=1487640642',
            'Host': 'www.youdaili.net',
            # 'If-Modified-Since': 'Tue, 21 Feb 2017 00:40:52 GMT',
            'If-None-Match': "5c67-548ffa1d8ca68-gzip",
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

        tree = getHtmlTree(url, header=header)
        page_url_list = tree.xpath('.//div[@class="chunlist"]/ul/li/p/a/@href')[0:days]
        for page_url in page_url_list:
            html = requests.get(page_url, headers=header).content
            # print html
            proxy_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)
            for proxy in proxy_list:
                yield proxy
        print 'finish youdaili fetching proxy ip'

    @staticmethod
    @robustCrawl
    def freeProxyFourth():
        """
        抓取西刺代理 http://api.xicidaili.com/free2016.txt
        :return:
        """

        # url = "http://api.xicidaili.com/free2016.txt"
        url = 'http://www.xicidaili.com/nn/'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            # 'Cookie:_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTI3OWQ2MmZlNzRhNjBkODVhODM5NWNkYzJkYWM1Mzc1BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMU42bFZ2NWRPUUlGNzNOUHBZTTNSMjhnVlJkL3MrYlBZYjhuL0sweVUxOWc9BjsARg%3D%3D--63d26ac91ca49227f33f19d0dab16f1a45f5dd5c; CNZZDATA1256960793=1622617834-1488331834-%7C1488331834
            'Host': 'www.xicidaili.com',
            'If-None-Match': 'W/"99fc3b208ce322f5e6b799290965ac14"',
            'Referer': 'http://www.xicidaili.com/wt/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

        tree = getHtmlTree(url=url, header=header)

        for i in range(10):
            ip_list = tree.xpath('//*[@id="ip_list"]/tbody/tr[2]/td[2]/text()')
            print ip_list
            # for tr in
            # ip = ip_list

            for row in ip_list:
                print row
                # ip = ip
                # print ip
                yield row
        # resp = requests.get(url=url, headers=header)
        # html = resp.content
        # for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
        #     yield proxy
        print 'finish xici fetching proxy ip'

    @staticmethod
    @robustCrawl
    def freeProxyFifth():
        """
        抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
        :return:
        """

        url_base = "http://www.goubanjia.com/free/gngn/index{}.shtml"

        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # Cookie:auth=49b87d158a2b9e02589295bb9b74e8cf; JSESSIONID=BE57CA28BB0D8DDC119A542A75216B30; CNZZDATA1253707717=2116078297-1487635832-%7C1487641386; Hm_lvt_2e4ebee39b2c69a3920a396b87bbb8cc=1487641109; Hm_lpvt_2e4ebee39b2c69a3920a396b87bbb8cc=1487641408
            'Host': 'www.goubanjia.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

        for tail in ['', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            url = url_base.format(tail)
            # print url
            tree = getHtmlTree(url, header=header)

            # 现在每天最多放15个（一页）
            for i in xrange(15):
                try:
                    d = tree.xpath('//*[@id="list"]/table/tbody/tr[{}]/td'.format(i + 1))[0]
                    # print d

                    o = d.xpath('.//span/text() | .//div/text()')
                    # print o
                except:
                    pass

                yield ''.join(o[:-1]) + ':' + o[-1]
                # print 'finish fetching index{}'.format(tail)
        print 'finish guobanjia fetching proxy ip'

    @staticmethod
    @robustCrawl
    def getKuaidaili():
        url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=988835387348925&num=500&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sep=1'
        resp = requests.get(url)
        proxy_list = resp.content.split('\r\n')
        for proxy in proxy_list:
            yield proxy


if __name__ == '__main__':
    gg = GetFreeProxy()
    # for e in gg.freeProxyFirst():
    #     print e
    # #
    # for e in gg.freeProxySecond():
    #     print e
    # #
    # for e in gg.freeProxyThird():
    #     print e
    #
    # for e in gg.freeProxyFourth():
    #     print e
    #
    # for e in gg.freeProxyFifth():
    #     print e

    # for i in gg.getKuaidaili():
    #     print i
