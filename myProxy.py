# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 19:43:49 2021

@author: 江榕煜

代理服务器API接口类

1. 构造对象即连接上代理服务器

2. 对象析构时，就释放连接

3. 调用getAll方法，获得目前所有的可用代理IP

4. 调用getOne方法，获得一个随机IP

5. 调用getAvailNum方法，获得可用代理的数量

6. 调用deltOne方法，删除服务器上已经注册的指定代理
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
        '''
        对象析构函数

        Returns
        -------
        None.

        '''
        self.httper.clear()
        
    def getOne(self):
        '''
        获得一个代理的IP字符串

        Returns
        -------
        STR
            IP:port字符串

        '''
        res = self.httper.request('GET', self._IP+':'+self._port+'/get')
        if res.status == 200:
            return json.loads(res.data)['proxy']
        else:
            return 'ERROR'
        
    
    def getAll(self):
        '''
        获得所有的IP构成的list

        Returns
        -------
        list of "IP:port"
            返回一个list，存储IP+port字符串

        '''
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
        '''
        获得服务器上可用代理服务器的数量

        Returns
        -------
        int
            可用数量.

        '''
        res = self.httper.request('GET',
                                     self._IP+':'+self._port+'/get_status')
        if res.status == 200:
            return json.loads(res.data)['count']
        else:
            return -1
        
    def deltOne(self,proxyIP):
        '''
        从服务器上删除一个指定的已经注册的代理

        Parameters
        ----------
        proxyIP : STR
            格式和getOne方法获得的“IP：port”一样.

        Returns
        -------
        BOOL
            删除成功或者失败

        '''
        res = self.httper.request('GET',
                            self._IP+':'+self._port
                            +"/delete/?proxy={}".format(proxyIP));
        if res.status == 200:
            return True;
        else:
            return False;

if __name__ == '__main__':
    myProxyPool = myProxy("http://stream.singularity-blog.top",5010)
