#! /bin/sh
# card_performance_test.sh

# -f    fast scroll
# -p    target page
# -t    test another app

usage()
{
    echo "Usage: `basename $0` [-f] [-p topic|hot|find|music|home|twitter]"
    exit 1
}

[ $# -eq 0 ] && usage

DIR_NOW=`date +%s` # use as sub dir name
DIR_RESULT='result_tmp'
CURRENT_PID=$$

target_pkg='com.sina.weibo'
up_and_down=0
sleep_time=1
drag_duration=0.05
repeat_times=3

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

if [ -z $scheme ]
then
    echo 'need arg -p'
    exit 1
fi

# funcion for drawing histogram with gfxinfo
function draw_histogram()
{
    cat << EOF | gnuplot
    set title "gfxinfo"
    set terminal png truecolor
    set output "gfxinfo.png"
    set term pngcairo size 3000,2000
    set grid
    set auto x
    unset xtics
    set xtics nomirror rotate by -45 scale 0 font ",8"
    set style data histogram
    set style histogram rowstacked
    set style fill solid border -1
    plot "gfxinfoSum.cvs" using 2:xtic(1) title 'Draw', '' using 3 title 'Process', '' using 4 title 'Execute', 16
EOF
    # ristretto gfxinfo.png
}

# funcion for reading gfxinfo
function read_gfx_info()
{
    adb shell dumpsys gfxinfo ${target_pkg} > /dev/null
    sleep 6
    # read gfxinfo
    echo '******* read gfxinfo *******'
    adb shell dumpsys gfxinfo ${target_pkg} | sed -n '/Draw\tProcess\tExecute/,/View hierarchy:/p'| tee gfxinfo${i}.cvs | grep [0-9] | awk '{printf("%02d %s\n", NR, $0)}' >> gfxinfoSum.cvs
    draw_histogram
}

# start activity, drag down and up
function run_monkey_script()
{
    cat << EOF | monkeyrunner
import os,signal
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
device = MonkeyRunner.waitForConnection()
device.startActivity(uri='${scheme}')
MonkeyRunner.sleep(10)
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

trap "read_gfx_info" SIGUSR1
trap "exit" SIGINT

for i in `seq ${repeat_times}`
do
    wait
done
