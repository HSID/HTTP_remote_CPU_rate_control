#!/usr/bin/env python

import threading
import time
import os
import string
import sys

class ControlThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.runflag = True

    def run(self):
        while self.runflag:
            #os.popen('usleep' + ' ' + sys.argv[5])
            time.sleep(string.atof(sys.argv[5]))

    def stop(self):
        self.runflag = False

threadList = []

print 'Start Thread Number:' + sys.argv[3] + '\tSleep Time (ms):' + sys.argv[5]

for i in range(0, string.atoi(sys.argv[3])):
    thread = ControlThread()
    threadList.append(thread)
    thread.start()

while True:
    try:
        output = 100 - string.atof(os.popen('sar 1 1 | grep ^Average | awk \'{print $8}\'').read())
        print 'CPU Usage:' + str(output) + '\tCurrent Thread Number:' + str(len(threadList))

        if output < string.atoi(sys.argv[1]):
            for i in range(0, string.atoi(sys.argv[4])):
                thread = ControlThread()
                thread.start()
                threadList.append(thread)
            print '++++++'
        if output > string.atoi(sys.argv[2]):
            for i in range(0, string.atoi(sys.argv[4])):
                thread = threadList.pop()
                thread.stop()
            print '------'
    except KeyboardInterrupt:
        for i in range(0, len(threadList)):
            thread = threadList.pop()
            thread.stop()
        exit(0)
