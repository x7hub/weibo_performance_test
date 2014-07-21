#! /bin/sh
# card_performance_test.sh

# -f    fast scroll
# -p    target page
# -t    test another app

# prepare python2
python_version=`python -V 2>&1 | awk '{print $2}'`
if [ ${python_version:0:1} = 3 ] && [ ! -s ~/bin/python ]
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
up_and_down=0
CURRENT_PID=$$

# store test output
mkdir -p ${DIR_RESULT}/${DIR_NOW}
cd ${DIR_RESULT}/${DIR_NOW}

# first arg
while getopts fp: opt
do
    case $opt in
        p)
            case $OPTARG in
                'topic')
                    echo 'OPTARG topic'
                    scheme='sinaweibo://pageinfo?containerid=100808db057fb6820d53fee904474bcbb75b1a'
                    ;;
                'hot' )
                    echo 'OPTARG hot'
                    scheme='sinaweibo://cardlist?containerid=100803'
                    ;;
                'find')
                    echo 'OPTARG find'
                    scheme='sinaweibo://cardlist?containerid=1087030002_417'
                    up_and_down=1
                    ;;
                'music')
                    echo 'OPTARG music'
                    scheme='sinaweibo://cardlist?containerid=10140310001'
                    ;;
                'home')
                    echo 'OPTARG home'
                    scheme='sinaweibo://gotohome'
                    ;;
                'twitter')
                    echo "OPTARG twitter"
                    scheme='twitter://timeline'
                    target_pkg='com.twitter.android'
                    ;;
                \?)
                    echo -e 'invalid arg'
                    exit 1
                    ;;
            esac
            ;;
        f)
            sleep_time=0.5
            drag_duration=0.01
            ;;
        *)
            echo -e 'invalid arg'
            exit 1
            ;;
    esac
done



# funcion for reading gfxinfo
function start_systrace()
{
    # set tag
    python ${DIR_SYSTRACE} --set-tags gfx,view
    adb shell stop
    adb shell start
    # start systrace
    python ${DIR_SYSTRACE} --time=10 -o trace.html
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
    if ${up_and_down} == 0:
        for i in range(0,15):
            device.drag((216,768),(216,153),${drag_duration},10)
            MonkeyRunner.sleep(${sleep_time})
    else:
        for i in range(0,8):
            device.drag((216,768),(216,153),${drag_duration},10)
            MonkeyRunner.sleep(${sleep_time})
            device.drag((216,153),(216,768),${drag_duration},10)
            MonkeyRunner.sleep(${sleep_time})

EOF
}

run_monkey_script &

trap "start_systrace" SIGUSR1
trap "exit" SIGINT

for i in `seq ${repeat_times}`
do
    wait
done
