# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 21:01:35 2021

@author: 江榕煜

代理服务器测试主程序

"""

import myProxy
import urllib3 


#代理获取器
myProxyPool = myProxy.myProxy("http://stream.singularity-blog.top",5010)
    
num = myProxyPool.getAvailNum()

goodIPlist = []

print("当前可用代理数量："+str(num))

while num > 0:
    #下载器
    
    proxyIP = myProxyPool.getOne()
    
    proxyHttp = urllib3.ProxyManager("http://"+proxyIP)

    try:
        r = proxyHttp.request('GET',
                          'https://movie.douban.com/top250?start=0',
                          retries = 2,
                          timeout = 1)
    
    except :
        print('艹！垃圾代理被查水表了'+proxyIP);
        myProxyPool.deltOne(proxyIP);
        
    else:    
        if r.status == 200:
            print('这个代理是好的!'+proxyIP);
            goodIPlist.append(proxyIP);
        else:
            print('垃圾代理!无法成功查数据'+proxyIP);
            myProxyPool.deltOne(proxyIP);

    num -= 1;

goodIPlist
