# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     utilFunction.py  
   Description :  tool function
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 添加robustCrawl、verifyProxy、getHtmlTree
-------------------------------------------------
"""
import requests
from bs4 import BeautifulSoup
from lxml import etree

# noinspection PyPep8Naming
def robustCrawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print u"sorry, 抓取出错。错误原因:"
            print e

    return decorate


def verifyProxy(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    return True if re.findall(verify_regex, proxy) else False


def getHtmlTree(url, header=None, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """

    html = requests.get(url=url, headers=header).content
    return etree.HTML(html)


def getHtmlSoup(url, header=None, **kwargs):
    html =requests.get(url=url, headers=header).content
    return BeautifulSoup(html, "lxml")

