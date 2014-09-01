#! /bin/env python
# StartTest.py
"""  """
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
    result = monitor.getResultInSum() # get result dict
    # print result

    if not os.path.exists("result"):
        os.mkdir("result")
    filename_cvs = "result/rawdata_%d.cvs" % round(time.time())
    fileobj_cvs = open(filename_cvs, "wb") # open output target file

    stat = {} # statistics analysed from the result

    for k,v in result.iteritems(): # dump raw data
        fileobj_cvs.write(k)
        fileobj_cvs.write('\n')
        stat[k] = {}
        count = 0
        summary = 0
        above16 = 0
        above30 = 0
        above100 = 0
        for item in v:
            fileobj_cvs.write(str(item))
            fileobj_cvs.write('\n')
            count += 1
            summary += item
            if item > 16:
                above16 += 1
            if item > 30:
                above30 += 1
            if item > 100:
                above100 += 1
        fileobj_cvs.write('\n')
        if count == 0:
            continue
        stat[k]['count'] = count
        stat[k]['avg'] = round(summary / count, 2)
        stat[k]['above16'] = above16
        stat[k]['above16_ratio'] = round(float(above16) / count, 4)
        stat[k]['above30'] = above30
        stat[k]['above30_ratio'] = round(float(above30) / count, 4)
        stat[k]['above100'] = above100
        stat[k]['above100_ratio'] = round(float(above100) /count, 4)
    fileobj_cvs.write('\n')
    fileobj_cvs.close()

    filename_json = "result/stat_%d.json" % round(time.time())
    fileobj_json = open(filename_json, "wb") # open output target file
    statdump = json.dumps(stat, indent=4, sort_keys=True)
    print statdump
    fileobj_json.write(statdump) # dump statistcs
    fileobj_json.write('\n')
    fileobj_json.close()

    time.sleep(1) # wait child thread to exit
