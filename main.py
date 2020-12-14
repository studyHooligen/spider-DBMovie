# -*- coding: UTF-8 -*-
import urllib3 
import bs4
from bs4 import BeautifulSoup
import time

import myCSV
import myNeo4j

#下载器
http = urllib3.PoolManager()

#图数据库
movieGDB = myNeo4j.myNeo4j();

#本地csv数据文件
# movieBrief_csvfile = open("./csvData/movieBrief.csv","w",newline='')
# movieBrief_csvWriter = csv.writer(movieBrief_csvfile)
movieBrief_csvWriter = myCSV.myCSV("./csvData/movieBrief.csv","wb","utf-8")

movieBrief_csvWriter.writerow(["电影名字",
                               "电影原名",
                               "其他名字",
                               "详细内容链接",
                               "导演",
                               "主演",
                               "年份",
                               "地区",
                               "评语"
                               ])

urlRoot = "https://movie.douban.com/top250?start="

pageNum = 0 #遍历用的页面号
while pageNum < 10:
    
    urlNow = urlRoot + str(pageNum*25)    #当前要爬的路径
    
    r = http.request('GET',urlNow)  #下载数据
    
    if(r.status != 200):    #检测是否请求失败（被豆瓣查水表）
        print("get error,status code:",str(r.status))
        exit(-1)
    
    pageNum += 1    #迭代
    
    '''
    存储网页数据
    '''
    localSaveFile = open("./sourceHTMl/豆瓣电影top250-"+str(pageNum)+".html",mode = "wb")
    
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
