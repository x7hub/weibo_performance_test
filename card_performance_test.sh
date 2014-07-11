#! /bin/sh
# card_performance_test.sh

TARGET_PKG='com.sina.weibo'

DIR_NOW=`date +%s` # use as sub dir name
DIR_RESULT='result'

# store test output
mkdir -p ${DIR_RESULT}/${DIR_NOW}
cd ${DIR_RESULT}/${DIR_NOW}

# first arg as conainner id
if [ $1 ]
then
    containerid=$1
else
    containerid=102803
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
    ristretto gfxinfo.png   
}

# funcion for reading gfxinfo
function read_gfx_info()
{
    # read gfxinfo
    for i in `seq 3`
    do
        echo '******* read gfxinfo *******'
        adb shell dumpsys gfxinfo ${TARGET_PKG} | sed -n '/Draw\tProcess\tExecute/,/View hierarchy:/p'| tee gfxinfo${i}.cvs | grep [0-9] | awk '{printf("%02d %s\n", NR, $0)}' >> gfxinfoSum.cvs
        sleep 7
    done
    draw_histogram
}

# start activity, drag down and up
function run_monkey_script()
{
    cat << EOF | monkeyrunner
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
device = MonkeyRunner.waitForConnection()
device.startActivity(uri='sinaweibo://cardlist?containerid=${containerid}')
MonkeyRunner.sleep(5)
for i in range(0,3):
    device.drag((216,768),(216,153),0.1,10)
    MonkeyRunner.sleep(1)
    device.drag((216,768),(216,153),0.1,10)
    MonkeyRunner.sleep(1)
    device.drag((216,153),(216,768),0.1,10)
    MonkeyRunner.sleep(1)
    device.drag((216,768),(216,153),0.1,10)
    MonkeyRunner.sleep(1)
    device.drag((216,153),(216,768),0.1,10)
    MonkeyRunner.sleep(1)
    device.drag((216,153),(216,768),0.1,10)
    MonkeyRunner.sleep(1)

EOF
}

run_monkey_script &
sleep 15
read_gfx_info
