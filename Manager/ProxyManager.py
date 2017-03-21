# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py  
   Description :  
   Author :       JHao
   date：          2016/12/3
-------------------------------------------------
   Change Activity:
                   2016/12/3: 
-------------------------------------------------
"""
__author__ = 'JHao'

from DB.DbClient import DbClient
from ProxyGetter.getFreeProxy import GetFreeProxy
from Util.GetConfig import GetConfig


class ProxyManager(object):
    """
    ProxyManager
    """

    def __init__(self):
        self.db = DbClient()
        self.config = GetConfig()
        self.raw_proxy_queue = 'raw_proxy'
        self.useful_proxy_queue = 'useful_proxy_queue'

    def refresh(self):
        """
        fetch proxy into Db by ProxyGetter
        :return:
        """
        for proxyGetter in self.config.proxy_getter_functions:
            proxy_set = set()
            # fetch raw proxy
            for proxy in getattr(GetFreeProxy, proxyGetter.strip())():
                proxy_set.add(proxy)

            # store raw proxy
            self.db.changeTable(self.raw_proxy_queue)
            for proxy in proxy_set:
                print proxy
                self.db.put(proxy)

    def get(self):
        """
        return a useful proxy
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        return self.db.get()
        # return self.db.pop()

    def delete(self, proxy):
        """
        delete proxy from pool
        :param proxy:
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        self.db.delete(proxy)

    def getAll(self):
        """
        get all proxy from pool
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        return self.db.getAll()

    def get_status(self):
        self.db.changeTable(self.raw_proxy_queue)
        quan_raw_proxy = self.db.get_status()
        self.db.changeTable(self.useful_proxy_queue)
        quan_useful_queue = self.db.get_status()
        return {'raw_proxy': quan_raw_proxy, 'useful_proxy_queue': quan_useful_queue}

    @staticmethod
    def validate():
        import sys
        import multiprocessing
        sys.path.append('../')
        from Schedule.ProxyRefreshSchedule import main_check
        p = multiprocessing.Process(target=main_check, args=(10,))
        p.start()
        print 'useful_proxy_validating'


if __name__ == '__main__':
    pp = ProxyManager()
    pp.refresh()
    # print pp.get_status()
