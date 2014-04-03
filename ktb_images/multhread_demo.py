# -*- coding: utf-8 -*- 
import threading  
import time     #导入time模块  

class Mythread(threading.Thread):  
    def __init__(self,threadname):  
        threading.Thread.__init__(self,name = threadname)  
    def run(self):  
        time.sleep(2) 
        for i in range(5):
            print '%s is running····'%self.getName()  
   
def join_demo():
    t2 = Mythread('B')  
    t2.start()
    t2.join()     
    for i in range(5):
        print 'the program is running···'
  
if __name__ == "__main__":
    for i in range(0, 100):   
        time.sleep(0.1)   
        view_bar(i, 100)  
