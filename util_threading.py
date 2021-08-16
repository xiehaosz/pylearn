# coding: UTF-8

import threading
import _thread  # 兼容py2.0的多线程
import time
import queue


# 为线程定义一个函数
def print_time(thread_name, delay, counter):

    while counter:
        time.sleep(delay)
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1


def print_time_return(thread_name, delay, counter):
    rtn = []
    while counter:
        time.sleep(delay)
        rtn.append((thread_name, time.ctime(time.time())))
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1
    return rtn


# threading.Thread 继承创建子类，实例化后调用start()方法启动新线程，即它调用了线程的run() 方法，好处是可任意重写
class MyThread (threading.Thread):
    def __init__(self, thread_id, name, delay, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.delay = delay
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # # 获取锁，锁住后其他进程将暂停直到该线程释放
        # threadLock.acquire()
        print_time(self.name, self.delay, self.counter)
        print("退出线程：" + self.name)
        # # 释放锁，开启下一个线程
        # threadLock.release()


threadLock = threading.Lock()


class MyThreadQ (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.name, self.q)
        print("退出线程：" + self.name)


def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print("%s processing %s" % (threadName, data))
        else:
            queueLock.release()
        time.sleep(1)


exitFlag = 0
workQueue = queue.Queue(10)
queueLock = threading.Lock()

# 创建两个线程
try:
    # ============================================================
    # # 直接起线程
    # # 主线程（如果主线程结束所有子线程会一起结束，不管子线程是否结束）
    # # _thread.start_new_thread(print_time, ("Thread-1", 1, 3))  # Py2.0
    # # _thread.start_new_thread(print_time, ("Thread-2", 2, 3))

    # thread1 = threading.Thread(target=print_time, args=("Thread-1", 1, 3))  # py3.0
    # thread2 = threading.Thread(target=print_time, args=("Thread-2", 2, 3))
    # thread1.start()
    # thread2.start()

    threads = []
    thread1 = threading.Thread(target=print_time_return, args=("Thread-1", 1, 3))  # py3.0
    thread2 = threading.Thread(target=print_time_return, args=("Thread-2", 2, 3))
    thread1.start()
    thread2.start()



    ccc = 10
    while ccc > 0:
        time.sleep(1)
        print(thread1.isAlive(), thread2.isAlive())
        ccc -= 1

    # ============================================================
    # # 通过类创建线程
    # thread1 = MyThread(1, "Thread-A", 1, 3)
    # thread2 = MyThread(2, "Thread-B", 2, 3)
    #
    # list_tsk = []
    # list_tsk.append(thread1)
    # list_tsk.append(thread2)
    #
    # # for tsk in list_tsk:
    # #     # 启动线程
    # #     tsk.start()
    # #     tsk.join()  # 加入主线程，join后必须等待该线程结束才能继续后续代码，此前已经启动的线程不受影响
    #
    # # join的执行顺序对比：
    # for tsk in list_tsk:
    #     # 启动线程
    #     tsk.start()
    #
    # # for tsk in list_tsk:
    # #     tsk.join()  # 加入主线程，join后必须等待该线程结束才能继续后续代码，Join可输入参数等待时间s
    #
    # ccc = 10
    # while ccc > 0:
    #     time.sleep(1)
    #     print(thread1.isAlive(), thread2.isAlive())
    #     ccc -= 1

    # ============================================================
    # thread_ist = ["Thread-1", "Thread-2", "Thread-3"]
    # name_list = ["One", "Two", "Three", "Four", "Five"]
    # threads = []
    # thread_id = 1
    #
    # # 创建新线程
    # for tName in thread_ist:
    #     thread = MyThreadQ(thread_id, tName, workQueue)
    #     thread.start()
    #     threads.append(thread)
    #     thread_id += 1
    #
    # # 填充队列
    # queueLock.acquire()
    # for word in name_list:
    #     workQueue.put(word)
    # queueLock.release()
    #
    # # 等待队列清空
    # while not workQueue.empty():
    #     pass
    #
    # # 通知线程是时候退出
    # exitFlag = 1
    #
    # # 等待所有线程完成
    # for t in threads:
    #     t.join()

    # ============================================================
    print("我是后续代码")

except:
    print("Error: 无法启动线程")



    
    
    # -*-* encoding:UTF-8 -*-
# 展示加锁和不加锁时，对数据修改情况

import threading
import time
list = [0,0,0,0,0,0,0,0,0,0,0,0]
class myThread(threading.Thread):
    def __init__(self,threadId,name,counter):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.counter = counter
    def run(self):
        print("开始线程:",self.name)
        # 获得锁，成功获得锁定后返回 True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回 False
        threadLock.acquire()
        print_time(self.name,self.counter,list.__len__())
        # 释放锁
        threadLock.release()
    def __del__(self):
        print(self.name,"线程结束！")
def print_time(threadName,delay,counter):
    while counter:
        time.sleep(delay)
        list[counter-1] += 1
        print("[%s] %s 修改第 %d 个值，修改后值为:%d" % (time.ctime(time.time()),threadName,counter,list[counter-1]))
        counter -= 1

threadLock = threading.Lock()
threads = []
# 创建新线程
thread1 = myThread(1,"Thread-1",1)
thread2 = myThread(2,"Thread-2",2)
# 开启新线程
thread1.start()
thread2.start()
# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)
# 等待所有线程完成
for t in threads:
    t.join()
print("主进程结束！")




#!/usr/bin/python3

import time

import threading

import sys
import threading
import queue

q = queue.Queue()


def worker1(x, y):
    func_name = sys._getframe().f_code.co_name
    print("%s run ..." % func_name)
    q.put((x + y, func_name))


def worker2(x, y):
    func_name = sys._getframe().f_code.co_name
    print("%s run ...." % func_name)
    q.put((x - y, func_name))


if __name__ == '__main__':
    result = list()
    t1 = threading.Thread(target=worker1, name='thread1', args=(10, 5, ))
    t2 = threading.Thread(target=worker2, name='thread2', args=(20, 1, ))
    print('-' * 50)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    while not q.empty():
        result.append(q.get())
        print(result)

    for item in result:
        if item[1] == worker1.__name__:
            print("%s 's return value is : %s" % (item[1], item[0]))
        elif item[1] == worker2.__name__:
            print("%s 's return value is : %s" % (item[1], item[0]))


            
            
#!/usr/bin/python3

import threading
import time


# MyThread.py线程类
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None


def add():
    sumup = 0
    for iii in range(5):
        sumup+=1
        # print(sumup)
        time.sleep(1)
    return sumup


if __name__=="__main__":
    thrds = []
    # 创建4个线程
    for i in range(3):
        task = MyThread(add, )
        thrds.append(task)
    #
    # for thrd in thrds:
    #     print(thrd.get_result())

