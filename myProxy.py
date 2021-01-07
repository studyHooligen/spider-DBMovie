# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 19:43:49 2021

@author: 23731
"""

import urllib3
import json

class myProxy:
    def __init__(self,serverIP,serverPort):
        '''
        代理对象构造函数

        Parameters
        ----------
        serverIP : STRING
            服务器地址
        serverPort : STRING
            服务器端口

        Returns
        -------
        None.

        '''
        self._IP = serverIP;
        self._port = str(serverPort);
        self.httper = urllib3.PoolManager()
        
    def __del__(self):
        self.httper.clear()
        
    def getOne(self):
        res = self.httper.request('GET', self._IP+':'+self._port+'/get')
        if res.status == 200:
            return json.loads(res.data)['proxy']
        else:
            return 'ERROR'
        
    
    def getAll(self):
        res = self.httper.request('GET', self._IP+':'+self._port+'/get_all')
        if res.status == 200:
            js = json.loads(res.data)
            res = []
            for j in js:
                res.append(j['proxy']);
            return res;
        else:
            return 'ERROR'
    
    def getAvailNum(self):
        res = self.httper.request('GET',
                                     self._IP+':'+self._port+'/get_status')
        if res.status == 200:
            return json.loads(res.data)['count']
        else:
            return -1
        
    def deltOne(self,proxyIP):
        res = self.httper.request('GET',
                            self._IP+':'+self._port
                            +"/delete/?proxy={}".format(proxyIP));
        if res.status == 200:
            return True;
        else:
            return False;

if __name__ == '__main__':
    myProxyPool = myProxy("http://stream.singularity-blog.top",5010)
