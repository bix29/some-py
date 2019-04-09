# -*- coding:utf-8 -*-

import os,time
import threading

rlock = threading.RLock()
curPosition = 0

class Reader(threading.Thread):
    def __init__(self, res):
        self.res = res
        super(Reader, self).__init__()

    def find(self,line):
        # 先按逗号分割，再讲第二部分按照等号分割，然后返回等号后面的值，即 value
        return line.split(',', 1)[1].split('=',1)[1]

    def run(self):
        global curPosition
        fstream = open(self.res.fileName, 'r')
        while True:
            #锁定共享资源
            rlock.acquire()
            startPosition = curPosition
            curPosition = endPosition = (startPosition + self.res.blockSize) if (startPosition + self.res.blockSize) < self.res.fileSize else self.res.fileSize
            #释放共享资源
            rlock.release()
            if startPosition == self.res.fileSize:
                break
            elif startPosition != 0:
                fstream.seek(startPosition)
                fstream.readline()
            pos = fstream.tell()
            while pos < endPosition:
                line = fstream.readline()
                # 输出 Value 值
                print(self.find(line))
                pos = fstream.tell()
        fstream.close()

class Resource(object):
    def __init__(self, fileName):
        self.fileName = fileName
        #分块大小
        self.blockSize = 10000000
        self.getFileSize()
    #计算文件大小
    def getFileSize(self):
        fstream = open(self.fileName, 'r')
        fstream.seek(0, os.SEEK_END)
        self.fileSize = fstream.tell()
        fstream.close()




if __name__ == '__main__':
    # 设置线程数
    threadNum = 4
  
    fileName = '/var/log/test.log'
    res = Resource(fileName)
    threads = []
    #初始化线程
    for i in range(threadNum):
        rdr = Reader(res)
        threads.append(rdr)
    #开始线程
    for i in range(threadNum):
        threads[i].start()
    #结束线程
    for i in range(threadNum):
        threads[i].join()