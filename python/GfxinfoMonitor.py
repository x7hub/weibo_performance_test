#! /bin/env python2
# GfxinfoMonitor.py

import subprocess
import time
import sched
import re
import signal
import sys


class GfxinfoMonitor(object):
    """ monitor for gfxinfo of Android device
    """

    def __init__(self, pkgname):
        self.timer = 1 # interval for executing adb command
        self.s = sched.scheduler(time.time,time.sleep) # init scheduler
        self.pkgname = pkgname
        self.interrupt = False
        self.result = {} # dict for restoring result

    def start(self):
        """ start to record gfxinfo every $timer seconds
        """
        signal.signal(signal.SIGINT, self.__signal_handler)
        self.__waitForDevice()
        self.__enableGfxProfile()
        self.s.enter(self.timer, 0, self.__performOnce, ())
        self.s.run()

    def getResult(self, interrupt = False):
        print "Finish monitoring."
        self.interrupt = interrupt
        return self.result

    def __waitForDevice(self):
        print "Waiting for device ..."
        p = subprocess.Popen('./adb wait-for-device', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        print "Device connected."

    def __enableGfxProfile(self):
        p = subprocess.Popen('./adb shell setprop debug.hwui.profile true', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

    def __performOnce(self):
        if self.interrupt == False :
            self.s.enter(self.timer, 0, self.__performOnce, ())
            p = subprocess.Popen('./adb shell dumpsys gfxinfo %s' % self.pkgname, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            datastart = False
            for line in p.stdout.readlines():
                striped = line.strip()
                if striped.startswith(self.pkgname): # start
                    datastart = True
                    activity = re.split(r'/', striped)[1]
                    if not self.result.has_key(activity):
                        self.result[activity] = []
                elif striped.startswith(r'View hierarchy:'): # end
                    break
                elif datastart and not striped.startswith(r'Draw') and striped: # data get
                    self.result[activity].append(striped)

    def __signal_handler(self, signum, frame):
        if signum == signal.SIGINT :
            print "\nSIGINT catched, finish monitoring."
            self.interrupt = True


if __name__ == '__main__':
    """ test function
    """
    monitor = GfxinfoMonitor(pkgname = "com.sina.weibo")
    monitor.start()
    res = monitor.getResult()
    print res
