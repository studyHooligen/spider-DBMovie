# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 16:27:43 2020

@author: 23731
"""

import neo4j
from neo4j import (GraphDatabase, WRITE_ACCESS, unit_of_work)

class myNeo4j:
    def __init__(self, 
                 url = "neo4j://localhost:7687", 
                 userName = "neo4j", 
                 password = "1234567890"):
        '''
        创建一个neo4j图数据库操作对象
        
        Parameters
        ----------
        url : str
            数据库路径，默认为本地的7687端口路径
        userName : str
            登陆用户名
        password : str
            登陆密码

        Returns
        -------
        None.

        '''
        self.driver = GraphDatabase.driver(url, auth=(userName,password))

    def __del__(self):
        '''
        对象析构函数

        Returns
        -------
        None.

        '''
        self.driver.close()
    
    '''
    neo4j库进行增删改查时使用的内部session
    禁止外部调用！
    BEGIN
    '''
    def __search_Movie(self,tx,movieName):
        '''
        功能：电影查找
        说明：根据电影主名字查找
        '''
        res = tx.run('''MATCH (
                a:movie {name: $name}) RETURN (a) AS mv''',
                name=movieName
                )
        resList = []
        for i in res:
            resList.append(i["mv"])
        return resList
    
    def __add_Movie(self,tx,movieName,originalName,otherName,
                    link,country,year,date,length,score):
        return tx.run('''
                      MERGE (
                          m:movie {
                              name : $movieName,
                              originalName : $originalName,
                              otherName : $otherName,
                              link : $link,
                              country : $country,
                              year : $year,
                              date : $date,
                              length : $length,
                              score : $score})
                      RETURN (m)
                      ''',
                      movieName = movieName,
                      originalName = originalName,
                      otherName = otherName,
                      link = link,
                      country = country,
                      year = year,date = date,
                      length = length,score = score).single().value()
    
    def __add_director(self,tx,name,link):
        return tx.run('''
                      MERGE (d:director {
                          name : $directorName,
                          link : $directorLink})
                      RETURN (d)
                      ''',
                      directorName = name,
                      directorLink = link).single().value()
    
    def __add_actor(self,tx,name,originalName,sex,birthday,country,link):
        
        return tx.run('''
                      MERGE (a:actor {
                          name : $actorName,
                          originalName : $actorOrgName,
                          sex : $actorSex,
                          birthday : $actorBirthday,
                          country : $actorCountry,
                          link : $actorLink})
                      RETURN (a)
                      ''',
                      actorName = name,
                      actorOrgName = originalName,
                      actorSex = sex,
                      actorBirthday = birthday,
                      actorCountry = country,
                      actorLink = link).single().value()
    
    def __add_movieType(self,tx,mType):
        return tx.run('''
                      MERGE (t:movieType {
                          name : $mtype})
                      RETURN t
                      ''',
                      mtype = mType).single().value()
    
    def __establishRelation(self,tx,
                            srcType,srcName,
                            tarType,tarName,
                            relation):
        return tx.run('''
                      MATCH (a:'''+srcType+''' {name:$srcN}),
                      (b:'''+tarType+''' {name : $tarN}) 
                      CREATE (a) -[r:'''+relation+''']-> (b)
                      RETURN a,b,r
                      ''',
                      srcN = srcName,
                      tarN = tarName).single().value()
    '''
    neo4j内部session定义
    END
    '''
    
    def add_Movie(self,
                  movieName,
                  originalName = '', otherName = '',
                  infPageLink = '',
                  country = '',
                  year = 0,date = 0,
                  length = 120,score = 0):
        '''
        

        Parameters
        ----------
        movieName : str
            电影名字.
        originalName : str
            电影原名.
        otherName : str
            其他名字.
        infPageLink : str
            电影内容页面链接

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        
        with self.driver.session() as session:
            return session.write_transaction(self.__add_Movie,   
                                                movieName,
                                                originalName, otherName,
                                                infPageLink,
                                                country,
                                                year,date,
                                                length,score
                                                );
    
    def add_director(self,name,link = ''):
        '''
        添加导演

        Parameters
        ----------
        name : STR
            导演名字.
        link : STR
            导演页面链接.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        with self.driver.session() as session:
            return session.write_transaction(self.__add_director,
                                             name,link);
        
    def add_scriptwriter(self,name,link = ''):
        '''
        添加编剧人物对象

        Parameters
        ----------
        name : STR
            编剧名字
        link : STR
            编剧的个人页面

        Returns
        -------
        None.

        '''
        def __add_scriptwriter(tx,name,link):
            return tx.run('''
                          MERGE (d:scriptwriter {
                              name : $directorName,
                              link : $directorLink})
                          RETURN (d)
                          ''',
                          directorName = name,
                          directorLink = link).single().value()
        
        with self.driver.session() as session:
            return session.write_transaction(__add_scriptwriter,name,link);
        
    def add_actor(self,
                  name,
                  originalName,
                  sex = True,
                  birthday = '1997-14-2',
                  country = '',
                  link = ''):
        '''
        添加演员

        Parameters
        ----------
        name : STR
            演员名字.
        originalName : STR
            原名.
        sex : bool
            性别，男生true，女生false.
        birthday : int
            生日时间戳，例如：20200819.
        country : STR
            演员所在国家.
        link : STR
            演员页面链接.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        with self.driver.session() as session:
            return session.write_transaction(self.__add_actor,
                                             name,originalName,sex,
                                             birthday,country,link);
    
    def add_movieType(self,mType):
        '''
        添加电影类型

        Parameters
        ----------
        mType : STR
            电影类型名，例如：喜剧、动作.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        with self.driver.session() as session:
            return session.write_transaction(self.__add_movieType,mType);
    
    def establishRelation_director2movie(self,
                                         directorSrcName,movieTargName,
                                         relation = "导演"):
        '''
        建立导演和电影的关系

        Parameters
        ----------
        directorSrcName : STR
            导演名字.
        movieTargName : STR
            电影名字.
        relation : STR
            关系.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        with self.driver.session() as session:
            return session.write_transaction(self.__establishRelation,
                                             "director",directorSrcName,
                                             "movie",movieTargName,
                                             relation);
    
    def establishRelation_srcriptWriter2movie(self,srcName,targName,relation = "编剧"):
        with self.driver.session() as session:
            return session.write_transaction(self.__establishRelation,
                                             "scriptwriter",srcName,
                                             "movie",targName,
                                             relation);
    
    def establishRelation_movie2type(self,srcName,targName,relation = "电影类型"):
        with self.driver.session() as session:
            return session.write_transaction(self.__establishRelation,
                                             "movie",srcName,
                                             "movieType",targName,
                                             relation);
    
    def establishRelation_actor2movie(self,srcName,targName,relation = "参演"):
        with self.driver.session() as session:
            return session.write_transaction(self.__establishRelation,
                                             "actor",srcName,
                                             "movie",targName,
                                             relation);
    
    def establishRelation_actor4director(self,srcName,targName,relation = "合作关系"):
        with self.driver.session() as session:
            return session.write_transaction(self.__establishRelation,
                                             "actor",srcName,
                                             "director",targName,
                                             relation);
    
    def establishRelation_movie4movie(self,srcName,targName,relation = "喜欢该电影的也喜欢"):
        with self.driver.session() as session:
            return session.write_transaction(self.__establishRelation,
                                             "movie",srcName,
                                             "movie",targName,
                                             relation);
    
    
    def cleanDatabase(self):
        '''
        清空数据库里面的所有数据

        Returns
        -------
        None.

        '''
        def __cleanRelation(tx):
            return tx.run('''MATCH (n)-[r]->(m) DELETE r''')
        
        def __cleanNode(tx):
            return tx.run('''MATCH (n) DELETE n''')
        
        # def __cleanAll(tx):
        #     return tx.run('''MATCH (n)-[r]->(m) DELETE r,n,m''')
        
        with self.driver.session() as session:
            session.write_transaction(__cleanRelation);
            session.write_transaction(__cleanNode);
    
    def search_Movie(self,movieName):
        '''
        查找电影资料

        Parameters
        ----------
        movieName : STR
            查找的电影名称.

        Returns
        -------
        None.

        '''
        with self.driver.session() as session:
            return session.read_transaction(self.__search_Movie,movieName);
            
if __name__ == "__main__":
    neoObj = myNeo4j();
    