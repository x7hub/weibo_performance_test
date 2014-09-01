#! /bin/env python
# GfxinfoMonitor.py

import subprocess
import time
import sched
import re
import signal
import sys
import thread
import platform
import os

class GfxinfoMonitor(object):
    """ monitor for gfxinfo of Android device
    """

    def __init__(self, pkgname):
        self.timer = 1 # interval for executing adb command
        self.s = sched.scheduler(time.time,time.sleep) # init scheduler
        self.pkgname = pkgname
        self.interrupted = False
        self.result = {} # dict for restoring result
        self.adbPath = self._getAdbPath()

    def start(self):
        """ start to record gfxinfo every $timer seconds
        """
        self._waitForDevice()
        self._enableGfxProfile()
        self._clearOldData()
        self.s.enter(self.timer, 0, self._performOnce, ())
        print 'Monitoring ...'
        self.s.run()
        print 'Exiting ...'

    def interrupt(self):
        print 'Finish monitoring.'
        self.interrupted = True

    def getResult(self):
        return self.result

    def getResultInSum(self):
        ret = {}
        for k,v in self.result.iteritems():
            ret[k] = []
            for item in v:
                splitedline = item.split('\t')
                # print splitedline
                sumofline = float(splitedline[0]) + float(splitedline[1]) + float(splitedline[2])
                ret[k].append(round(sumofline, 2))
        return ret

    def _getAdbPath(self):
        if platform.system() == 'Windows':
            hasAdb = False
            for cmdpath in os.environ['PATH'].split(':'):
                if os.path.isdir(cmdpath) and 'adb.exe' in os.listdir(cmdpath):
                    hasAdb = True
            if hasAdb:
                adbPath = 'adb.exe'
            else:
                adbPath = 'adb\\windows\\adb.exe'
        elif platform.system() == 'Linux':
            hasAdb = False
            for cmdpath in os.environ['PATH'].split(':'):
                if os.path.isdir(cmdpath) and 'adb' in os.listdir(cmdpath):
                    hasAdb = True
            if hasAdb:
                adbPath = 'adb'
            else:
                adbPath = 'adb/linux/adb'
        elif platform.system() == 'Darwin':
            hasAdb = False
            for cmdpath in os.environ['PATH'].split(':'):
                if os.path.isdir(cmdpath) and 'adb' in os.listdir(cmdpath):
                    hasAdb = True
            if hasAdb:
                adbPath = 'adb'
            else:
                adbPath = 'adb/mac/adb'
            pass
        print "using adb : %s\n" % adbPath # execption here if there is no adb
        return adbPath

    def _machine(self):
        """Return type of machine."""
        if os.name == 'nt' and sys.version_info[:2] < (2,7):
            return os.environ.get("PROCESSOR_ARCHITEW6432", os.environ.get('PROCESSOR_ARCHITECTURE', ''))
        else:
            return platform.machine()

    def _os_bits(self):
        """http://stackoverflow.com/questions/7164843/in-python-how-do-you-determine-whether-the-kernel-is-running-in-32-bit-or-64-bi"""
        """Return bitness of operating system, or None if unknown."""
        machine=self._machine()
        machine2bits = {'AMD64': 64, 'x86_64': 64, 'i386': 32, 'x86': 32}
        return machine2bits.get(machine, None)

    def _waitForDevice(self):
        print 'Waiting for device ...'
        cmd = '%s wait-for-device' % self.adbPath
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        for line in p.stdout.readlines():
            print line
        print 'Device connected.'

    def _enableGfxProfile(self):
        cmd = '%s shell setprop debug.hwui.profile true' % self.adbPath
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

    def _clearOldData(self):
        cmd = '%s shell dumpsys gfxinfo %s' % (self.adbPath, self.pkgname)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

    def _performOnce(self):
            self.s.enter(self.timer, 0, self._performOnce, ())
            cmd = '%s shell dumpsys gfxinfo %s' % (self.adbPath, self.pkgname)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            datastart = False
            for line in p.stdout.readlines():
                # print line
                striped = line.strip()
                if striped.startswith(self.pkgname): # start
                    datastart = True
                    activity = re.split(r'/', striped)[1]
                    if not self.result.has_key(activity):
                        self.result[activity] = []
                elif striped.startswith(r'View hierarchy:'): # end
                    break
                elif striped.startswith('Toast'): # fix error caused by Toast info
                    datastart = False
                elif datastart and not striped.startswith(r'Draw') and striped: # data get
                    self.result[activity].append(striped)

if __name__ == '__main__':
    """ test function
    """
    monitor = GfxinfoMonitor(pkgname = 'com.sina.weibo')
    # monitor.start()
    thread.start_new_thread(monitor.start, ())
    time.sleep(3)
    monitor.interrupt()
    time.sleep(1)
    print monitor.getResult()
    print monitor.getResultInSum()
