#! /bin/env python
# GfxinfoMonitor.py

import subprocess
import time
import sched
import re
import signal
import sys
import thread

class GfxinfoMonitor(object):
    """ monitor for gfxinfo of Android device
    """

    def __init__(self, pkgname):
        self.timer = 1 # interval for executing adb command
        self.s = sched.scheduler(time.time,time.sleep) # init scheduler
        self.pkgname = pkgname
        self.interrupted = False
        self.result = {} # dict for restoring result

    def start(self):
        """ start to record gfxinfo every $timer seconds
        """
        self._waitForDevice()
        self._enableGfxProfile()
        self._clearOldData()
        self.s.enter(self.timer, 0, self._performOnce, ())
        print "Monitoring ..."
        self.s.run()
        print "Exiting ..."

    def interrupt(self):
        print "Finish monitoring."
        self.interrupted = True

    def getResult(self):
        return self.result

    def getResultInSum(self):
        ret = {}
        for k,v in self.result.iteritems():
            ret[k] = []
            for item in v:
                splitedline = item.split('\t')
                sumofline = float(splitedline[0]) + float(splitedline[1]) + float(splitedline[2])
                ret[k].append(round(sumofline, 2))
        return ret

    def _waitForDevice(self):
        print "Waiting for device ..."
        p = subprocess.Popen('./adb wait-for-device', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        print "Device connected."

    def _enableGfxProfile(self):
        p = subprocess.Popen('./adb shell setprop debug.hwui.profile true', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

    def _clearOldData(self):
        p = subprocess.Popen('./adb shell dumpsys gfxinfo %s' % self.pkgname, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

    def _performOnce(self):
        if not self.interrupted:
            self.s.enter(self.timer, 0, self._performOnce, ())
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

if __name__ == '__main__':
    """ test function
    """
    monitor = GfxinfoMonitor(pkgname = "com.sina.weibo")
    # monitor.start()
    thread.start_new_thread(monitor.start, ())
    time.sleep(3)
    monitor.interrupt()
    time.sleep(1)
    print monitor.getResultInSum()
