#! /bin/sh
# card_performance_test.sh

# -f    fast scroll
# -p    target page
# -t    test another app

if [ ! -s ~/bin/python ]
then
    mkdir ~/bin
    ln -s /usr/bin/python2 ~/bin/python
    ln -s /usr/bin/python2-config ~/bin/python-config
fi
export PATH=~/bin:$PATH

DIR_NOW=`date +%s` # use as sub dir name
DIR_RESULT='result_tmp'
DIR_SYSTRACE='/opt/android-sdk/platform-tools/systrace/systrace.py'

target_pkg='com.sina.weibo'
sleep_time=0.5
drag_duration=0.05
repeat_times=1
CURRENT_PID=$$

# store test output
mkdir -p ${DIR_RESULT}/${DIR_NOW}
cd ${DIR_RESULT}/${DIR_NOW}

# funcion for reading gfxinfo
function start_systrace()
{
    # set tag
    python ${DIR_SYSTRACE} --set-tags gfx,view
    adb shell stop
    adb shell start
    # start systrace
    python ${DIR_SYSTRACE} -o trace.html
}

# start activity, drag down and up
function run_monkey_script()
{
    cat << EOF | monkeyrunner
import os,signal
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
device = MonkeyRunner.waitForConnection()
for i in range(0,${repeat_times}):
    os.kill(${CURRENT_PID},signal.SIGUSR1)
    device.drag((216,768),(216,153),${drag_duration},10)
    MonkeyRunner.sleep(${sleep_time})
    device.drag((216,768),(216,153),${drag_duration},10)
    MonkeyRunner.sleep(${sleep_time})
    device.drag((216,153),(216,768),${drag_duration},10)
    MonkeyRunner.sleep(${sleep_time})
    device.drag((216,153),(216,768),${drag_duration},10)
    MonkeyRunner.sleep(${sleep_time})
    device.drag((216,768),(216,153),${drag_duration},10)
    MonkeyRunner.sleep(${sleep_time})
    device.drag((216,768),(216,153),${drag_duration},10)
    MonkeyRunner.sleep(${sleep_time})
    device.drag((216,153),(216,768),${drag_duration},10)
    MonkeyRunner.sleep(${sleep_time})
    device.drag((216,153),(216,768),${drag_duration},10)
    MonkeyRunner.sleep(${sleep_time})

EOF
}

run_monkey_script &

trap "start_systrace" SIGUSR1

for i in `seq ${repeat_times}`
do
    wait
done

#if read -n 1 -p "Save ? [Y/n]:"
#then  
#    case $REPLY in  
#        N|n)
#            echo -e "\nexit.\n"  
#            exit
#            ;;
#        *)
#            echo '\n'
#            read -p "Save as :" saveas
#            cp -i gfxinfo.png ../${saveas}.png
#            ;;  
#    esac   
#fi
