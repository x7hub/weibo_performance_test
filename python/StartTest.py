#! /bin/env python
# StartTest.py

import thread
import time
import os
import json
from GfxinfoMonitor import GfxinfoMonitor

def _find_getch():
    """ http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user """
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

def _readTargetPkg():
    pkg = raw_input("typein pkg name [default com.sina.weibo]: ")
    print pkg
    if len(pkg) < 2: # empty or \n
        return "com.sina.weibo"
    else:
        return pkg

def _dumpRaw(raw):
    ret = ''
    for k,v in raw.iteritems():
        if v:
            ret = ret + "%s\n" % k
            for item in v:
                ret = ret + '%s\n' % item
            ret = ret + '\n'
    return ret

def _dumpStat(stat):
    ret = ''
    for k,v in stat.iteritems():
        if v:
            ret = (ret
                    + "%s\n" % k
                    + "count: %d\n" % v['count']
                    + "avg: %0.4f\n" % v['avg']
                    + "above_16: %d\tratio: %0.4f\n" % (v['above16'], v['above16_ratio'])
                    + "above_30: %d\tratio: %0.4f\n" % (v['above30'], v['above30_ratio'])
                    + "above_50: %d\tratio: %0.4f\n" % (v['above50'], v['above50_ratio'])
                    + "above_80: %d\tratio: %0.4f\n" % (v['above80'], v['above80_ratio'])
                    + "above_100: %d\tratio: %0.4f\n" % (v['above100'], v['above100_ratio'])
                    + "\n"
                    )
    return ret

if __name__ == "__main__":
    print "Starting ..."
    print "press ANYKEY to finish and get result."
    pkg = _readTargetPkg() # get pkg name
    monitor = GfxinfoMonitor(pkg)
    thread.start_new_thread(monitor.start, ()) # start in new thread

    time.sleep(1) # avoid wrong indent
    getch = _find_getch()
    getch() # press anykey to interrupt
    monitor.interrupt()
    raw = monitor.getResult() # get result dict
    if not os.path.exists("result"):
        os.mkdir("result")
    filename_raw = "result/rawdata_%d.cvs" % round(time.time())
    fileobj_raw = open(filename_raw, "wb") # open output target file
    rawdump = _dumpRaw(raw)
    fileobj_raw.write(rawdump) # dump raw data
    fileobj_raw.close()

    result = monitor.getResultInSum() # get result dict
    stat = {} # statistics analysed from the result
    for k,v in result.iteritems(): # caculate stat
        stat[k] = {}
        count = 0
        summary = 0
        above16 = 0
        above30 = 0
        above50 = 0
        above80 = 0
        above100 = 0
        for item in v:
            count += 1
            summary += item
            if item > 16:
                above16 += 1
            if item > 30:
                above30 += 1
            if item > 50:
                above50 += 1
            if item > 80:
                above80 += 1
            if item > 100:
                above100 += 1
        if count == 0:
            continue
        stat[k]['count'] = count
        stat[k]['avg'] = round(summary / count, 2)
        stat[k]['above16'] = above16
        stat[k]['above16_ratio'] = round(float(above16) / count, 4)
        stat[k]['above30'] = above30
        stat[k]['above30_ratio'] = round(float(above30) / count, 4)
        stat[k]['above50'] = above50
        stat[k]['above50_ratio'] = round(float(above50) / count, 4)
        stat[k]['above80'] = above80
        stat[k]['above80_ratio'] = round(float(above80) / count, 4)
        stat[k]['above100'] = above100
        stat[k]['above100_ratio'] = round(float(above100) /count, 4)

    filename_stat = "result/stat_%d.cvs" % round(time.time())
    fileobj_stat = open(filename_stat, "wb") # open output target file
    statdump = _dumpStat(stat)
    print '\n', statdump
    fileobj_stat.write(statdump) # dump statistcs
    fileobj_stat.write('\n')
    fileobj_stat.close()

    time.sleep(1) # wait child thread to exit
