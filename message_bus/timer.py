#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

class Timer(object):
    """
    定时器类，用于执行一些定时任务
        :param object: 
    """
    def __init__(self,id=None,max_times=0):
        """
        docstring here
            :param self: 
            :param id=None: 定时器ID，用于多个定时器时定时器的标识
            :param max_times=0: 定时器任务运行次数，为0时为不指定次数
        """   
        self.ID = id
        self.max_times = max_times
        
        # 当前运行次数
        self.times = 0
        
        self._tm = None
        self._fn = None        
        self._args = None
        self._kwargs = None   
        # 定时器
        self._timer = None

    def start(self,tm,func,args=[],kwargs={}):
        """
        启动定时器            
            :param tm: 定时器间隔
            :param func: 定时器触发时执行的函数
            :param args=[]: 定时器触发执行函数参数
            :param kwargs={}: 定时器触发执行函数参数
        """   
        self._fn = func
        self._tm = tm
        self._args = args
        self._kwargs = kwargs     
        print("Timer {0} is running...".format(self.ID))          
        # self._timer = threading.Timer(self._tm, self._do_func, self._args, self._kwargs) 
        self._do_start()
        

    def _do_start(self):
        """
        启动定时器线程            
        """   
        if self._timer == None:
            self._timer = threading.Timer(self._tm, self._do_func, self._args, self._kwargs) 
            # self._timer.
            self._timer.daemon = True
            self._timer.start()        
            
            self._timer.join()

        # print("Thread {} done.".format(threading.enumerate()[1:]))
        # for i in threading.enumerate()[1:]:
        #     self._timer.cancel()
        # print("Thread {} done.".format(threading.enumerate()[1:]))
        # [(lambda t: t.cancel())(timer) for timer in threading.enumerate() if type(timer)==threading._Timer]
        # timer = threading.Timer(self._tm, self._do_func, self._args, self._kwargs) 
        # timer.start()
        # timer.join()        
        self._timer = threading.Timer(self._tm, self._do_func, self._args, self._kwargs) 
        self._timer.start()      
        # self._timer.daemon = True  
        self._timer.join()

    def _do_func(self,args=[],kwargs={}):
        """
        定时器触发时执行的函数            
            :param args=[]: 定时器触发时执行函数的参数
            :param kwargs={}: 定时器触发时执行函数的参数
        """   
        if self._fn:
            if self.max_times == 0:                
                print("\nTimer {0} has running {1} times".format(self.ID,self.times+1))
                self.times = self.times+1
                self._fn(args,kwargs) 
                self._do_start()
            elif self.times<self.max_times:                
                print("\nTimer {0} has running {1} times".format(self.ID,self.times+1))
                self.times = self.times+1
                self._fn(args,kwargs)                              
                self._do_start()                    
            else:
                self.stop()

    def stop(self):
        """
        结束定时器线程
        """   
        try:
            self._timer.cancel()
        except:
            pass

def counter(identity, limit):
    import sys
    import datetime
    for n in range(limit):
        # stderr无缓存，避免线程间交叉输出
        sys.stderr.write('datetime = {}， id = {}, cnt = {}\n'.format(datetime.datetime.now(),identity, n))       

 

def main():
    mt = Timer(id=1,max_times=100)
    mt.start(1, counter,[1,4])    

if __name__ == '__main__':
    main()