#! /usr/bin/env python
# _*_ coding:utf-8 _*_

from threading import Thread
from Queue import Queue,Empty

"""消息对象"""
class Message(object):
    def __init__(self, subject=None):
        self.subject = subject      # 消息主题
        self.dict = {}              # 字典用于保存具体的消息数据



class MsgCenter(object):

    MSG_QUEUE_LEN = 0

    def __init__(self):
        # 消息队列
        self.__msg_queue = Queue(MsgCenter.MSG_QUEUE_LEN)
        # __subscribers字典类型{msg,[subscriber1,subscriber2,...]}
        self.__subscribers = dict()

        self.__thread = Thread(target=self.__run)


    def subscribe(self,subject,subscriber):
        """
        docstring here        
            :param msg: 消息主题
            :param subscriber: 消息订阅者，为Subscriber对象
        """   
        try:
            subscribers = self.__subscribers[subject]            
        except KeyError:
            subscribers = []
        
        self.__subscribers[subject] = subscribers

        if subscriber not in self.__subscribers[subject]:
            self.__subscribers[subject].append(subscriber)
        # self.__subscribers.setdefault(msg.subject,[]).append(subscriber)

    def unsubscribe(self,subject,subscriber):
        """
        docstring here        
            :param msg: 消息，为字符串
            :param subscriber: 消息订阅者，为Subscriber对象
        """           
        try:
            self.__subscribers[subject].remove(subscriber)
        except:
            pass
        
    def Start(self):
        self.__active = True
        self.__thread.start()
        
    
    def Stop(self):
        self.__active = False
        self.__thread.join()

    def __run(self):
        while self.__active == True:
            try:
                # 获取消息的阻塞时间设为1秒
                msg = self.__msg_queue.get(block = True, timeout = 1)  
                self.__msg_process(msg)
            except Empty:
                pass        
    
    def __msg_process(self,msg):

        if msg.subject in self.__subscribers:
            for subscriber in self.__subscribers[msg.subject]:
                subscriber.process(msg)

    def Send(self,msg):
        if self.__msg_queue.full():
            self.__msg_queue.get()
        self.__msg_queue.put(msg)


class Publisher(object):

    def __init__(self, msg_center):
        self.__msg_center = msg_center

    def publish(self, msg):
        print("Publisher send message: {1} of subject {0}".format(msg.subject, msg.dict))
        self.__msg_center.Send(msg)

class Subscriber(object):

    def __init__(self, name, msg_center):
        self.name = name
        self.__msg_center = msg_center

    def subscribe(self, subject):
        self.__msg_center.subscribe(subject, self)

    def unsubscribe(self, subject):
        self.__msg_center.unsubscribe(subject, self)
    
    def process(self, msg):
        print("{} got subject {}, got message{}".format(self.name, msg.subject, msg.dict))        

mc = MsgCenter()
pp = Publisher(mc)
msg = Message('music')
msg.dict['name'] = "hello world"

def notify(args=[],kwargs={}):
    pp.publish(msg)

def main():
    
    mc.Start()

    
    jim = Subscriber('Jim',mc)
    jim.subscribe("music")
    jack = Subscriber('Jack',mc)
    jack.subscribe("music")    


    from timer import Timer
    
    
    mt = Timer(id=1,max_times=10)
    mt.start(0.01, notify)    

    mt1 = Timer(id=2)
    mt1.start(5,(lambda mc: mc.Stop())(mc))
    
    # # 定时器控制线程
    # t = threading.Thread(group=None,target=monitor,args=[mt,10])
    # t.start()
    # t.join()
    # import time

    # time.sleep(50)

if __name__ == '__main__':
    main()