# -*- coding: utf-8 -*-

from queue import Queue,deque

class urlCtrl:
    def __init__(self):
        '''
        创建URL管理器对象

        Returns
        -------
        None.

        '''
        self.__queueCache = deque();
        
    def empty(self):
        if len(self.__queueCache) == 0:
            return True;
        else:
            return False;
        
    def add_URL(self,URL,Name = ''):
        '''
        向管理器中添加URL和对应的名字

        Parameters
        ----------
        URL : str
            url字符串.
        Name : str, optional
            网址名称. The default is ''.

        Returns
        -------
        None.

        '''
        self.__queueCache.append((Name,URL));
        
    def get_URL(self):
        '''
        从URL管理器中提取一个单位

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        return self.__queueCache.popleft();
    
    def rollBack_URL(self):
        '''
        回滚上一次放进管理器的URL数据

        Returns
        -------
        (Name,URL).
            名字+URL
        '''
        return self.__queueCache.pop();
    
    def clear(self):
        '''
        清空管理器中所有的数据
        '''
        self.__queueCache.clear();
    
    def __len__(self):
        return len(self.__queueCache)
        
if __name__ == '__main__':
    ctrl = urlCtrl();
