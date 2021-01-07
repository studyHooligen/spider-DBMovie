# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 20:28:40 2021

@author: 江榕煜

豆瓣电影top250电影主页面分析器

"""

from bs4 import BeautifulSoup
import myCSV

def top250analyse(urlManager,   # url管理器
                  httper,   # 不使用代理，直接下载器下载
                  # proxy,
                  graphDB,       #图数据库操作器
                  HTMLsavePath = None,     #爬取到的页面存储位置
                  ):
    
    #根路径
    urlRoot = "https://movie.douban.com/top250?start="

    pageNum = 0 #遍历用的页面号
    while pageNum < 10:
        
        urlNow = urlRoot + str(pageNum*25)    #当前要爬的路径
        
        r = httper.request('GET',urlNow)  #下载数据
        
        if(r.status != 200):    #检测是否请求失败（被豆瓣查水表）
            print("豆瓣250页面分析执行失败，WEB状态码：",str(r.status))
            print("失败前已爬取至："+str(pageNum+1)+"段主页面")
            exit(-1)
        
        pageNum += 1    #迭代
        
        if HTMLsavePath != None :
            '''
            存储网页数据
            '''
            localSaveFile = open(HTMLsavePath + "/豆瓣电影top250-"+str(pageNum)+".html",mode = "wb")
            
            localSaveFile.write(r.data) #存储网页数据
            
            localSaveFile.close()   #关闭文件
        
        '''
        开始分析网页文件
        '''
        wholeHTML_bsObj = BeautifulSoup(r.data,"html.parser",from_encoding="utf-8")
        
        mainGrid = wholeHTML_bsObj.find("ol",class_ = "grid_view")
        
        movieBrief_list = mainGrid.find_all("li")
        
        for movie in movieBrief_list:
            
            movieName = movie.find_all("span",class_ = "title")   #查电影的名字
            movieOtherName = movie.find("span",class_ = "other")    #查电影的其他名字
            movieLink = movie.find('a').attrs['href'] #电影详细内容链接
            
            
            movieName.append(movieName[0])
            
            movieBrief_csvWriter.writerow([movieName[0].text.replace(u'\xa0', u' '),
                                           movieName[1].text.replace(u'\xa0', u' ').replace(" / ",''),
                                           movieOtherName.text.replace(u'\xa0', u' ').replace(" / ",' '),
                                           movieLink
                                           ])
            
            movieGDB.add_Movie(movieName[0].text.replace(u'\xa0', u' '),
                               movieName[1].text.replace(u'\xa0', u' ').replace(" / ",''),
                               movieOtherName.text.replace(u'\xa0', u' ').replace(" / ",' '),
                               movieLink
                               )
        
        '''
        防止查水表
        '''
        time.sleep(2)
        
        print("爬取了第"+str(pageNum)+"次网页数据")
        
    print("源数据爬取完成")
    del movieBrief_csvWriter
